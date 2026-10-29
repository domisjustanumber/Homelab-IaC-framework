# base

This role configures each Debian 13 host. It has no feature switch.
It installs the base packages and the QEMU guest agent.
It configures the admin user, sshd, chrony, the journald size limit and the hardening sysctls.

Decisions: [BQXN](../../decisions/BQXN-debian-hosts-and-the-base-role.md) (the role),
[NTK9](../../decisions/NTK9-generic-roles-and-host-values.md) (values) and
[XQ9A](../../decisions/XQ9A-guest-backups-by-the-hypervisor.md) (the guest agent).

## Inventory values

All are required. The role stops when a value is not defined, or when it is `CHANGEME` or `CONFIRM`.

| Value | Use |
|---|---|
| `hostname` | The hostname of the host |
| `timezone` | The IANA time zone |
| `admin_user` | The admin user. It gets passwordless sudo. |
| `admin_ssh_key_op_item` | The 1Password item that holds the public key of the admin user |
| `op_vault` | The 1Password vault of that item |

## Role defaults

`base_packages`, `base_apt_cache_valid_time`, `base_journald_system_max_use`,
`base_ssh_dropin_dir`, `base_sshd_binary`, `base_admin_shell`, `base_admin_groups`,
`base_admin_ssh_key_op_field`, `base_sysctl_file`, `base_sysctls`.

## Handlers

`Reload sshd`, `Restart journald`.

## Notes

- The role is for a VM. The QEMU guest agent lets the hypervisor freeze the filesystems for a
  backup. The agent must also be on in the VM options.
- In `--check`, the role does not install the admin key. A 1Password lookup runs on the controller
  also in `--check`, so the task is skipped.
- The role does not set `net.ipv4.ip_forward`. Docker manages it.
- The role configures no firewall.
- The sshd drop-in is `00-hardening.conf`. sshd keeps the first value that it reads, so this
  drop-in wins over a later drop-in. `sshd -t` validates it before it is installed.
