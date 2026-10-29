# system_mail

This role installs msmtp as a null client.
msmtp gives `/usr/sbin/sendmail`, and it relays all mail to an SMTP relay.
The role writes `/etc/msmtprc` and `/etc/aliases`.
It also installs `status-email@.service` for `OnFailure=`.
The role purges other mail transport agents first.
See [GEE3](../../decisions/GEE3-system-mail-through-msmtp.md).

The secrets role of [0004](../../decisions/0004-secrets-split-by-domain.md) (proposed) renders
the SMTP password file `/etc/msmtp-password`. This repository does not hold that role yet. Until it
does, the site must render the file before this role runs.
`/etc/msmtprc` holds no password.

The playbook applies this role only when `system_mail_enabled` is on
([NTK9](../../decisions/NTK9-generic-roles-and-host-values.md)).

## Inventory values

All values are required.
The role fails at the start when a value is not set or is a placeholder.

| Variable | Use |
|---|---|
| `system_mail_smarthost` | The hostname of the SMTP relay |
| `system_mail_port` | The port of the relay: 587 for STARTTLS, 465 for implicit TLS |
| `system_mail_tls_starttls` | `true` for STARTTLS, `false` for implicit TLS |
| `system_mail_user` | The SMTP user name |
| `system_mail_from` | The envelope sender. It must be a valid mailbox. |
| `system_mail_admin` | The recipient of the mail to `root` and `default` |

The `apt_unattended_upgrades` role also reads `system_mail_admin`, `system_mail_from` and
`system_mail_report`.
This role does not read `system_mail_report`.

## Role defaults

- `system_mail_conflicting_packages`: the mail transport agents that the role purges.
- `system_mail_packages`: `msmtp` and `msmtp-mta`.

## Handlers

- `Reload systemd for status-email`
