# Homelab-IaC-framework

Generic Ansible roles for Debian 13 hosts that run Docker, with the lint tools and the decision log
that come with them.

This is a personal homelab framework. The owner publishes it as it is, with no promise of support.
A separate, private site repository holds the values of each host and uses this framework as a Git
submodule. This repository never holds a host value: no host name, domain, address or account.

## What it holds today

| Role | What it does |
|---|---|
| [`base`](roles/base/README.md) | Configures each Debian 13 host: base packages, the QEMU guest agent, the hostname, the timezone, the admin user with passwordless sudo, sshd (key login only, no root login), chrony, the journald size limit and the hardening sysctls. |
| [`apt_unattended_upgrades`](roles/apt_unattended_upgrades/README.md) | Configures `unattended-upgrades`: the origins, the reboot policy and the report mail. |
| [`avahi`](roles/avahi/README.md) | Publishes the host over mDNS with `avahi-daemon`, and enables `.local` name resolution. |
| [`docker_engine`](roles/docker_engine/README.md) | Removes the distribution container packages, installs Docker CE from the Docker apt repository, and writes `daemon.json`, the mount drop-ins and the containerd root drop-in. A change to these files restarts Docker. The restart stops each container, because `live-restore` is off. |
| [`docker_gc`](roles/docker_gc/README.md) | Installs a daily systemd timer. It runs `docker system prune -af --filter until=<retention>`, which removes stopped containers, unused networks, unused images and the build cache. Then it runs `docker volume prune -f`, which removes only anonymous volumes. |
| [`system_mail`](roles/system_mail/README.md) | Installs msmtp as a null client that relays all system mail to an SMTP relay. |

The repository also holds:

- `tools/lint.sh`, which runs `yamllint` and `shellcheck` from the uv venv, then `ansible-lint`
  and the role checks in the lint image (`tools/lint/`);
- the doc checks in `tools/` (decision log, links, private data, AI attribution) and their tests;
- the decision log in [`decisions/`](decisions/README.md).

Generic Compose stacks ([ADR-0003](decisions/entries/0003-controller-pushes-stacks.md)) and
OpenTofu modules ([ADR-0005](decisions/entries/0005-opentofu-scope.md)) are planned. Their
entries are proposed. Playbooks are planned too, but they have no entry yet.

## Use it

1. Add the framework as a submodule of your site repository:

   ```sh
   git submodule add <url of this repository> framework
   ```

2. Point Ansible at the roles in your site `ansible.cfg`:

   ```ini
   [defaults]
   roles_path = framework/roles:roles
   ```

3. Install the pinned collections:

   ```sh
   ansible-galaxy collection install -r framework/requirements.yml
   ```

4. Give each host its values in your inventory. The README of each role lists its variables.
   Each role with required values checks them first. It stops when a value is not set or is
   empty, or when it contains `CHANGEME` or `CONFIRM`
   ([ADR-NTK9](decisions/entries/NTK9-generic-roles-and-host-values.md)).
5. Apply the roles from your own playbook. `avahi` and `system_mail` do not read their switches
   (`avahi_enabled`, `system_mail_enabled`). Your playbook must apply each of them only when its
   switch is true. `apt_unattended_upgrades` and `docker_gc` read `system_mail_enabled` to add
   mail. When it is true, also set `system_mail_admin`, `system_mail_from` and `hostname`, and
   apply `system_mail`.

Requirements:

- Ansible runs on a Linux controller. The lint image pins ansible-core 2.21.5 and ansible-lint
  26.10.1 (`uv.lock`). The roles are linted with these versions. No test in this repository
  applies a role to a host.
- The roles target Debian 13 (trixie) QEMU/KVM VMs, for example on Proxmox VE. Turn on the QEMU
  guest agent in the VM options before you run `base`, or its guest agent task fails.
- `base` reads the admin SSH public key from 1Password. It has no other key source. The controller
  needs the 1Password CLI (`op`), signed in or with a service account token. A `--check` run skips
  this lookup.
- After `base`, sshd accepts only key login, and root login is off. Run the later plays as
  `admin_user`, with `become`.
- `system_mail` reads the relay password from `/etc/msmtp-password`. The role does not create or
  check this file. Put it on the host first, or each mail fails.

## Checks

```sh
uv sync
uv run pre-commit install
uv run pytest tools/tests
tools/lint.sh
```

`tools/lint.sh` needs Docker for the Ansible checks. In CI, `tools/lint/ci.sh` runs all the lint
and doc checks in the lint image
([ADR-E7ZX](decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md)). A separate workflow
runs `gitleaks`.

## Decisions

The [decision log](decisions/README.md) records each decision, its reasons and the alternatives
that were rejected. A citation in the form `site ADR-<ID>`, or in the older form `site <ID>` (for
example `site 0010`), names an entry of the private site repository. That log is not published.
Each entry here restates every rule that it takes from a site entry.

## Contributions and security

You can open an issue. Each contribution uses the licence of the code: the GNU AGPL version 3 only
([ADR-B7ZV](decisions/entries/B7ZV-licence-agpl-3-0-or-later.md)).

Do not report a security problem in a public issue. Use the private vulnerability reporting of
GitHub, in the Security tab of this repository.

## Licence

Copyright (C) 2026 Dom Scott

SPDX-License-Identifier: AGPL-3.0-only

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
Affero General Public License, version 3 only, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
It is in [`LICENSE`](LICENSE). If not, see <https://www.gnu.org/licenses/>.
