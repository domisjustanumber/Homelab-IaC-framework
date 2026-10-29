# Decision log

This log records the technical decisions of the framework, with their reasons and evidence. An entry
explains **why**. Read this file and [open-work.md](open-work.md) before you change a role, a
playbook, a module, a stack or the agent instructions. Then read the Active entries that apply to
your task. Then you do not repeat a settled question or a completed measurement. Read a Proposed
entry only for work in its section, or when a skill tells you to. Read an entry of
[historical.md](historical.md) only to find the reason for a decision
([0001](0001-decision-log-agents-md-and-private-data.md)).

Each entry gives the decision, its reason, the evidence (when there is evidence), the alternatives
rejected and a "Not repeated" section for pitfalls already found. When a decision changes, add a new
entry that supersedes the old entry in full. A change of the text under a heading that an entry
links does not supersede that entry. The body of a decided entry changes only by the edits that the
[Rules](#rules) allow. To write an entry, use [template.md](template.md).

## Index

### Active

These entries are `accepted` or `evidence`.

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-decision-log-agents-md-and-private-data.md) | Decision log of the framework and its rules; own IDs; restate a site rule only when cited; `AGENTS.md` only; no private data | accepted |
| [bqxn](bqxn-debian-hosts-and-the-base-role.md) | Managed hosts run Debian 13, with no Ubuntu parts; the `base` role hardens sshd and installs the guest agent | accepted |
| [eq0z](eq0z-unattended-upgrades-and-reboots.md) | Unattended upgrades match Debian's security suite; the upgrade time is in the window; reboots are automatic and opt-in | accepted |
| [gee3](gee3-system-mail-through-msmtp.md) | System mail goes through an SMTP relay with msmtp, as a null client | accepted |
| [apg1](apg1-daily-docker-gc.md) | Daily Docker GC with anonymous-only volume pruning | accepted |
| [msam](msam-docker-host-vm-disks.md) | A Docker host VM has three disks, ext4 by UUID, and all three are in the backup | accepted |
| [xq9a](xq9a-guest-backups-by-the-hypervisor.md) | The hypervisor backs up each guest to PBS; no backup agent in the guest; a restore drill before go-live | accepted |
| [ntk9](ntk9-generic-roles-and-host-values.md) | Roles are generic; host values come from the inventory of the site; feature switches | accepted |
| [cvm2](cvm2-storage-layout-containerd-root-by-flag.md) | Docker hosts keep state apart from image churn; the containerd root is set by a `--root` flag, not in the package conffile | accepted |

### Proposed

These entries wait for a decision of the user. Section is the section or area of the change, or
`none`.

| # | Decision | Section | Status |
|---|----------|---------|--------|
| [0002](0002-controller-vm.md) | The controller is a Debian 13 VM that runs tofu, Ansible, `op`, Semaphore and the runner | `controller` | proposed |
| [0003](0003-controller-pushes-stacks.md) | The controller pushes Compose stacks; hosts hold no Git credentials | `stacks` | proposed |
| [0004](0004-secrets-split-by-domain.md) | Secrets: vaults and service accounts split by domain; hosts never run `op` | `secrets` | proposed |
| [0005](0005-opentofu-scope.md) | OpenTofu provisions guests, Proxmox VE API objects and PBS backup jobs; local encrypted state | `tofu` | proposed |
| [b7zv](b7zv-licence-agpl-3-0-or-later.md) | The framework is licensed under the GNU AGPL, version 3 or later | `licence` | proposed |
| [NXK2](NXK2-current-decision-log-kit.md) | The current decision-log kit: upper-case IDs, `ADR-` citations, `decisions/`, no AI attribution, linters in a uv venv | `process` | proposed |

