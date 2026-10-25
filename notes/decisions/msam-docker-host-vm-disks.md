# msam — A Docker host VM has three disks, and all three are in the backup

**Status:** proposed, 2026-10-25 (agent).

This entry restates the VM rules of site 0034. The storage rules for each Docker host are in
[s3xt](s3xt-storage-layout-and-bind-mounted-state.md). A site entry restates the site values of site
0034 and supersedes it.

## Decision

1. **Three virtual disks.**
   - `/`: the OS, the packages, journald and a swapfile;
   - the churn disk: the containerd root and the Docker data-root;
   - the state disk, mounted at `docker_dir`: all persistent container state.

   The site records the size of each disk.
2. **Filesystem.** Each disk is ext4 and is mounted by UUID. `discard=on` is set on the hypervisor,
   and `fstrim.timer` runs in the guest. There is no LVM in the guest. Each disk grows alone, with
   `qm resize` and then `resize2fs`. When a disk has a partition table, `growpart` comes before
   `resize2fs`.
3. **All three disks in the backup.** The backup job of the VM includes each disk. Do not set
   `backup=0` on the churn disk until the stateful services are pinned by digest and a restore
   runbook holds the image updates for one cooldown.

## Reason

- Separate virtual disks isolate the three kinds of data without LVM in the guest, and each one grows
  on its own.
- PBS splits a VM disk into fixed chunks of 4 MiB and stores each chunk once. A backup uploads only
  the chunks that PBS does not have yet, and a dirty bitmap limits the read to the changed blocks.
  With `discard=on` and `fstrim`, freed blocks read as zeros. The nightly cost of the churn disk is
  therefore about its new image layers and logs.
- A restore with all three disks is byte-identical and has one step.
- A restore without the churn disk has no disk at its UUID, so its mount fails until a person
  creates and formats a new disk.
- Without the churn disk, a restore pulls each image again. For a moving tag, a pull can get an image
  that is newer than the update cooldown allows. Only a digest pin makes a pull identical.

## Consequences

- Three disks to size and grow, not one.
- The backup holds images that can be rebuilt. With deduplication, the cost is small.
- After a stop of the QEMU process, the dirty bitmap is gone. The next backup reads the whole disk,
  but it still uploads only the new chunks.
- Docker on an LXC needs its own entry: mount points, their `backup=` flag, the storage driver and
  the UID mapping differ.

## Evidence

- PBS chunks, deduplication and dirty bitmaps:
  [PBS technical overview](https://pbs.proxmox.com/docs/technical-overview.html).
- Per-disk backup flag: [Qemu/KVM Virtual Machines](https://pve.proxmox.com/wiki/Qemu/KVM_Virtual_Machines).
- The loss of the dirty bitmap after a QEMU stop is from the Proxmox forum, not from the official
  docs.

## Alternatives rejected

- **Two disks, with the churn on `/`.** An image pull can then fill `/`, and apt and journald stop.
- **One disk with LVM volumes.** The same isolation, but a resize needs LVM in the guest.
- **The churn disk out of the backup (`backup=0`).** A smaller backup, but a two-step restore, and a
  re-pull of moving tags. Look at it again after digest pins.
- **State on a host dataset through virtiofs.** Host snapshots and replication, but the state is then
  outside the VM backup, and the UID mapping and the database performance are open questions.

## Not repeated

- Do not exclude the churn disk from the backup while moving tags are in use.
