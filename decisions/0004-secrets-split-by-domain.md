# 0004 — Secrets: vaults and service accounts split by domain; hosts never run `op`

**Status:** proposed, 2026-10-25 (agent).

## Decision

**Source and accounts**

1. **One source.** 1Password is the only place where a secret is authored.
2. **Vaults by domain.** Secrets are split into three vaults: infrastructure credentials (Proxmox
   VE, Cloudflare), stack secrets, and the items of the controller itself.
3. **One service account per vault.** Each service account can read only its own vault. Write access
   for an account needs its own decision.
4. **Controller only.** Only the controller holds the service-account tokens. Each lookup names its
   vault and uses the token of that vault's account. The host needs no `op` CLI and no session, and
   it holds no credential that can fetch more secrets.

**Delivery**

5. **Render on the controller.** Ansible reads each value with the `community.general.onepassword`
   lookup and writes it as a file on the host. The site does not run 1Password Connect or another
   runtime secret service on the host.
6. **Files.** Each stack secret goes to `<stack_dir>/secrets/<name>`. Containers consume it as a
   Docker secret. Use a `*_FILE` environment variable where the image supports one.
7. **The `.env` exception.** An image without `*_FILE` support takes the secret from `.env` (`0600`)
   through an `env_secrets` entry. The site documents each one.
8. **Names only in git.** The inventory holds names only (`op_vault`, `op_items`, `op_secrets`,
   `env_secrets`), never values. No Ansible Vault.
9. **Render tasks.** Each render task uses `no_log: true`, `diff: false`, `loop_control.label`,
   `| trim` and `force: "{{ op_secrets_force | default(false) }}"`. Secret tasks are skipped in
   `--check`.
10. **Attributes.** The default is `root:root 0400`. A consumer that runs as a configurable non-root
    user gets `owner` and `group` set to that user, mode `0400`. A consumer whose image fixes its
    user gets `group` set to that GID, mode `0440`, owner root. A secret file is never
    world-readable. Each `op_secrets` entry holds its values, with a comment that names the user.
11. **Enforce on each run.** An `ansible.builtin.file` task after each render sets owner, group and
    mode on each run. It does no 1Password lookup and notifies nothing.
12. **Rotation.** Change the field in 1Password, then run the play with `-e op_secrets_force=true`.
    The handler recreates the containers. A credential that a service registers (for example a
    CrowdSec bouncer key) is deregistered before the recreate.

## Reason

- The user decided (2026-10-24): vaults and service accounts split by domain, and the host never
  runs `op`.
- A long-lived controller holds the tokens for all deploys. With one account, a leaked token reads
  every secret. With one account per domain, it reads one vault.
- A runtime secret service on the host keeps a cache of the vault scope and a live token there. It
  does not give live rotation, because a container reads its secrets at start.
- Outside Swarm, a Compose file secret keeps the owner and mode of the host file. Compose ignores
  `uid`, `gid` and `mode` on it.
- `ansible.builtin.copy` with `force: false` does not touch an existing file. Without rule 11, a
  change of attributes has no effect after the first deploy.

## Consequences

- A play that needs two domains uses two tokens. It is not yet known whether the lookup accepts a
  token for each call. If it does not, a wrapper selects the token.
- Vault access of a service account is fixed when it is created. The vaults and the scope of each
  account must be decided before the accounts exist.
- A host cannot refresh its own secrets. A rotation needs a controller run.
- Secret files stay on the host while the stack runs. A group-readable secret is readable by each
  process on the host with that GID.
- HashiCorp Vault stays out. On 2026-10-25 none of its revisit triggers was true: no three hosts
  share secrets yet, and no SSH certificate authority is chosen. Check again when hosts migrate to
  the controller, or when an SSH certificate authority is chosen.

## Alternatives rejected

- **One vault and one service account.** A leak of the one token exposes all secrets.
- **`op` on each host.** Each host then holds a token that can fetch more secrets.
- **1Password Connect.** Extra containers, a cache of the vault and a live token on the host, with no
  gain in rotation.
- **HashiCorp Vault.** A second secret store and a sync from 1Password, for static secrets.
- **Ansible Vault or SOPS.** A second copy of each secret, and a new key to protect.
- **World-readable secret files (`0444`).** Each host user can then read the secret.

## Not repeated

- Do not assume that a Compose secret is readable by the container user.
- Do not rely on `copy` with `force: false` to set attributes on an existing file.
- Do not pass a secret on a command line or print it.