The entries that are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX` or `done` are in [historical.md](historical.md).

## Open work

The open work is in [open-work.md](open-work.md).

## Rules

- Write one entry for each decision or measurement. Use [template.md](template.md).
- The body of an entry that is not `proposed` does not change, except for four edits: a link or
  anchor repair, a typo that does not change the meaning, the redaction of private data, and a
  change of ID with the repair of its citations. Each edit adds `_Edited YYYY-MM-DD (#PR): <kind>._`
  at the end of the entry. `<kind>` is `link repair`, `typo`, `redaction`, `re-ID from XXXX` or
  `citation repair`. When a change has no PR, write the entry that caused the edit in place of the
  PR.
- A `proposed` entry can change until the user decides it. An agent writes a new entry as
  `proposed`. Only the user changes it to `accepted` or `rejected`.
- When the source of a `proposed` entry changes (for example, another repo sends a new version of
  the proposal that the entry records), edit the same entry. Do not add a second entry. Its status
  line adds `recorded again <YYYY-MM-DD> (<source>)`.
- To change a decision, add a new entry. It restates each rule of the old entry that stays, and it
  supersedes the old entry in full. Do not supersede, amend or correct a part of an entry. A link can
  restate a rule. The link must go to a heading of a normative document of the absorb rule below, and
  that heading must state the rule. Then that document is the only source of the rule. The commit
  that changes the text under such a heading cites its own entry next to the changed rule. A later
  entry that changes the text under such a heading does not supersede the linking entry. A later
  entry that changes a rule that the linking entry states in its own text supersedes the linking
  entry in full.
- The status line of an entry can change. These changes are allowed: `proposed` to `accepted` or
  `rejected`, `accepted` to `superseded by XXXX`, `accepted` to `absorbed into <path>#<anchor>`,
  `absorbed into <path>#<anchor>` to `superseded by XXXX`, `accepted` to `done`, and `evidence` to
  `evidence; used by XXXX`. Each change adds its date and the PR that made it (or the entry, when
  the change has no PR). An absorbed entry is superseded when a new entry changes one of its rules.
  In the same change, change the status in the index and move the row to the table for the new
  status.
- The tables and their status forms: Active (`accepted`, `evidence`) and Proposed (`proposed`) in this
  file, and Historical (`rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
  `evidence; used by XXXX`, `done`) in [historical.md](historical.md). The Status cell has only a
  status form of its table. `XXXX` must be an entry that is not `proposed` or `rejected`. The
  Decision cell has 160 characters or fewer.
- A Proposed row has a Section cell: the section or area of the change as an ID in backticks, or
  `none`.
- An `evidence` entry gets `evidence; used by XXXX` when an accepted entry cites it for its decision.
- An accepted entry is absorbed when a normative document states all of its rules. The normative
  documents are `AGENTS.md`, the skills, and the Rules of this file with [template.md](template.md).
  Then that document is the source of the rules.
- An accepted entry that records a one-off action, with no rule that stays, is `done` when the action
  is complete.
- A consolidation entry states the rules that stay from a group of entries, and it supersedes each
  entry of the group. It changes no decision. Write one when the read-path limit fails.
- Delete an open-work item when the work is done.
- Keep the log inside its limits: 14,000 characters for this file, 20,000 for `open-work.md`, 6,000
  for each entry without its status line and its `_Edited` lines, and 220,000 for the read path:
  this file, `open-work.md` and the Active entries. Proposed and Historical entries are not in the
  read path. Put long evidence in a tracked file next to the entry, and link to it. Run
  `uv run python tools/check_decision_log.py` to see the read-path size and the warnings at 80% of a
  limit. `uv run pytest tools/tests` runs the same check.
- The tool counts characters after it changes CRLF to LF. It checks the rows, the tables, the cells,
  the status forms, the `XXXX` of each status and the limits. A warning does not fail the doc tests.
  An entry does not warn. A PR can lower a limit. A PR that raises a limit must add an entry.
- An entry ID has 4 characters from `0123456789ABCDEFGHJKMNPQRSTVWXYZ`. The first character is a
  letter. Write an ID in upper case in each file name, heading, index row and citation. IDs that
  differ only in case are one ID. Entries 0001 to 0005 keep their numbers. Do not make a new
  all-digit ID. The IDs of this log are independent of the site log.
- Before you add an entry, run `git fetch --all` when you can. Then run
  `uv run python tools/check_decision_log.py --new`. Give the entry the ID of the `new:` line. Create
  its file immediately. Add its index row at the end of the table for its status, in the same PR. The
  index order is the order of addition.
- The pre-push hook runs `--collisions`, the same check without the `new:` line. A `re-ID:` line
  names an entry of this tree whose ID a different file has on another branch or worktree. Both sides
  get the same verdict: an entry on `main` wins, then an entry on a remote-tracking branch, then the
  entry whose first commit has the earlier author date, then the file name that sorts first. An
  uncommitted file loses to a committed file. Refs merged into `HEAD`, the upstream and push refs of
  the branch, `backup/` branches and an old file name of an entry are not collisions. An ID does not
  change for a different reason.
- To change an ID, run `--new`. Rename the file to the new ID. Change the ID in its heading and in its
  index row. Find the citations with `git grep -n -i -E "\bXXXX\b|XXXX-"`, and repair each one. Ask
  the user before you change a PR title or a PR body. If the entry is on `main`, add
  `_Edited YYYY-MM-DD (#PR): re-ID from XXXX._` to it, and a `citation repair` line to each entry on
  `main` that you repair.
- Do not give an ID that an entry had on `main` to a different entry. Do not keep two index rows with
  one ID.
- A tool is code that the repo runs in its normal work: a test, a hook, a CI job, a skill or a
  workflow step calls it, or it writes a tracked file. Each tool is in `tools/`. A tool has tests.
- A script made the evidence for an entry, or did a one-off job that an entry records, and that entry
  names it. No test, hook, CI job, skill or workflow step runs it on the files of the repo. A script
  does not change after its entry is decided. It is in the `scripts/` folder of the log. Its own
  tests are in `scripts/tests/`. When a later step starts to run a script, move it to `tools/` and
  add a test.
- Cite a tracked file with a relative link. Cite a commit, or the code of another public repo, with a
  GitHub permalink that pins a full 40-character SHA on the default branch of that repo. Do not cite
  or link `plans/`.
- Until a commit is on `main`, cite its PR number and the file path, not its SHA.
- Cite an entry of this log as `ADR-<ID>`. Put the prefix in the link text. A bare ID is always an
  entry of this log. Do not use the prefix in a file name, a heading, an index row, a status line or
  a YAML value. End each commit subject that adds or changes an entry with `(ADR-<ID>)`. Write an ID
  in YAML front matter in quotes. Cite a provisional entry of another repo by the repo name, the PR
  number and the slug.
- Cite an entry of the site log as `site XXXX`, with no link. Never link to the site repository, and
  never name its location.
- A site rule becomes an entry of this log only when framework code or framework documents cite it.
  A site entry that holds both generic rules and site values splits: an entry of this log restates
  the generic rules, and a new site entry restates the site values and supersedes the old site entry
  in full.
- An entry that waits for a decision of another repo has a `**Depends on:**` line under its status
  line.
- The site log uses the same rules. Each repo keeps its own copy of the rules and of the tools. A
  change of these rules needs a matching change in the site log. No file of one repo imports from the
  other repo.
- This repo becomes public. No file holds a credential, a host name, a domain, an IP address other
  than a documentation address (`192.0.2.0/24`), an email address, a user name or a path in a user
  folder. The rule has no exemption.
- Write entries in ASD-STE100 Simplified Technical English. Use short sentences, the active voice and
  one instruction in each sentence. "must" is the requirement word. Technical names, field names,
  values, formulas, code and YAML stay unchanged.
