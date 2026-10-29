# S3XT — Docker hosts keep state apart from image churn, behind enforced mounts

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user); superseded by [CVM2](CVM2-storage-layout-containerd-root-by-flag.md), 2026-10-29 (user).

This entry restates the generic rules of site 0034 for each Docker host. A VM host also follows
[MSAM](MSAM-docker-host-vm-disks.md). A site entry restates the site values of site 0034 and
supersedes it.

## Decision

1. **Scope.** These rules apply to each Docker host, VM or LXC. They do not apply to Proxmox VE
   nodes, appliances or guests without Docker.
2. **Two storage units.** A state unit is mounted at `docker_dir` (for example `/docker`). A churn
   unit holds the containerd root and the Docker data-root: images, snapshots, container layers and
   container logs. The host type decides what a unit is: a disk for a VM ([MSAM](MSAM-docker-host-vm-disks.md)),
   a mount point for an LXC (a later entry).
3. **Image store.** The hosts use the default containerd image store of Docker Engine. The
   `docker_engine` role sets the containerd `root` (`/etc/containerd/config.toml`) and the Docker
   `data-root` (`daemon.json`) to folders on the churn unit. The paths are role defaults. The
   containerd root is a folder that `dockerd` does not use.
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

- The three kinds of data grow in different ways. The OS grows slowly. Images grow in spikes,
  because moving tags and the GC retention keep superseded images on disk. State grows steadily and
  cannot be recovered without the backup. On one filesystem, an image pull that fills the disk also
  stops the database writes.
- A mount that fails at boot is worse. The daemons start, write into the empty mount point on `/`,
  the database creates a fresh datadir, and the web application shows its installer on its public
  hostname.
- With the containerd image store, `data-root` does not move the images. containerd keeps them in
  its own root, by default on `/`. Docker's docs say to configure it separately, to avoid a full root
  partition. A drop-in on `docker.service` alone does not stop `containerd.service`.
- A bind mount is at a host path that the stack chooses. Ansible sets its owner and mode. It survives
  `docker compose down -v`, `docker volume prune -a` and a renamed project, and host scripts reach it
  by its path. A named volume is on the churn unit, `down -v` deletes it, and its name contains the
  project name.
- An image `VOLUME` that no mount covers becomes an anonymous volume on the churn unit. A recreate
  leaves it behind, and the GC removes it ([APG1](APG1-daily-docker-gc.md)).
- The graph-driver store is deprecated. A host that starts on it must migrate each image later.

## Consequences

- An image pull cannot fill `/` or the state unit.
- A unit that does not mount stops the stack. The stack cannot start empty.
- All state is in one tree on one unit: easy to size, inspect, restore-drill and migrate.
- The role owns `/etc/containerd/config.toml`. The settings that the `containerd.io` package ships
  must stay. Check the file on the first host.
- Ansible, not the Docker copy-up, owns the ownership of each state folder. A new stateful service
  needs a `stack_runtime_paths` entry.
- Docker does not seed a bind mount from the image. A file bind mount keeps the old inode when the
  file is replaced, so a change of the file needs a recreate of the container.

## Evidence

- The containerd store is the default for fresh installs from Docker Engine 29
  ([release notes](https://docs.docker.com/engine/release-notes/29/)). Its storage is separate from
  the Docker data directory and is not moved with it
  ([containerd image store](https://docs.docker.com/engine/storage/containerd/)).
- systemd `RequiresMountsFor=`:
  [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#RequiresMountsFor=).
- Volumes and bind mounts: [Docker storage](https://docs.docker.com/engine/storage/).

## Alternatives rejected

- **One storage unit.** Image churn and the database share the free space, and nothing protects
  against a missing mount.
- **The graph-driver store** (`containerd-snapshotter: false`). Deprecated, so a later migration of
  each image.
- **Named volumes for state.** On the churn unit, deleted by `down -v`, tied to the project name and
  hidden from host scripts.
- **The churn on the state unit.** Image churn is then next to the database again.
- **`nofail` mounts without `RequiresMountsFor=`.** The host boots and starts the stack on an empty
  `docker_dir`.

## Not repeated

- Do not assume that `data-root` moves the images. With the containerd store, it does not.
- Do not start `containerd` or `dockerd` before their storage mounts.
- Do not use a named volume for state.

_Edited 2026-10-29 (ADR-NXK2): re-ID from s3xt._

_Edited 2026-10-29 (ADR-NXK2): citation repair._
