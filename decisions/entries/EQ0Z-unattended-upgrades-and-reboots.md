# EQ0Z — Unattended upgrades match Debian's security suite; reboots are automatic and opt-in

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user).

This entry restates the generic rules of site 0020 and site 0029. A site entry restates their site
values and supersedes them.

## Decision

1. **Origins.** The `apt_unattended_upgrades` role renders this pattern:

   ```
   Unattended-Upgrade::Origins-Pattern {
           "origin=Debian,codename=${distro_codename},label=Debian";
           "origin=Debian,codename=${distro_codename},label=Debian-Security";
           "origin=Debian,codename=${distro_codename}-security,label=Debian-Security";
           "origin=Docker,label=Docker CE";
   {% if updates_full %}
           "origin=Debian,codename=${distro_codename}-updates";
   {% endif %}
   };
   ```

2. **Both security lines stay**, as Debian ships them. Before you trust the Docker line on a new
   target, check the `Origin` and `Label` fields of the Docker `Release` file.
3. **One origin switch.** `updates_full` is the only switch. There is no `updates_security_only`.
4. **Upgrade time.** When `updates_upgrade_time` is set (`HH:MM`), a drop-in for
   `apt-daily-upgrade.timer` sets `OnCalendar=` to that time with `RandomizedDelaySec=0`. The default
   is empty: the drop-in is removed, and the Debian timer does not change.
5. **Reboot.** The role default is `updates_automatic_reboot: false`. Each host opts in. With the
   switch on, the role renders `Automatic-Reboot "true"`, `Automatic-Reboot-Time` from
   `updates_reboot_time` and `Automatic-Reboot-WithUsers "true"`. The reboot occurs only when
   `/var/run/reboot-required` exists.
6. **`live-restore` is off** in `daemon.json`. On a shutdown, `dockerd` stops each container with
   SIGTERM, and the Compose `stop_grace_period` applies. A database service must have a
   `stop_grace_period` that is long enough for a clean shutdown.
7. **One maintenance window.** On each host, the Docker GC, the image updates, the upgrade and the
   reboot run at different times, in this order. The upgrade time is before the reboot time. The
   site records the times of each host.
8. **Report.** With system mail on, `unattended-upgrades` reports `on-change`
   ([GEE3](GEE3-system-mail-through-msmtp.md)). Without it, the role writes no `Mail` lines.
9. **Verify.** The verify play asserts that `unattended-upgrades --dry-run --debug` lists
   `<codename>-security` in the allowed origins, that both `Automatic-Reboot` settings are present
   where the host opts in, and that `/var/run/reboot-required` is absent after the window.

## Reason

- Since Debian 11, the security suite is `<codename>-security`. A pattern with only
  `codename=${distro_codename},label=Debian-Security` matches no security pocket, so no security
  update is installed. Debian's shipped `50unattended-upgrades` has both lines.
- The `docker-ce` maintainer scripts restart `docker.service`. With `live-restore` off, that stops
  and starts each container. The Docker origin makes the engine update automatic, so its time must
  be in the window.
- Debian's `apt-daily-upgrade.timer` runs at 06:00 with `RandomizedDelaySec=60m`. Without the drop-in,
  a kernel installed after the reboot time waits almost a day for its reboot, and the Docker restart
  occurs at a random time.
- A `tmux` or SSH session counts as a logged-in user. Without `WithUsers`, one lingering session
  stops each security reboot, with no warning.
- With `live-restore` on, `dockerd` does not stop the containers on a host shutdown. The database is
  then killed during a write.
- A manual reboot needs a person who sees `/var/run/reboot-required`. Kernel fixes can then wait with
  no limit.

## Consequences

- On an update day, the host is down for a few minutes at the reboot time, with a database restart.
- A reboot can stop a long background job.
- A Docker engine update or a `daemon.json` change stops each container for a short time.
- Point-release updates (`label=Debian`) are automatic.
- An upgrade that runs past the reboot time moves the reboot to the next day.
- `apt-daily.timer` (twice a day, not changed) refreshes the package lists, so the upgrade can use
  lists that are several hours old.

## Evidence

- Debian `unattended-upgrades`, shipped config `data/50unattended-upgrades.Debian`; Debian 11 release
  notes, "Changed security archive layout"; `apt` package,
  `/lib/systemd/system/apt-daily-upgrade.timer`.

## Alternatives rejected

- **Only the old security line.** It matches no security pocket on Debian 11 or later.
- **`site=` or `suite=` patterns.** They differ from Debian's shipped file for no gain.
- **The Debian default timer.** Docker restarts and kernel installs occur outside the window.
- **Pin `docker-ce` and upgrade it by hand.** The engine is the largest surface that would stay
  unpatched.
- **Manual reboot, or a monthly reboot.** A fix can wait for weeks.

## Not repeated

- Do not remove the `${distro_codename}-security` line. It is the line that matches.
- Do not turn on `live-restore`.

_Edited 2026-10-29 (ADR-NXK2): re-ID from eq0z._

_Edited 2026-10-29 (ADR-NXK2): citation repair._
