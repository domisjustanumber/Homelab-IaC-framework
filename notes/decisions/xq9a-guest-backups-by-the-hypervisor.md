# xq9a — The hypervisor backs up each guest; no backup agent in the guest

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user).

This entry restates the generic rules of site 0023. A site entry restates its site values (the
backup windows of the host) and supersedes site 0023.

## Decision

1. **No agent in the guest.** A guest runs no backup agent and no scheduled backup. Proxmox VE backs
   up the whole VM to Proxmox Backup Server (PBS).
2. **Filesystem-consistent.** The `base` role installs `qemu-guest-agent`. The agent must be on in
   the VM options, so that the backup freezes the filesystems (fsfreeze).
3. **Backup window.** The backup job of a guest does not run during the maintenance jobs of that
   guest ([eq0z](eq0z-unattended-upgrades-and-reboots.md)).
4. **PBS jobs.** Retention, verification and the off-site copy are PBS jobs: a prune job, a verify
   job and a sync job. Check that they exist. Do not assume them. This entry does not manage them.
5. **Restore drill.** Before a host goes live, and after each change to its disks or to the
   datastore, restore the VM to a scratch VMID, boot it, and check its services and its database.
   The scratch VM must have no network access:
   - Restore with `qmrestore --unique`, so that each network device gets a new MAC address.
   - Before the first boot, set `link_down=1` on each network device, or attach it to a bridge with
     no uplink and no route to the LAN. Set `onboot` to `0`.
   - Do the checks from the console. Delete the scratch VM after the drill.
6. **Recovery path.** A VM restore, plus 1Password, plus the Git repositories.

## Reason

- The Proxmox VE nodes already back up to PBS. A second backup system in the guest duplicates the
  storage, the credentials, the retention, the alerts and the patches.
- A VM backup holds all that a host needs: the database datadir, the application files, the ACME
  store, the state of the services and the deployed config.
- PBS gives deduplication, encryption and retention in one place, and one restore procedure for each
  guest.
- The backup cannot drift from what is on the disks.
- fsfreeze needs the guest agent. Without it, the backup is only crash-consistent.
- A restored VM is a copy of the live VM: the same IP address, hostname and credentials. On the
  network, it takes the address of the live VM, it announces the same name, and its tunnel and API
  credentials let it serve public traffic or change shared state from old data.

## Consequences

- No backup daemon, repository password or schedule in the guest.
- fsfreeze makes the backup filesystem-consistent, not application-consistent. A database recovers
  from it as after a crash (InnoDB crash recovery).
- The main restore is a whole-VM restore. A restore of single files from PBS is possible, but slower.
- The correctness of the backup is outside the guest. The restore drill is the only real check.
- A restore takes the guest back to the time of the last backup.

## Alternatives rejected

- **`restic` in the guest.** It duplicates a backup system that already runs.
- **A database dump on a schedule only.** It protects the database, not the files, the ACME state or
  the config.
- **Proxmox snapshots only.** The same datastore, and no versions beyond the snapshot chain. A
  snapshot is not a backup.
- **No backup.** Not acceptable for a public service.

## Not repeated

- Do not treat a Proxmox snapshot as a backup.
- Do not boot a restore drill with its network devices connected to the LAN.
- Do not assume that the PBS prune, verify and sync jobs exist. Check them.
