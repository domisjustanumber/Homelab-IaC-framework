# 0002 — The controller is a Debian 13 VM that runs tofu, Ansible, `op`, Semaphore and the runner

**Status:** proposed, 2026-10-25 (agent); recorded again 2026-11-17 (user: the P3 design answers); accepted, 2026-11-17 (user).

## Decision

1. **One controller.** One controller manages the estate. It is a Debian 13 virtual machine on a
   Proxmox VE node. The site decides the node, the size and the disk layout.
2. **Tools.** The controller runs these tools:
   - `ansible-core` and the Galaxy collections of `requirements.yml`;
   - OpenTofu ([0005](0005-opentofu-scope.md));
   - the 1Password CLI `op`, version 2.30 or later ([0004](0004-secrets-split-by-domain.md));
   - Semaphore UI Community, reachable on the LAN only;
   - a GitHub self-hosted runner that serves the private site repository only.
3. **Pinned tools.** Each tool has a pin, and a tool update is a change to that pin. Renovate
   proposes each bump ([3EV6](3EV6-renovate-proposes-each-version-bump.md)):
   - The controller venv installs the locked `ansible` group of `uv.lock`, the same group that the
     lint image installs. The controller then runs the versions that CI tested.
   - The `controller` role pins OpenTofu by version and sha256. It checks the sha256 of the download.
   - The role pins `op` by version only, because 1Password publishes no checksum. It checks the GPG
     signature of the download with the key that 1Password publishes.
   - The runner updates itself. GitHub stops sending jobs to a runner that is too far behind.
   The lint image stays separate from the controller, and it holds no secret.
4. **Push, not pull.** The controller reaches each managed machine. Ansible uses SSH. OpenTofu uses
   the HTTPS API of each Proxmox VE node. A managed machine runs no agent and needs no inbound
   connection from the internet.
5. **Outbound only.** The runner connects out to GitHub on HTTPS port 443. The controller needs no
   inbound webhook, no public hostname and no published port for the runner.
6. **Single point of trust.** The controller holds the SSH identity for each managed machine, the
   1Password service-account tokens and the OpenTofu state. Each of these has its own entry or
   site decision.
7. **Not in its own state.** The controller VM is never in OpenTofu state. A runbook and a seed
   script build it, and a Proxmox Backup Server restore recovers it. A tofu run on the controller
   then cannot plan to replace the machine that runs it.

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
- The user decided (2026-11-17) the pins, the install checks and that the controller stays out of
  OpenTofu state. A pin that CI tested is the same version on the controller and in the lint image.

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

## Evidence

- OpenTofu publishes `tofu_<version>_SHA256SUMS` with each release, signed:
  <https://opentofu.org/docs/intro/install/standalone/>.
- 1Password publishes a GPG key for `op` and no checksum:
  <https://www.1password.dev/cli/install-server/>.

## Alternatives rejected

- **A Windows workstation with WSL as the controller.** The tokens and the state then live on a
  workstation, and no job can run when the workstation is off.
- **An LXC container.** The user chose a VM.
- **A controller on an existing application host.** The controller then depends on the services that
  it deploys, and a fault in one stops the other.
- **The controller in OpenTofu state, with `prevent_destroy`.** A plan on the controller can still
  try to change the machine that runs it, and a guard is one more thing to keep correct.
- **A hand-made sha256 for `op`.** Nobody can check it against a published value.

## Not repeated

- Do not register the runner on the public framework repository. A public repository lets any
  author start jobs on a self-hosted runner.
