# Decision log

This log records the technical decisions of the framework, with their reasons and evidence. An entry
explains **why**. Read this file and [open-work.md](open-work.md) before you change a role, a
playbook, a module, a stack or the agent instructions. Then read the Active entries that apply to
your task. Then you do not repeat a settled question or a completed measurement. Read a Proposed
entry only for work in its section, or when a skill tells you to. Read an entry of
[historical.md](historical.md) only to find the reason for a decision
([ADR-0001](entries/0001-decision-log-agents-md-and-private-data.md)).

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
| [0001](entries/0001-decision-log-agents-md-and-private-data.md) | Decision log of the framework and its rules; own IDs; restate a site rule only when cited; `AGENTS.md` only; no private data | accepted |
| [BQXN](entries/BQXN-debian-hosts-and-the-base-role.md) | Managed hosts run Debian 13, with no Ubuntu parts; the `base` role hardens sshd and installs the guest agent | accepted |
| [EQ0Z](entries/EQ0Z-unattended-upgrades-and-reboots.md) | Unattended upgrades match Debian's security suite; the upgrade time is in the window; reboots are automatic and opt-in | accepted |
| [GEE3](entries/GEE3-system-mail-through-msmtp.md) | System mail goes through an SMTP relay with msmtp, as a null client | accepted |
| [APG1](entries/APG1-daily-docker-gc.md) | Daily Docker GC with anonymous-only volume pruning | accepted |
| [MSAM](entries/MSAM-docker-host-vm-disks.md) | A Docker host VM has three disks, ext4 by UUID, and all three are in the backup | accepted |
| [XQ9A](entries/XQ9A-guest-backups-by-the-hypervisor.md) | The hypervisor backs up each guest to PBS; no backup agent in the guest; a restore drill before go-live | accepted |
| [NTK9](entries/NTK9-generic-roles-and-host-values.md) | Roles are generic; host values come from the inventory of the site; feature switches | accepted |
| [CVM2](entries/CVM2-storage-layout-containerd-root-by-flag.md) | Docker hosts keep state apart from image churn; the containerd root is set by a `--root` flag, not in the package conffile | accepted |

### Proposed

These entries wait for a decision of the user. Section is the section or area of the change, or
`none`.

| # | Decision | Section | Status |
|---|----------|---------|--------|
| [0002](entries/0002-controller-vm.md) | The controller is a Debian 13 VM that runs tofu, Ansible, `op`, Semaphore and the runner | `controller` | proposed |
| [0003](entries/0003-controller-pushes-stacks.md) | The controller pushes Compose stacks; hosts hold no Git credentials | `stacks` | proposed |
| [0004](entries/0004-secrets-split-by-domain.md) | Secrets: vaults and service accounts split by domain; hosts never run `op` | `secrets` | proposed |
| [0005](entries/0005-opentofu-scope.md) | OpenTofu provisions guests, Proxmox VE API objects and PBS backup jobs; local encrypted state | `tofu` | proposed |
| [B7ZV](entries/B7ZV-licence-agpl-3-0-or-later.md) | The framework is licensed under the GNU AGPL, version 3 or later | `licence` | proposed |
| [NXK2](entries/NXK2-current-decision-log-kit.md) | The current decision-log kit: essential Rules, `decisions/entries/`, upper-case IDs with a digit, `ADR-` citations, no AI attribution, linters in a uv venv | `process` | proposed |

The entries that are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX` or `done` are in [historical.md](historical.md).

## Open work

The open work is in [open-work.md](open-work.md).

## Rules

- The body of an entry that is not `proposed` changes only by four edits: a link or anchor repair, a
  typo that does not change the meaning, the redaction of private data, and a change of ID with the
  repair of its citations. Each edit adds `_Edited YYYY-MM-DD (#PR): <kind>._` at the end of the
  entry, for example `re-ID from XXXX`. For a change of ID, the renamed entry gets
  `re-ID from XXXX`, and each repaired entry gets `citation repair`. Add these two lines only to an
  entry that is on `main`. When a change has no PR, write the entry that caused the edit in place of
  the PR.
- When the source of a `proposed` entry changes (for example, the site sends a new version of the
  proposal that the entry records), edit the same entry. Do not add a second entry. Its status line
  adds `recorded again <YYYY-MM-DD> (<source>)`.
- An absorb document is one of these: `AGENTS.md`, the skills, the Rules of this file with
  [template.md](template.md), and the docstring of a tool in `tools/` for the rules that it checks.
  An accepted entry is absorbed when one absorb document states all of its rules.
- The entry that supersedes an old entry restates each rule of the old entry that stays. A link can
  restate a rule. The link must go to a heading of an absorb document, and that heading must state
  the rule. The commit that changes the text under such a heading cites its own entry next to the
  changed rule.
- Only these status changes are allowed: `proposed` to `accepted` or `rejected`; `accepted` to
  `superseded by XXXX`, `absorbed into <path>#<anchor>` or `done`; `absorbed into <path>#<anchor>`
  to `superseded by XXXX`; and `evidence` to `evidence; used by XXXX`, when an accepted entry cites
  the `evidence` entry for its decision. `done` is for an accepted entry that records a one-off
  action, with no rule that stays, when the action is complete. Each status change adds its date and
  the PR that made it (or the entry, when the change has no PR). In the same change, change the
  status in the index and move the row to the table for the new status.
- `tools/check_decision_log.py` checks the tables, the status forms, the Section cell, the ID
  alphabet and the size limits. Its docstring states them. `tools/check_links.py` checks the links
  and the full-SHA permalinks. A tool is the source of a rule that it checks.
- A consolidation entry states the rules that stay from a group of entries, and it supersedes each
  entry of the group. It changes no decision. Write one when the read-path limit fails.
- Delete an open-work item when the work is done. Put a dated fact in `open-work.md` or in an
  entry, not in `AGENTS.md`.
- Put long evidence in a tracked file next to the entry, and link to it. A PR can lower a limit of
  `tools/check_decision_log.py`. A PR that raises a limit must add an entry.
- An ID changes only on a `re-ID:` line of `tools/check_decision_log.py`, to the ID of a new `--new`
  run.
- Until a commit is on `main`, cite its PR number and the file path, not its SHA. The `ADR-` prefix
  is for citations only: a file name, a heading, an index row, a status line and a YAML value hold
  the bare ID. Write an ID in a YAML value in quotes. Cite a provisional entry of another repo by the
  repo name, the PR number and the slug. Do not edit a decided entry only to add or move the prefix
  or the link.
- The IDs of this log are independent of the site log. An ID without a repo name is an entry of this
  log.
- A site entry that holds both generic rules and site values splits: an entry of this log restates
  the generic rules, and a new site entry restates the site values and supersedes the old site entry
  in full. An entry of this log that supersedes a site entry states it under its status line, for
  example `Supersedes site ADR-0013 in full.` The supersession of an entry of this log is only in
  the status line of the old entry.
- A `**Depends on:**` line names a site entry as `site ADR-<ID>`, with no permalink.
- The Evidence section of an entry cites the upstream docs or code for each claim about them.
- The site log uses the same rules. Each repo keeps its own copy of the rules and of the tools. A
  change of these rules needs a matching change in the site log. The entry of the change cites its
  mirror entry as `site ADR-<ID>`. No file of one repo imports from the other repo.
