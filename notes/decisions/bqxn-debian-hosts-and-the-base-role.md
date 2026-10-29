# bqxn — Managed hosts run Debian 13; the `base` role

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user).

This entry restates the generic rules of site 0018. A site entry restates its site values and
supersedes site 0018.

## Decision

1. **Base OS.** Each host that the roles manage runs Debian 13 ("trixie"). The roles install no
   Ubuntu packages, services, apt origins or credentials. No Ubuntu Pro, no Livepatch, no ESM.
2. **Kernel fixes need a reboot.** `unattended-upgrades` installs kernel updates. They take effect
   at the next reboot. Each host must have a reboot policy
   ([eq0z](eq0z-unattended-upgrades-and-reboots.md)).
3. **apt sources.** apt sources use the Debian codename. The Docker repository is
   `https://download.docker.com/linux/debian`.
4. **The `base` role.** The role applies to each host. It has no feature switch. It installs the base
   packages and `qemu-guest-agent`, and it configures the admin user, sshd, chrony, the journald size
   limit and the hardening sysctls.
5. **sshd.** Key-only authentication, no root login and no password or keyboard-interactive login.
   The drop-in is `00-hardening.conf`, so it comes first and its values win. `sshd -t` validates it
   before it is installed.
6. **Admin key.** The public key of the admin user comes from a 1Password lookup. The key is not a
   secret, but the lookup is skipped in `--check`, as each 1Password lookup is
   ([0004](0004-secrets-split-by-domain.md)).
7. **Not in `base`.** The role does not set `net.ipv4.ip_forward`, because Docker manages it. The role
   configures no firewall. A firewall needs its own entry.

## Reason

- Livepatch covers only kernel vulnerabilities rated critical or high. It does not patch userspace
  libraries (glibc, OpenSSL, systemd), and Canonical states that it does not replace a reboot
  ([Livepatch FAQ](https://ubuntu.com/security/livepatch)). It adds a subscription, `snapd` and a
  credential on the host, and a reboot is still necessary.
- One base OS gives one update mechanism, with no subscription and no snap.
- Debian 13 has standard support to 2028 and LTS to 2030.
- A password or a root login over SSH is a common attack path. Each admin key is in 1Password, so a
  password login has no use.
- A first drop-in wins: sshd keeps the first value that it reads for each keyword.

## Consequences

- A kernel fix waits for the next reboot. The reboot policy manages that window, not a vendor
  service.
- Kernel and userspace fixes share one reboot cadence.
- A host that is not Debian 13 needs a new entry before the roles support it.

## Alternatives rejected

- **Ubuntu LTS with Livepatch.** A narrow benefit, a second OS-specific mechanism, and a reboot is
  still necessary.
- **Debian with kpatch or kGraft.** Self-managed, not supported by Debian security, and a continuous
  build effort.

## Not repeated

- Do not set `net.ipv4.ip_forward` in a hardening sysctl file. Docker needs it.
- Do not rename the sshd drop-in to a name that sorts after another drop-in.
