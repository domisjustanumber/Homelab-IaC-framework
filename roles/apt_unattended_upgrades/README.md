# apt_unattended_upgrades

This role configures `unattended-upgrades`: the origins, the reboot policy and the report mail.
It can also move `apt-daily-upgrade.timer`.
The rules are in [eq0z](../../notes/decisions/eq0z-unattended-upgrades-and-reboots.md) and
[gee3](../../notes/decisions/gee3-system-mail-through-msmtp.md).

## Inventory values

The role has no required value.
It reads these values from the inventory of the site only when `system_mail_enabled` is true:

| Value | Use |
|---|---|
| `system_mail_enabled` | Feature switch. When it is not true, the role writes no `Mail` lines. |
| `system_mail_admin` | The recipient of the report (`Mail`) |
| `system_mail_report` | `MailReport`. When it is not set, the role uses `on-change`. |
| `system_mail_from` | The mailbox in `Sender` |
| `hostname` | The name in `Sender` |

## Role defaults

The inventory of the site can override each default.

| Variable | Default | Use |
|---|---|---|
| `updates_full` | `false` | Opt-in. Also install from `<codename>-updates`. |
| `updates_automatic_reboot` | `false` | Opt-in. Set `Automatic-Reboot`. |
| `updates_reboot_time` | `"03:30"` | `Automatic-Reboot-Time` |
| `updates_upgrade_time` | `""` | `HH:MM` installs the timer drop-in. `""` removes it. |
| `updates_autoremove` | `false` (the Debian default) | `Remove-Unused-Dependencies` |
| `updates_remove_kernels` | `true` | `Remove-Unused-Kernel-Packages` |
| `updates_mail` | `system_mail_admin`, or `""` | `Mail`. `""` writes no `Mail` lines. |
| `updates_mail_report` | `system_mail_report` | `MailReport` |
| `updates_mail_sender` | `<hostname> Unattended-Updates <system_mail_from>` | `Sender` |

## Handlers

- `Reload systemd for apt timer`
