# Decision log

This log records the technical decisions of the framework, with their reasons and evidence. An entry
explains **why**. Read this file and [open-work.md](open-work.md) before you change a role, a
playbook, a module, a stack or the agent instructions. Then read the Active entries that apply to
your task. Read a Deferred entry only for work in its area. Read a Historical entry only to find the
reason for a decision ([0001](0001-decision-log.md)).

Each entry gives the decision, its reason, the evidence (when there is evidence), the alternatives
rejected and a "Not repeated" section for pitfalls already found. When a decision changes, add a new
entry that supersedes the old entry in full.

## Index

### Active

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-decision-log.md) | Decision log of the framework: own numbering, restate a site rule only when cited, no link to the site | proposed |
| [0002](0002-controller-vm.md) | The controller is a Debian 13 VM that runs tofu, Ansible, `op`, Semaphore and the runner | proposed |
| [0003](0003-controller-pushes-stacks.md) | The controller pushes Compose stacks; hosts hold no Git credentials | proposed |
| [0004](0004-secrets-split-by-domain.md) | Secrets: vaults and service accounts split by domain; hosts never run `op` | proposed |
| [0005](0005-opentofu-scope.md) | OpenTofu provisions guests, Proxmox VE API objects and PBS backup jobs; local encrypted state | proposed |

### Deferred

These entries are `proposed`. The latest date in their status line is more than 183 days old.

| # | Decision | Status |
|---|----------|--------|

### Historical

These entries are `rejected`, `superseded by NNNN`, `absorbed into <path>#<anchor>` or
`evidence; used by NNNN`.

| # | Decision | Status |
|---|----------|--------|

## Open work

The open work is in [open-work.md](open-work.md).

## Rules

- Write one entry for each decision or measurement.
- The body of an entry that is not `proposed` does not change, except for three edits: a link or
  anchor repair, a typo that does not change the meaning, and the redaction of private data. Each
  edit adds `_Edited YYYY-MM-DD (#PR): <kind>._` at the end of the entry. Until the repo has a
  remote, write the entry that caused the edit in place of the PR.
- A `proposed` entry can change until the user decides it. An agent writes a new entry as
  `proposed`. Only the user changes it to `accepted` or `rejected`.
- To change a decision, add a new entry. It restates each rule of the old entry that stays, and it
  supersedes the old entry in full. Do not supersede, amend or correct a part of an entry.
- The status line of an entry can change. These changes are allowed: `proposed` to `accepted` or
  `rejected`, `accepted` to `superseded by NNNN`, `accepted` to `absorbed into <path>#<anchor>`, and
  `evidence` to `evidence; used by NNNN`. Each change adds its date and the PR that made it (or the
  entry, until the repo has a remote). In the same change, change the status in the index and move
  the row to the table for the new status.
- The Status cell of an index row has only a status form of its table. The Decision cell has 160
  characters or fewer.
- Move a `proposed` row to Deferred when the latest date in its status line is more than 183 days
  old.
- An `evidence` entry gets `evidence; used by NNNN` when an accepted entry cites it for its decision.
- An accepted entry is absorbed when a normative document states all of its rules. The normative
  documents are `AGENTS.md` and the skills of this repository.
- A consolidation entry states the rules that stay from a group of entries, and it supersedes each
  entry of the group. It changes no decision.
- Delete an open-work item when the work is done.
- Keep the log inside its limits: 14,000 characters for this file, 20,000 for `open-work.md`, 6,000
  for each entry, and 220,000 for this file, `open-work.md` and all Active entries together. Put
  long evidence in a tracked file next to the entry, and link to it.
- Give a new entry the number after the highest number in the index. Never reuse a number. Add the
  entry to the index in the same change.
- Cite a tracked file with a relative link. Cite a commit, or the code of another public repo, with
  a GitHub permalink that pins a full SHA on the default branch of that repo.
- In this repo, `ADR-NNNN` and a bare number are always entries of this log. Cite an entry of the
  site log as `site NNNN`. Never link to the site repository, and never name its location.
- An entry that waits for a decision of another repo has a `**Depends on:**` line under its status
  line.
- This repo becomes public. No file holds a credential, a host name, a domain, an IP address other
  than a documentation address (`192.0.2.0/24`), an email address, a user name or a path in a user
  folder. The rule has no exemption.
- Write entries in ASD-STE100 Simplified Technical English. Use short sentences, the active voice and
  one instruction in each sentence. "must" is the requirement word. Technical names, field names,
  values, formulas, code and YAML stay unchanged.

## Entry template

The file name is `NNNN-<short-slug>.md`.

```markdown
# NNNN — <title>

**Status:** <proposed | accepted | evidence>, <YYYY-MM-DD> (<source>).
**Depends on:** <repo> NNNN (<status> on YYYY-MM-DD)

Supersedes [NNNN](NNNN-<slug>.md) in full.

## Decision

## Reason

## Consequences

## Evidence

## Alternatives rejected

## Not repeated
```

- **Status.** `accepted` is a decision. `evidence` is a measurement. `proposed` waits for a decision.
  The source says who decided, for example "user", or who proposed, for example "agent".
- **Depends on.** Optional. Write it only when the entry waits for a decision of another repo.
- **Supersedes.** Optional. Write it only when the entry supersedes other entries. Name each one.
- **Decision.** What is decided, written so that a reader can apply it.
- **Reason.** Why. Each entry gives its own reasons.
- **Consequences.** Optional. What becomes harder, what must change later and what the decision
  costs.
- **Evidence.** Write it only when there is evidence: measurements with their tool and command, or
  code facts with their file and function. Cite upstream docs or code for each claim about them.
- **Alternatives rejected.** The options that were examined and not used, with the reason for each.
- **Not repeated.** Pitfalls already found.
- Omit an optional section when it has no items. Put open-work items in
  [open-work.md](open-work.md), not in an entry.
