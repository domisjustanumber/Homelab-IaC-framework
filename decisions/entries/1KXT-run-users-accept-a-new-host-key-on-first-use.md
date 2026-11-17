# 1KXT — The run users of the controller accept a new host key on first use

**Status:** proposed, 2026-11-17 (agent: the answer of the user, 2026-11-17); accepted, 2026-11-17 (user).

## Decision

1. **First use.** The SSH client config of each run user of the controller
   ([0004](0004-secrets-split-by-domain.md) rule 4) sets `StrictHostKeyChecking accept-new`. The
   first connection to a managed host stores its host key in the `known_hosts` file of that run
   user. A later connection with a different key fails.
2. **A rebuilt host.** After a rebuild of a managed host, a human removes its old line from the
   `known_hosts` file of each run user (`ssh-keygen -R <host> -f <file>`).
3. **Git servers.** A Git server stays pinned. The controller user trusts only the host keys of the
   site repo server that the inventory lists, with `StrictHostKeyChecking=yes`.
4. **Not in Ansible.** `host_key_checking` stays `True`. Ansible then adds no option, and the
   client config of the run user applies.

## Reason

- The user decided on 2026-11-17.
- A run user has no login shell, so nobody can answer the prompt of a first connection.
- A host key in the inventory needs a copy from the console at each build and each rebuild of a VM.
- The host keys of GitHub are published and change rarely, so a pin costs nothing there.

## Consequences

- The first connection to a new host trusts the network. An attacker on the LAN at that moment can
  give a false key.
- Each run user has its own `known_hosts` file. A rebuild needs the removal for each run user.
- An SSH certificate authority would remove both steps. It is a trigger of site ADR-0014, and it
  needs its own entry.

## Evidence

- `accept-new` adds the keys of a new host and refuses a changed key, from OpenSSH 7.6:
  <https://man.openbsd.org/ssh_config#StrictHostKeyChecking>.
- With `host_key_checking` set to `True`, the ssh connection plugin adds no
  `StrictHostKeyChecking` option:
  <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ssh_connection.html>.

## Alternatives rejected

- **Each host key in the inventory.** A manual copy at each build and rebuild.
- **`StrictHostKeyChecking no`.** It accepts a changed key with no error.
