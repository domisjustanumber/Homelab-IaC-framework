# CVM2 — Docker hosts keep state apart from image churn; the containerd root is set by a flag

**Status:** proposed, 2026-10-29 (agent); accepted, 2026-10-29 (user).

Supersedes [S3XT](S3XT-storage-layout-and-bind-mounted-state.md) in full. This entry restates each
rule of S3XT. It changes one: how the `docker_engine` role sets the containerd root. S3XT restated
the generic rules of site 0034. A VM host also follows [MSAM](MSAM-docker-host-vm-disks.md).

## Decision

1. **Scope.** These rules apply to each Docker host, VM or LXC. They do not apply to Proxmox VE
   nodes, appliances or guests without Docker.
2. **Two storage units.** A state unit is mounted at `docker_dir` (for example `/docker`). A churn
   unit holds the containerd root and the Docker data-root: images, snapshots, container layers and
   container logs. The host type decides what a unit is: a disk for a VM ([MSAM](MSAM-docker-host-vm-disks.md)),
   a mount point for an LXC (a later entry).
3. **Image store.** The hosts use the default containerd image store of Docker Engine. The
   `docker_engine` role sets the containerd root with the `--root` flag, in a drop-in on
   `containerd.service`. It sets the Docker `data-root` in `daemon.json`. Both are folders on the
   churn unit. The paths are role defaults. The containerd root is a folder that `dockerd` does not
   use. The role does not change `/etc/containerd/config.toml`.
4. **Mounts are enforced.** The inventory lists the mounts in `docker_storage_mounts`. The preflight
   of each playbook refuses to run while one of them is not mounted. The role adds a drop-in with
   `RequiresMountsFor=` to `containerd.service` and to `docker.service`, for the containerd root,
   the data-root, `docker_dir` and those mounts. A path that is not its own mount requires only `/`,
   so the drop-ins are safe on a host with one disk.
5. **No named volumes for state.** Each persistent path of a container is a bind mount under
   `${STACK_DIR}/appdata/` or `${STACK_DIR}/logs/`. Ansible creates it from `stack_runtime_paths`,
   with the owner and mode that the container needs.
6. **Image `VOLUME` paths.** Each `VOLUME` that an image declares is bound under `${STACK_DIR}`, or
   the stack records it as disposable.
7. **Backup.** The state unit is always in the backup of the host. The host type decides the backup
   of the churn unit.

## Reason

- The OS grows slowly, images grow in spikes, and state grows steadily and needs the backup. On one
  filesystem, an image pull that fills the disk also stops the database writes.
- When a mount fails at boot, the daemons write into the empty mount point on `/`, and the database
  creates a fresh datadir.
- With the containerd image store, `data-root` does not move the images. containerd keeps them in
  its own root, by default on `/`. Docker's docs say to configure it separately, to avoid a full root
  partition. A drop-in on `docker.service` alone does not stop `containerd.service`.
- `/etc/containerd/config.toml` is a conffile of the `containerd.io` package. When a host changes it
  and a later release changes the shipped copy, `unattended-upgrades` holds the package back, with
  no error ([EQ0Z](EQ0Z-unattended-upgrades-and-reboots.md) rule 1 then fails for the Docker
  origin). The `--root` flag leaves the conffile as shipped, and the shipped settings still apply.
- A bind mount survives `docker compose down -v`, `docker volume prune -a` and a renamed project,
  and Ansible sets its owner and mode. A named volume is on the churn unit, and `down -v` deletes it.
- An image `VOLUME` that no mount covers becomes an anonymous volume that the GC removes
  ([APG1](APG1-daily-docker-gc.md)).

## Consequences

- An image pull cannot fill `/` or the state unit. A unit that does not mount stops the stack.
- All state is in one tree on one unit: easy to size and migrate.
- The drop-in replaces the `ExecStart=` line of `containerd.service`, so a later change of that line
  does not reach the host. After a containerd major update, compare the unit with the drop-in.
- Ansible, not the Docker copy-up, owns the ownership of each state folder. A new stateful service
  needs a `stack_runtime_paths` entry.
- Docker does not seed a bind mount from the image. A changed file bind mount needs a recreate.

## Evidence

- The containerd store is the default for fresh installs from Docker Engine 29
  ([release notes](https://docs.docker.com/engine/release-notes/29/)). Its storage is separate from
  the Docker data directory and is not moved with it
  ([containerd image store](https://docs.docker.com/engine/storage/containerd/)).
- systemd `RequiresMountsFor=`:
  [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#RequiresMountsFor=).
- Volumes and bind mounts: [Docker storage](https://docs.docker.com/engine/storage/).
- A conffile prompt holds a package back in `unattended-upgrades` unless `DPkg::Options` holds
  `--force-confold` or `--force-confnew` (its `dpkg_conffile_prompt()` check).

## Alternatives rejected

- **One storage unit.** Image churn and the database share the free space.
- **The graph-driver store.** It is deprecated, so each image must migrate later.
- **Named volumes for state.** On the churn unit, and deleted by `down -v`.
- **The churn on the state unit.** Image churn is then next to the database again.
- **`nofail` mounts without `RequiresMountsFor=`.** The stack starts on an empty `docker_dir`.
- **The containerd root in `/etc/containerd/config.toml`** (S3XT). The changed conffile can hold
  `containerd.io` back.
- **`--force-confold` for each unattended upgrade.** It covers each package, but it also keeps a
  changed conffile when Debian changes the shipped copy for a reason, with no notice.

## Not repeated

- Do not assume that `data-root` moves the images. With the containerd store, it does not.
- Do not start `containerd` or `dockerd` before their storage mounts.
- Do not use a named volume for state.
- Do not set the containerd root in `/etc/containerd/config.toml`.

_Edited 2026-10-29 (ADR-NXK2): re-ID from cvm2._

_Edited 2026-10-29 (ADR-NXK2): citation repair._
