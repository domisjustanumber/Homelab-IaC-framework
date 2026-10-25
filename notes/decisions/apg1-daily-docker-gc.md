# apg1 — Daily Docker GC with anonymous-only volume pruning

**Status:** proposed, 2026-10-25 (agent).

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
   ([eq0z](eq0z-unattended-upgrades-and-reboots.md)).
4. **Missed runs.** The timer has `Persistent=true`, so a run that the host missed starts at the
   next boot.
5. **Failure mail.** With system mail on, the service has `OnFailure=status-email@%n.service`
   ([gee3](gee3-system-mail-through-msmtp.md)).
6. **Manual reaping.** To remove the named volumes of an old project, run
   `docker volume prune -af --filter "label=com.docker.compose.project=<old>"` by hand, for that
   project only.

## Reason

- `docker system prune --filter until=` applies to containers, images and networks. Build cache is
  always eligible.
- `docker volume prune` has no `until=` filter. Without `-a`, it removes only anonymous volumes that
  no container uses. With `-a`, named volumes are eligible too, so a stack that is stopped at the
  time of the run loses its named volumes.
- A systemd unit is observable (`systemctl list-timers`, `journalctl -u docker-gc`), and systemd is
  already on each host.

## Consequences

- Image and build-cache growth has a limit, and no application data is at risk.
- Abandoned named volumes stay until a person removes them.
- `until=` compares the creation time of an image, which is its build time, not the time of its
  pull or its last use. A superseded image is normally older than the retention, so it goes at the
  next run. The retention is not a rollback window.
- A stopped stack loses its images at the next run.

## Evidence

- `docker system prune` and `docker volume prune` filter behaviour:
  [system prune](https://docs.docker.com/reference/cli/docker/system/prune/),
  [volume prune](https://docs.docker.com/reference/cli/docker/volume/prune/).

## Alternatives rejected

- **`docker volume prune -af` each night.** It deletes the named volumes of stopped stacks, and no
  age filter exists.
- **`-af` with a protection label.** Each volume must opt in, or its data is at risk.
- **A GC container (`clockworksoul/docker-gc-cron`).** One more container and one more updater.
- **No pruning.** The disk of a small VM fills.

## Not repeated

- Do not add `-a` to the volume prune.
- Do not join the two commands with `&&` in one `ExecStart=`.
- Do not count on `until=` to keep a superseded image for a rollback.
