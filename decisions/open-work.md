# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The change that closes an item records the result.

- **Restate the generic stack contract before [0003](0003-controller-pushes-stacks.md) is
  accepted.** site 0042 holds the stack contract. Its generic rules stay: the host layout under
  `stack_dir`, the `.env` that Ansible owns, the `.env.example` contract, the generic stack with no
  host values, the recreate of a service when its `config/<service>/` files change, host values
  through the environment or `command:` flags only, no inline `configs:` on a service that Watchtower
  manages, `${VAR:?message}` for each mandatory value, the `common/` fragments and the inline-config
  hash. Restate them without site values, in 0003 or in an entry of their own if 0003 then exceeds
  its limit. Decide whether "deploys follow `main` only" stays. A site entry restates the site
  values of site 0042 and supersedes it.
- **Decide the open parts of 0003 before it is accepted:** one Compose project per host or several,
  how public and private stacks are composed and what the push copies, and whether the Compose
  files are renamed for Dependabot.
- **Site exceptions to framework rules.** The user decided (2026-10-25): this log decides which of
  its rules allow a site exception, and how. A site entry records each use of that mechanism. A
  rule with no exception mechanism needs a change in this log first. When a rule is written here,
  state whether it allows a site exception and what the site entry must hold. The first known
  case is an application that must mount the Docker socket.
- **Write the storage entry for Docker on an LXC.** [CVM2](CVM2-storage-layout-containerd-root-by-flag.md)
  covers each Docker host, and [MSAM](MSAM-docker-host-vm-disks.md) covers a VM only. An LXC entry
  needs the answers to these questions first: which Docker hosts are LXCs, and are they unprivileged;
  the container storage of each node (ZFS subvol, LVM-thin or directory); whether state comes from
  the node or a NAS through a bind mount or NFS, and who backs it up; and whether AppArmor
  `unconfined` is acceptable. Known rules: each mount point sets `backup=1` (vzdump leaves mount
  points out by default); no state on a host bind mount; `nesting=1`, with `keyctl=1` when
  unprivileged; `pct fstrim` and `pct resize`; overlayfs on ZFS needs OpenZFS 2.2 or later.
  [BQXN](BQXN-debian-hosts-and-the-base-role.md) rule 4 and [XQ9A](XQ9A-guest-backups-by-the-hypervisor.md)
  rule 2 assume a VM (`qemu-guest-agent`). A later entry decides them for an
  LXC.
- **Changed conffiles hold packages back.** When a role changes a conffile and a later release
  changes the shipped copy, `unattended-upgrades` holds the package back, with no error.
  [CVM2](CVM2-storage-layout-containerd-root-by-flag.md) removes this case for containerd. Two
  roles still change a conffile: `avahi` (`/etc/avahi/avahi-daemon.conf`) and
  `apt_unattended_upgrades` (`/etc/apt/apt.conf.d/50unattended-upgrades`). Decide for each: a
  separate file (for example a later file in `apt.conf.d/`), or a verify check for held-back
  packages.
