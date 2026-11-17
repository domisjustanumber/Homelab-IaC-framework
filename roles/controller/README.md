# controller

This role configures the controller VM: the machine that runs Ansible, OpenTofu and `op` for the
estate. It installs the pinned tools, the users and the launcher that gives each run one token.

Decisions: [0002](../../decisions/entries/0002-controller-vm.md) (the controller and its pins),
[0004](../../decisions/entries/0004-secrets-split-by-domain.md) (the tokens and the run users),
[3EV6](../../decisions/entries/3EV6-renovate-proposes-each-version-bump.md) (Renovate bumps the pins)
and [NTK9](../../decisions/entries/NTK9-generic-roles-and-host-values.md) (values).

## Inventory values

Required:

- `controller_op_vault`: the vault of the items that only the controller uses.
- `controller_ssh_key_op_item`: the SSH Key item that reaches the managed machines.
- `controller_deploy_key_op_item`: the SSH Key item of a read-only deploy key of the site repo.

The defaults (`defaults/main.yml`) give the user names, the paths and the pinned versions.

## What it does

1. It installs the packages, the controller user (`iac`) and one run user for each token
   (`iac-hosts`, `iac-controller`).
2. It installs uv and OpenTofu, and checks the pinned sha256 of each download.
3. It installs `op`, and checks its GPG signature against the code-signing key of 1Password
   (`files/1password-cli.asc`, fingerprint `controller_op_key_fingerprint`). 1Password publishes no
   checksum for `op`.
4. It installs the locked `ansible` group of `uv.lock` into the venv, the same group as the lint
   image, and the collections of `requirements.yml`.
5. It installs the launcher `controller-run`, its config and one `sudo` rule for the controller
   user.
6. It writes the SSH key into the home of each run user, and the deploy key into the home of the
   controller user. It reads a key from 1Password only when the file is missing or
   `op_secrets_force` is true.

## The tokens and the launcher

A human puts each service-account token into `controller_token_dir` (`/etc/controller/tokens`), as a
file that only root can read. The file name is the token name: `hosts` or `controller`. Each run
then goes through the launcher:

```sh
sudo controller-run hosts ansible-playbook playbooks/site.yml --limit myhost
```

The launcher reads the token, starts the command as the run user of that token in a transient
systemd unit, and gives it the token in `OP_SERVICE_ACCOUNT_TOKEN`. A run user has no `sudo` rule, so
code in a run cannot start a run with the other token, and it cannot write into the home of the
other run user.

This role itself runs as root on the controller, with the controller token. Only a human runs it:

```sh
sudo sh -c 'OP_SERVICE_ACCOUNT_TOKEN=$(cat /etc/controller/tokens/controller) exec \
  /opt/controller/venv/bin/ansible-playbook -c local playbooks/controller.yml'
```

## Limits

- The role supports Linux amd64 only.
- A run user can still use `cron` or `at` if they are installed. The controller installs neither.
