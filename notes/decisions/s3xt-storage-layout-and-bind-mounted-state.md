# s3xt — Three VM disks for a Docker host; all persistent state is bind-mounted

**Status:** proposed, 2026-10-25 (agent).

This entry restates the generic rules of site 0034. A site entry restates its site values (the disk
sizes and the mounts of each container) and supersedes site 0034.

## Decision

1. **Three disks.** Each Docker host VM has three virtual disks:
   - `/`: the OS, the packages, journald and a swapfile;
   - the Docker data-root (`/var/lib/docker`): images, container layers and container logs;
   - `docker_dir` (for example `/docker`): all persistent container state.

   Each disk is ext4 and is mounted by UUID. `discard=on` is set on the hypervisor, and
   `fstrim.timer` runs in the guest. There is no LVM in the guest. Each disk grows alone, with
   `qm resize`, `growpart` and `resize2fs`. The site records the size of each disk.
2. **All disks in the backup.** All three disks stay in the backup job of the VM.
3. **Mounts are enforced.** The inventory lists the mounts in `docker_storage_mounts`. The preflight
   of each playbook refuses to run while one of them is not mounted. The `docker_engine` role adds a
   `docker.service` drop-in with `RequiresMountsFor=` for the data-root, `docker_dir` and those
   mounts, so `dockerd` never starts without its storage. A path that is not its own mount requires
   only `/`, so the drop-in is safe on a host with one disk.
4. **No named volumes for state.** Each persistent path of a container is a bind mount under
   `${STACK_DIR}/appdata/` or `${STACK_DIR}/logs/`. Ansible creates it from `stack_runtime_paths`,
   with the owner and mode that the container needs. The Docker data-root holds only data that can be
   rebuilt.

## Reason

- The three kinds of data grow in different ways. The OS grows slowly. Images grow in spikes,
  because moving tags and the GC retention keep superseded images on disk. State grows steadily and
  cannot be recovered without the backup. On one filesystem, an image pull that fills the disk also
  stops the database writes.
- A mount that fails at boot is worse. `dockerd` starts, writes into the empty mount point on `/`,
  the database creates a fresh datadir, and the web application shows its installer on its public
  hostname.
- A restore without the data-root pulls newer images for each moving tag, and so bypasses the update
  cooldown.
- A bind mount is at a host path that the stack chooses. Ansible sets its owner and mode. It survives
  `docker compose down -v`, `docker volume prune -a` and a renamed project, and host scripts reach it
  by its path.
- A named volume is on the data-root disk, `down -v` deletes it, and its name contains the project
  name.

## Consequences

- An image pull cannot fill `/` or the state disk.
- A disk that does not mount stops the stack. The stack cannot start empty.
- All state is in one tree on one disk: easy to size, inspect, restore-drill and migrate.
- No data depends on the Compose project name or on `docker volume` commands.
- Three disks to size and grow, not one.
- Ansible, not the Docker copy-up, owns the ownership of each state folder. A new stateful service
  needs a `stack_runtime_paths` entry.
- Docker does not seed a bind mount from the image. A file bind mount keeps the old inode when the
  file is replaced, so a change of the file needs a recreate of the container.
- The backup holds images that can be rebuilt. This costs backup space.

## Evidence

- systemd `RequiresMountsFor=`:
  [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#RequiresMountsFor=).
- Volumes and bind mounts: [Docker storage](https://docs.docker.com/engine/storage/).

## Alternatives rejected

- **One disk.** Image churn and the database share the free space, and nothing protects against a
  missing mount.
- **One disk with LVM volumes.** The same isolation, but a resize needs LVM in the guest. Separate
  virtual disks are simpler.
- **Named volumes for state.** On the churn disk, deleted by `down -v`, tied to the project name and
  hidden from host scripts.
- **The Docker data-root on the state disk.** Image churn is then next to the database again.
- **No data-root in the backup.** A restore pulls newer images and bypasses the cooldown.
- **`nofail` mounts without `RequiresMountsFor=`.** The host boots and starts the stack on an empty
  `docker_dir`.

## Not repeated

- Do not start `dockerd` before its storage mounts. Keep the `RequiresMountsFor=` drop-in.
- Do not use a named volume for state.
