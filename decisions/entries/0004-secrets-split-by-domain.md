# 0004 — Secrets: two vaults by consumer, one token for each run; hosts never run `op`

**Status:** proposed, 2026-10-25 (agent); recorded again 2026-11-17 (user: two vaults by consumer,
a token for each run, a lookup only when a file is missing).

## Decision

**Source and accounts**

1. **One source.** 1Password is the only place where a secret is authored.
2. **Two vaults, by consumer.** The controller vault holds the items that only the controller uses:
   its own keys and the credentials that manage machines (Proxmox VE, Cloudflare management, the
   Proxmox Backup Server, the OpenTofu state key). The hosts vault holds each secret that a host or
   a stack receives. A further split needs a new entry.
3. **One service account per vault.** Each service account can read only its own vault. Write access
   for an account needs its own decision.
4. **One token for each run.** Only the controller holds the tokens, each as a file that only root
   can read. The user that runs Ansible and OpenTofu cannot read them. A root-owned launcher, allowed
   by one `sudo` rule, starts each run with only the token of the vault that the run needs. Each
   lookup names its vault and passes that token as `service_account_token`. The host needs no `op`
   CLI and no session, and it holds no credential that can fetch more secrets.
5. **Public keys.** A public key that a host receives is an item in the hosts vault with the public
   key only. A private key is never in the hosts vault.

**Delivery**

6. **Render on the controller.** Ansible reads each value with the `community.general.onepassword`
   lookup and writes it as a file on the host. The site does not run 1Password Connect or another
   runtime secret service on the host.
7. **Files.** Each stack secret goes to `<stack_dir>/secrets/<name>`. Containers consume it as a
   Docker secret. Use a `*_FILE` environment variable where the image supports one.
8. **The `.env` exception.** An image without `*_FILE` support takes the secret from `.env` (`0600`)
   through an `env_secrets` entry. The site documents each one.
9. **Names only in git.** The inventory holds names only (`op_vault`, `op_items`, `op_secrets`,
   `env_secrets`), never values. No Ansible Vault.
10. **Look up only when needed.** A render task looks up a value only when its file is missing on the
    host or `op_secrets_force` is true. A run that finds each file reads no secret. When `.env` must
    change, the task looks up its `env_secrets` values again.
11. **Render tasks.** Each render task uses `no_log: true`, `diff: false`, `loop_control.label` and
    `| trim`. Secret tasks are skipped in `--check`.
12. **Attributes.** The default is `root:root 0400`. A consumer that runs as a configurable non-root
    user gets `owner` and `group` set to that user, mode `0400`. A consumer whose image fixes its
    user gets `group` set to that GID, mode `0440`, owner root. A secret file is never
    world-readable. Each `op_secrets` entry holds its values, with a comment that names the user.
13. **Enforce on each run.** An `ansible.builtin.file` task after each render sets owner, group and
    mode on each run. It does no 1Password lookup and notifies nothing.
14. **Rotation.** Change the field in 1Password, then run the play with `-e op_secrets_force=true`.
    The handler recreates the containers. A credential that a service registers (for example a
    CrowdSec bouncer key) is deregistered before the recreate.

## Reason

- The user decided (2026-10-24) the split and that the host never runs `op`, and (2026-11-17) two
  vaults by consumer. A leaked token then reads one vault, and a host or stack run never holds the
  token that manages machines.
- A split protects only when each run holds only its token. If one user can read each token file,
  each playbook can read each vault.
- 1Password scopes a service account by vault, not by item. A Families plan allows 1,000 reads a
  day for all accounts. A lookup only for a missing file keeps a routine deploy at zero reads.
- A runtime secret service keeps a live token on the host, and it gives no live rotation.
- Outside Swarm, a Compose file secret keeps the owner and mode of the host file. Compose ignores
  `uid`, `gid` and `mode` on it.
- `ansible.builtin.copy` with `force: false` does not touch an existing file. Without rule 13, a
  change of attributes has no effect after the first deploy.

## Consequences

- A value that changes in 1Password reaches a host only on a force run.
- Vault access of a service account is fixed when it is created. A further split needs new accounts.
- A host cannot refresh its own secrets. A rotation needs a controller run.
- A group-readable secret file is readable by each process on the host with that GID.
- HashiCorp Vault stays out. Check its revisit triggers again when hosts migrate to the
  controller, or when an SSH certificate authority is chosen.

## Evidence

- The lookup takes `service_account_token` (community.general 7.1.0 and later):
  <https://docs.ansible.com/ansible/latest/collections/community/general/onepassword_lookup.html>.
- Vault scope, immutable access and rate limits:
  <https://www.1password.dev/service-accounts/get-started/>,
  <https://www.1password.dev/service-accounts/rate-limits/>.

## Alternatives rejected

- **One vault and one service account.** A leak of the one token exposes all secrets.
- **Three vaults by domain, or a vault per host or stack.** The user chose two vaults (2026-11-17).
- **One user that reads each token file.** The split then stops only a leak.
- **`op` on each host, 1Password Connect, HashiCorp Vault, Ansible Vault or SOPS.** A live token or a
  second store of each secret.
- **World-readable secret files (`0444`).** Each host user can then read the secret.

## Not repeated

- Do not assume that a Compose secret is readable by the container user.
- Do not rely on `copy` with `force: false` to set attributes on an existing file.
- Do not pass a secret on a command line or print it.
