# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The change that closes an item records the result.

- **Restate the generic stack contract before [0003](0003-controller-pushes-stacks.md) is
  accepted.** site 0042 holds the stack contract. Its generic rules stay: the host layout under
  `stack_dir`, the `.env` that Ansible owns, the `.env.example` contract, the generic stack with no
  host values, the recreate of a service when its `config/<service>/` files change, host values
  through the environment or `command:` flags only, no inline `configs:` on a service that Watchtower
  manages, `${VAR:?message}` for each mandatory value, the `common/` fragments and the inline-config
  hash. Restate them without site values, in 0003 or in an entry of their own if 0003 then exceeds
  its limit. Decide whether "deploys follow `main` only" stays. A site entry restates the site
  values of site 0042 and supersedes it.
- **Cross-repository status line.** 0003 supersedes site 0013. The site log must first allow a
  status line that names an entry of this log.
- **Decide the open parts of 0003 before it is accepted:** one Compose project per host or several,
  how public and private stacks are composed and what the push copies, and whether the Compose
  files are renamed for Dependabot.
- **The site log adopts the same process.** [0001](0001-decision-log-agents-md-and-private-data.md)
  states that the site log uses the same rules, with its own copy of the rules and the tools. The
  site log still uses its older process: sequential numbers, a Deferred table and the template in its
  index. A site entry must supersede site 0046 in full and copy the process of this log. Until then,
  a change of the rules here has no matching site change to wait for.
- **Site exceptions to framework rules.** The user decided (2026-10-25): this log decides which of
  its rules allow a site exception, and how. A site entry records each use of that mechanism. A
  rule with no exception mechanism needs a change in this log first. When a rule is written here,
  state whether it allows a site exception and what the site entry must hold. The first known
  case is an application that must mount the Docker socket.
