# APG1 — Daily Docker GC with anonymous-only volume pruning

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user).

This entry restates the generic rules of site 0010. A site entry restates its site values (the time
and the retention) and supersedes site 0010.

## Decision

The `docker_gc` role installs a systemd oneshot service and a daily timer:

```ini
[Service]
Type=oneshot
ExecStart=/usr/bin/docker system prune -af --filter until=<docker_gc_image_retention>
ExecStart=/usr/bin/docker volume prune -f
Nice=10
IOSchedulingClass=idle
```

1. **Anonymous volumes only.** Volume pruning removes only anonymous volumes that no container uses.
   Automation never prunes a named volume: never `docker volume prune -a` or `-af`.
2. **Two `ExecStart=` lines.** systemd does not use a shell, so `&&` would be an argument to
   `docker`. In a oneshot unit, the lines run in order, and a failure skips the rest.
3. **Host values.** `docker_gc_time` (`HH:MM`) and `docker_gc_image_retention` (the `until=` value)
   come from the inventory. The time fits the maintenance window of the host
   ([EQ0Z](EQ0Z-unattended-upgrades-and-reboots.md)).
4. **Missed runs.** The timer has `Persistent=true`, so a run that the host missed starts at the
   next boot.
5. **Failure mail.** With system mail on, the service has `OnFailure=status-email@%n.service`
   ([GEE3](GEE3-system-mail-through-msmtp.md)).
6. **Manual reaping.** To remove the named volumes of an old project, run
   `docker volume prune -af --filter "label=com.docker.compose.project=<old>"` by hand, for that
   project only.
7. **The retention is not a rollback promise.** What `until=` measures depends on the image store
   (Consequences). Do not plan a rollback on an image that the GC can remove.

## Reason

- `docker system prune --filter until=` applies to stopped containers, unused networks, unused
  images and the build cache. `prune -a` never removes an image that a container uses.
- `docker volume prune` has no `until=` filter. Without `-a`, it removes only anonymous volumes that
  no container uses. With `-a`, named volumes are eligible too, so a stack that is stopped at the
  time of the run loses its named volumes. A `dangling=true` filter has the same effect.
- A systemd unit is observable (`systemctl list-timers`, `journalctl -u docker-gc`), it reports a
  failure by its exit status, and systemd is already on each host. No container gets access to the
  Docker API for the GC.

## Consequences

- Image and build-cache growth has a limit, and no named volume or bind-mounted state is at risk.
- Abandoned named volumes stay until a person removes them.
- **Image age.** The hosts use the containerd image store, the default of a fresh Docker Engine 29
  install ([S3XT](S3XT-storage-layout-and-bind-mounted-state.md)). There, `until=` compares the time
  of the local image record. When a pull replaces a tag, the old image becomes a dangling record
  with the time of that pull. An image that Watchtower replaced therefore stays for about the
  retention, plus up to one day. With the older graph-driver store, `until=` compares the build
  time, and a superseded image normally goes at the next run.
- A stack that is stopped at the time of a run loses its containers that were created before the
  retention, their anonymous volumes and then its unused images. Its bind-mounted state stays.

## Evidence

- `docker system prune` and `docker volume prune`:
  [system prune](https://docs.docker.com/reference/cli/docker/system/prune/),
  [volume prune](https://docs.docker.com/reference/cli/docker/volume/prune/).
- The containerd store is the default for fresh installs from Docker Engine 29
  ([release notes](https://docs.docker.com/engine/release-notes/29/)).
- On the containerd store, the `until` filter compares the `CreatedAt` of the containerd image
  record ([moby `daemon/containerd/image_list.go`](https://github.com/moby/moby/blob/b711d21792db6db488de976eb3c4a653c92c3bc3/daemon/containerd/image_list.go)).
  A pull that replaces a tag keeps the old image as a dangling record
  ([`image_pull.go`](https://github.com/moby/moby/blob/b711d21792db6db488de976eb3c4a653c92c3bc3/daemon/containerd/image_pull.go#L129-L137)).
- The CLI passes the same filter to the build-cache prune
  ([docker/cli `prune.go`](https://github.com/docker/cli/blob/6d274590f2f63276a54da8adf475a455d21c1fdd/cli/command/system/prune.go#L98-L107)).
- Research of 2026-10-25 on the `clockworksoul/docker-gc-cron` image: its wrapped script
  (`spotify/docker-gc`) is archived, the last published image ships Docker client 1.12, and its
  volume clean-up removes each dangling volume, named volumes included.

## Alternatives rejected

- **`docker volume prune -af` each night.** It deletes the named volumes of stopped stacks, and no
  age filter exists.
- **`-af` with a protection label.** Each volume must opt in, or its data is at risk.
- **A GC container (`clockworksoul/docker-gc-cron`).** Not maintained, it needs delete rights on the
  Docker API, it hides its errors, and its volume clean-up removes named volumes.
- **A script that keeps the last N images of each repository.** The CLI cannot express it. Pinned
  tags can be pulled again, so the window has little value.
- **No pruning.** The disk of a small VM fills.

## Not repeated

- Do not add `-a` to the volume prune, and do not prune volumes with `dangling=true`.
- Do not join the two commands with `&&` in one `ExecStart=`.
- Do not count on the retention as a rollback window. It depends on the image store.

_Edited 2026-10-29 (ADR-NXK2): re-ID from apg1._

_Edited 2026-10-29 (ADR-NXK2): citation repair._
