# controller

This role configures the controller VM: the machine that runs Ansible, OpenTofu and `op` for the
estate. It installs the pinned tools, the users and the launcher that gives each run one token.

Decisions: [0002](../../decisions/entries/0002-controller-vm.md) (the controller and its pins),
[0004](../../decisions/entries/0004-secrets-split-by-domain.md) (the tokens and the run users),
[3EV6](../../decisions/entries/3EV6-renovate-proposes-each-version-bump.md) (Renovate bumps the pins),
[1KXT](../../decisions/entries/1KXT-run-users-accept-a-new-host-key-on-first-use.md) (host keys)
and [NTK9](../../decisions/entries/NTK9-generic-roles-and-host-values.md) (values).

## Inventory values

Required:

- `controller_op_vault`: the vault of the items that only the controller uses.
- `controller_ssh_key_op_item`: the SSH Key item that reaches the managed machines.
- `controller_deploy_key_op_item`: the SSH Key item of a read-only deploy key of the site repo.
- `controller_site_repo`: the SSH URL of the site repo.
- `controller_site_repo_host_keys`: the `known_hosts` lines of the server of the site repo, for
  example the published keys of GitHub.

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
   `op_secrets_force` is true. Each run user accepts the host key of a new host on first use.
7. It clones the site repo into `controller_checkout_dir` (`/opt/controller/site`) as the
   controller user, with the deploy key and the pinned host keys. It clones once and never pulls.

## The tokens and the launcher

`files/seed.sh` asks for each service-account token that is not on disk, and writes it into
`controller_token_dir` (`/etc/controller/tokens`), as a file that only root can read. The file name is the token name: `hosts` or `controller`. Each run
then goes through the launcher:

```sh
sudo controller-run hosts ansible-playbook playbooks/site.yml --limit myhost
```

The launcher reads the token, starts the command as the run user of that token in a transient
systemd unit, and gives it the token in `OP_SERVICE_ACCOUNT_TOKEN`. A run user has no `sudo` rule, so
code in a run cannot start a run with the other token, and it cannot write into the home of the
other run user.

This role itself runs as root on the controller, with the controller token. Only a human runs it,
through `files/seed.sh` ([Build the controller](#build-the-controller)).

## Build the controller

Do these steps on a new VM. The site decides the node, the size and the disk.

1. Create the two service accounts in 1Password, each with read access to one vault only. Keep
   each token ready. The script asks for each token one time.
2. Create the deploy key of the site repo (read-only) and the SSH key of the controller as SSH Key
   items in the controller vault. Put the public key of the controller key in the hosts vault, in
   an item that holds only the public key.
3. In Proxmox VE, create the VM: Debian 13 netinst ISO, a VirtIO SCSI disk, a VirtIO NIC, and the
   QEMU guest agent turned on in the options. `base` fails without the guest agent.
4. Install Debian 13 with no desktop and with the SSH server. Give `admin_user` as the user of the
   installer.
5. Log in on the console as root. Install Git:

   ```sh
   apt-get update && apt-get install -y git
   ```

6. Put the private deploy key into `/root/.ssh/site-deploy-key` (mode `0600`), in OpenSSH format.
   Put the `ssh-ed25519` line of the GitHub SSH key fingerprints page into
   `/root/.ssh/known_hosts`.
7. Clone the site repo with its submodule, and run the script:

   ```sh
   GIT_SSH_COMMAND='ssh -i /root/.ssh/site-deploy-key -o StrictHostKeyChecking=yes' \
     git clone --recurse-submodules <SSH URL of the site repo> /root/seed
   cd /root/seed && sh framework/roles/controller/files/seed.sh
   ```

8. Run the script a second time. Each of its two runs must report `changed=0`.
9. Remove the seed copy: `rm -rf /root/seed /root/.ssh/site-deploy-key`.

## Update the controller

The controller user pulls the checkout. Then root runs the script from it:

```sh
sudo -u iac git -C /opt/controller/site pull --recurse-submodules
cd /opt/controller/site && sudo sh framework/roles/controller/files/seed.sh
```

To render a key again after a change in 1Password, remove its file. Then run the script.

## Live runs

The controller user starts each live run through the launcher, from its checkout:

```sh
sudo -u iac -i
cd /opt/controller/site
sudo controller-run hosts ansible-playbook playbooks/site.yml --limit myhost
```

After a rebuild of a managed host, remove its old host key from each run user
([1KXT](../../decisions/entries/1KXT-run-users-accept-a-new-host-key-on-first-use.md)):

```sh
for user in iac-hosts iac-controller; do sudo -u "$user" ssh-keygen -R myhost; done
```

## Limits

- The role supports Linux amd64 only.
- A run user can still use `cron` or `at` if they are installed. The controller installs neither.
