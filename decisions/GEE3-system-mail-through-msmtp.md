# GEE3 — System mail goes through an SMTP relay with msmtp

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user).

Supersedes site 0025 in full. This entry restates each rule of site 0025. Site 0025 holds no site
values.

## Decision

The `system_mail` role installs msmtp as a null client. It relays all mail through an external SMTP
submission service. The packages are `msmtp` and `msmtp-mta`.

1. **No listening daemon.** Nothing binds port 25. There is no local mailbox and no local delivery.
2. **One recipient.** `/etc/aliases` maps `root:` and `default:` to `system_mail_admin`. msmtp reads
   the aliases file itself. There is no `newaliases` step.
3. **No password in the config.** `/etc/msmtprc` is `0644` and holds
   `passwordeval cat /etc/msmtp-password`. The password file is `0400 root`. The secrets role renders
   it from 1Password on the controller ([0004](0004-secrets-split-by-domain.md)), before this role
   runs.
4. **TLS with the system CA bundle.** `tls_trust_file /etc/ssl/certs/ca-certificates.crt`. STARTTLS
   on port 587, implicit TLS on port 465 (`system_mail_tls_starttls`).
5. **Failure is reported, success is silent.** A unit that must report a failure has
   `OnFailure=status-email@%n.service`. `unattended-upgrades` reports `on-change`.
6. **A real `From`.** msmtp sets an envelope `from` (`system_mail_from`). `Unattended-Upgrade::Sender`
   is `<hostname> Unattended-Updates <system_mail_from>`. The value becomes the `From` header
   without a change, so it must be a valid mailbox.
7. **Other MTAs are purged.** `msmtp-mta` conflicts with `mail-transport-agent`. The role removes
   `postfix`, `exim4-daemon-light`, `exim4-daemon-heavy`, `dma`, `nullmailer` and `ssmtp` first.
8. **No `mailx`.** No `mailx` package, no `/etc/mail.rc` and no `/etc/mailname`.

## Reason

- `unattended-upgrades`, `cron`, `systemd` `OnFailure=`, `logrotate`, `apt-listchanges`, `smartd`
  and `mdadm` send mail through `/usr/sbin/sendmail`. Without an MTA, their output goes nowhere, and
  `unattended-upgrades` fails with no warning.
- A host has outbound HTTPS, no mail domain and no static public IP. It must not listen on port 25.
- `unattended-upgrades` uses `/usr/sbin/sendmail` when it exists, and only then falls back to
  `/usr/bin/mail`. `apt-listchanges` uses `mail` only when `/usr/sbin/sendmail` exists. `msmtp-mta`
  provides `/usr/sbin/sendmail`, so `mailx` is not necessary.
- `/etc/mailname` is read only for `%M` substitutions and for generated `Message-ID` values.
- The default sender `root` gives `From: root`. Many relays reject it.
- The password follows the same 1Password-to-file path as each other secret. There is no second
  secret store and no second rotation procedure.

## Consequences

- Delivery needs the external provider. When it cannot be reached, msmtp exits non-zero and the
  message is lost. msmtp has no spool. This is acceptable for failure notices, not for mail that
  must not be lost.
- Provider quotas and rate limits apply. A unit that fails again and again can use them up.
- A provider filter can drop a message that looks like a bounce.
- The purge of other MTAs breaks local mail delivery on a host that used it. Check this on each new
  host.
- Send a test mail in the verify play. A mail configuration that never sent a message is not tested.

## Evidence

- `unattended-upgrades` functions `_send_mail_using_sendmail` and `_send_mail_using_mailx`: the
  script checks `/usr/sbin/sendmail` first.
- The `Sender` value is set on `msg['From']` without a change.

## Alternatives rejected

- **`postfix` in satellite mode.** A listening daemon and a queue to configure, for outbound mail of
  one host.
- **`dma`.** One package, but it queues on disk, needs `dma.conf`, `auth.conf` and `MASQUERADE`, has
  no implicit TLS on port 465 and has coarser TLS trust settings.
- **`bsd-mailx` with msmtp.** Not necessary, because `msmtp-mta` provides `/usr/sbin/sendmail`.
- **`nullmailer`.** Its config is in several files, and it runs a daemon.
- **No MTA, with `curl` notices from systemd.** `cron` and `unattended-upgrades` then have no
  `sendmail`, and their output is lost.
- **Inbound routing only, for example Cloudflare Email Routing.** Outbound mail still needs an
  authenticated submission endpoint.

## Not repeated

- Do not put the SMTP password in `/etc/msmtprc`.
- Do not leave `Unattended-Upgrade::Sender` at its default.

_Edited 2026-10-29 (ADR-NXK2): re-ID from gee3._
