# 0005 — OpenTofu provisions guests, Proxmox VE API objects and PBS backup jobs

**Status:** proposed, 2026-10-25 (agent).

## Decision

1. **Scope.** OpenTofu manages these objects:
   - VM and LXC guests on the Proxmox VE nodes;
   - API objects of each Proxmox VE node: storage, bridges, VLANs and SDN, users and tokens,
     hardware mappings, ACME and the firewall;
   - PBS backup jobs.
2. **Not Cloudflare.** OpenTofu does not manage a Cloudflare resource, and it does not import one.
3. **Boundary with Ansible.** Ansible manages the operating system and the packages of each node
   over SSH. OpenTofu manages only what the node API exposes.
4. **Standalone nodes.** The nodes are standalone Proxmox VE 9.x nodes, not a cluster. Each node is
   its own API endpoint.
5. **Local state.** The state uses the local backend on the controller. OpenTofu native state
   encryption protects it. The encryption key comes from the controller vault in 1Password
   ([0004](0004-secrets-split-by-domain.md)).
6. **State is not in git.** `.gitignore` excludes `*.tfstate*`. The backup of the controller holds
   the state.
7. **Modules here, values in the site.** Reusable modules live in `tofu/modules/` of this repository.
   They hold no host values and pin no provider. Root configurations, lock files and values live in
   the site repository.
8. **A human applies.** Each `tofu apply` needs a human. No automated job applies a plan.

## Reason

- The user decided (2026-10-24) the scope, the local state with native encryption, and that each
  apply needs a human.
- Guests and node objects that are in code can be rebuilt and reviewed. Today they exist only as
  hand-made state on each node.
- Some Cloudflare resources have another owner: the CrowdSec worker bouncer creates and changes them
  itself. A second owner would fight over them.
- The API of a node does not cover its packages or its base OS. Ansible already has roles for that.
- A local backend adds no service that the controller depends on. Encryption keeps the state safe in
  a backup.

## Consequences

- The state holds what OpenTofu reads or creates, including token secrets. A lost key makes the
  state unreadable, and each object must then be imported again.
- If the backup of the controller is lost, the state is lost with it. Import blocks that stay in the
  code let a plan rebuild the state.
- A network object in OpenTofu can cut a node off. Changes to such objects need care at apply time.
- OpenTofu cannot create its own first credential on a node. The site must decide who creates it.
- These are not decided here: the provider, the key provider of the state encryption, one state per
  node or one state for all, which kind of PBS job, and the image of a new guest.

## Alternatives rejected

- **No OpenTofu; guests made by hand.** The user chose to manage guests as code.
- **A remote state backend.** It adds a service that the controller depends on.
- **Cloudflare in OpenTofu.** The user excluded it.
- **OpenTofu for the node OS and packages.** The node API does not expose them.

## Not repeated

- Do not commit a state file or a plan file. Both can hold secrets.
- Do not print a plan with sensitive values in a job log.
