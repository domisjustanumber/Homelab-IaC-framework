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
- **Add the doc checks.** Add `tools/check_decision_log.py`, `tools/check_links.py` and
  `tools/check_private_data.py` with their tests. Every entry of this log has the 6,000-character
  limit, so the decision-log check limits entries from 0001. Until then, run the site copies with
  this repository as the root, and count the entry size by hand.
