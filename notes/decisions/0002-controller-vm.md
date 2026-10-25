# 0002 — The controller is a Debian 13 VM that runs tofu, Ansible, `op`, Semaphore and the runner

**Status:** proposed, 2026-10-25 (agent).

## Decision

1. **One controller.** One controller manages the estate. It is a Debian 13 virtual machine on a
   Proxmox VE node. The site decides the node, the size and the disk layout.
2. **Tools.** The controller runs these tools:
   - `ansible-core` and the Galaxy collections of `requirements.yml`;
   - OpenTofu ([0005](0005-opentofu-scope.md));
   - the 1Password CLI `op`, version 2.30 or later ([0004](0004-secrets-split-by-domain.md));
   - Semaphore UI Community, reachable on the LAN only;
   - a GitHub self-hosted runner that serves the private site repository only.
3. **Pinned tools.** The controller role pins the version of each tool. A tool update is a change to
   that pin. The lint image stays separate from the controller, and it holds no secret.
4. **Push, not pull.** The controller reaches each managed machine. Ansible uses SSH. OpenTofu uses
   the HTTPS API of each Proxmox VE node. A managed machine runs no agent and needs no inbound
   connection from the internet.
5. **Outbound only.** The runner connects out to GitHub on HTTPS port 443. The controller needs no
   inbound webhook, no public hostname and no published port for the runner.
6. **Single point of trust.** The controller holds the SSH identity for each managed machine, the
   1Password service-account tokens and the OpenTofu state. Each of these has its own entry or
   site decision.

## Reason

- The user decided (2026-10-24): controller first, as a Debian 13 VM, with Semaphore UI Community
  and a self-hosted runner for merge deploys.
- A VM on Proxmox VE has the same backup path as each other guest. A backup of the VM also holds
  the tool versions, the checkout and the state.
- Debian 13 is the base OS of the managed guests. The controller then uses the same packages and
  the same update policy.
- One fixed place for the tokens and the state is easier to protect than a workstation. A local
  OpenTofu state lock protects only one machine.
- An outbound runner needs no inbound path. It adds no public hostname and no published port.

## Consequences

- The controller is a high-value target. A compromise of the controller gives root on each managed
  machine and access to each vault that it can read.
- The controller cannot rebuild itself or the node that holds it. The site must decide a bootstrap
  path and a disaster-recovery path before the first build.
- The runner credentials are files on the controller. A restored clone of the controller on the
  network can take jobs as the same runner. A restore test must keep the clone off the network.
- These are site decisions, not part of this entry: the node and size, the bootstrap and recovery
  path, whether the controller manages itself, whether live runs from other machines continue, and
  where the tokens are stored.

## Alternatives rejected

- **A Windows workstation with WSL as the controller.** The tokens and the state then live on a
  workstation, and no job can run when the workstation is off.
- **An LXC container.** The user chose a VM.
- **A controller on an existing application host.** The controller then depends on the services that
  it deploys, and a fault in one stops the other.

## Not repeated

- Do not register the runner on the public framework repository. A public repository lets any
  author start jobs on a self-hosted runner.
