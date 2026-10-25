# 0003 — The controller pushes Compose stacks; hosts hold no Git credentials

**Status:** proposed, 2026-10-25 (agent).

Supersedes site 0013 in full. This entry restates each rule of site 0013 that stays. It changes one:
how the stack files reach the host.

## Decision

**Where stacks live**

1. **Split by stack.** A generic stack (for example Watchtower or socket-proxy) lives in this
   repository. A personal or identifying stack lives in the site repository. Each stack is classed
   when it moves.
2. **One pin.** The site repository pins this repository as a Git submodule. A site stack reaches a
   generic stack through Compose `include:` and that submodule.

**How stacks reach the host**

3. **Push from the controller.** The play copies the stack files from the checkout on the controller
   to the host, before the deploy. The module then reads them on the host. The host holds no Git
   checkout, no deploy key and no other Git credential.
4. **Deploy module.** The play deploys with `community.docker.docker_compose_v2`:

   ```yaml
   - name: Deploy stack
     community.docker.docker_compose_v2:
       project_src: "{{ docker_dir }}/{{ stack_name }}"
       files: ["compose.yaml"]
       state: present
       pull: missing
       remove_orphans: true
       wait: true
       wait_timeout: 180
   ```

5. **`pull: missing`.** Ansible never upgrades an image that is already present.
6. **`wait: true`.** The play fails when a healthcheck never passes. It does not report success for
   a dead container.
7. **`remove_orphans: true`.** When a fragment is removed, the next run removes its service.
8. **No restart for config changes.** The play does not use `state: restarted`. A config change
   recreates its service.
9. **Rotation recreates.** A secret rotation recreates the containers. It never restarts them,
   because a restart does not mount the secrets again.
10. **Image movement.** Ansible does not move images. A service that follows a moving tag gets new
    images from Watchtower. A pinned service gets a new image only from a merged tag change. The site
    decides which services are pinned.

## Reason

- The user decided (2026-10-24): the controller pushes stack files from its checkout, and hosts hold
  no Git credentials. This reverses the host pull of the site stack contract.
- A host without Git credentials cannot read other stacks of the repository. A pull model gave each
  host a key that could read every host folder.
- The controller already holds the checkout for Ansible and OpenTofu. A second checkout on each host
  adds a credential and a moving part.
- Rules 4 to 9 keep the deploy idempotent: a second run reports `changed=0`.

## Consequences

- A stack change reaches a host only through a controller run.
- The controller needs the files of the framework submodule at the pinned commit.
- A fresh host has no images, so `pull: missing` pulls each image once on the first run.
- Config drift inside a running container is corrected only by a recreate.
- These are not decided here: one Compose project per host or several, how public and private
  stacks are composed, whether the Compose files are renamed for Dependabot, and how the play finds
  the config files that changed since the last deploy.

## Alternatives rejected

- **Host pull from a stack repository with a read-only deploy key.** The site used it before. Each
  host held a key that could read all stacks, and the deploy depended on Git access from the host.
- **`ansible.builtin.command: docker compose up -d`.** It is always `changed`, it does not wait for
  health, and it shows no errors.
- **`community.docker.docker_compose` (v1).** Deprecated in favour of v2.
- **Portainer stacks.** Manual, outside Ansible, with no review of the code.
- **An Ansible call to the Watchtower HTTP API.** More moving parts for no gain.

## Not repeated

- Do not let Ansible pull a newer image on each run. It bypasses the update policy and makes the
  deploy non-deterministic.
- Do not restart a container after a secret rotation. Recreate it.
