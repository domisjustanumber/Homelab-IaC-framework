# Repository Instructions

All new and changed documentation must use ASD-STE100 Simplified Technical English.
This rule applies to `AGENTS.md`, skills, decision entries and templates.
Use short sentences. Use active voice. Use one instruction per sentence.
Use "must" for a requirement.
Keep technical names, field names, values, formulas, code and YAML unchanged.

## 1. Purpose

This repository is a generic, host-agnostic homelab framework.
It holds Ansible roles, playbooks, OpenTofu modules and generic Compose stacks.
A site repository supplies the values of each host and uses this framework.
This repository never holds a site value.

| Path | Role |
|---|---|
| `AGENTS.md` | The single instructions file for coding agents |
| `CLAUDE.md` | Imports this file. It has no other content. |
| `notes/decisions/` | Decision log ([`README.md`](notes/decisions/README.md)) and its open work ([`open-work.md`](notes/decisions/open-work.md)) |
| `tools/` | The doc checks: `check_decision_log.py`, `check_links.py` and `check_private_data.py`. Their tests are in `tools/tests/`. |
| `pyproject.toml` | The dev tools of the doc checks only (`pytest`, `pre-commit`) |
| `.github/workflows/` | The doc checks and the secret scan in CI |
| `plans/` | A local working folder. Git ignores it. |

## 2. Skills

Load the skill that matches the task.
If your agent does not support skills, read the skill file.
Each skill is in `.claude/skills/<skill>/SKILL.md`.
The rules in this file also apply.

This repository has no skills yet.
When you add a skill, add a row to this table.

| Skill | Use it to |
|---|---|

## 3. Install and Test

Run `uv sync`.
Then run `uv run pre-commit install` once in the clone ([section 8](#8-private-data)).
It installs the pre-commit hooks and the pre-push hook.
Run it again in each clone after `.pre-commit-config.yaml` changes.
Use `uv run` for project commands.
Do not depend on an activated virtual environment.

Run `uv run pytest`.
These tests must pass.
Run `uv run pytest tools/tests` to run only the doc checks.
The doc checks test the decision log, the relative links and the private-data rule.
Report each new test failure to the user.
Fix the failures of one root cause in one PR.

## 4. Project Rules

The rules for roles, playbooks, modules and stacks are not written yet.
Do not invent them. Ask the user.
Do not change code that your task does not need.

## 5. Decision Log

Read [`notes/decisions/README.md`](notes/decisions/README.md) and
[`notes/decisions/open-work.md`](notes/decisions/open-work.md) before you change a role, a
playbook, a module, a stack or these instructions.
The log records decisions and the evidence behind them.
Then read the Active entries of the index that apply to your task.
Read a Proposed entry only for work in its section, or when a skill tells you to.
Read an entry of [`historical.md`](notes/decisions/historical.md) only to find the reason for a
decision.
Add one entry for each new decision or measurement.
Write a new entry as `proposed`.
Only the user changes an entry to `accepted` or `rejected`.
An entry has a random ID of 4 characters, for example `k7m2`.
Before you add an entry, run `git fetch` when you can.
Then run `uv run python tools/check_decision_log.py --new`.
Give the entry the ID of the `new:` line.
Create the entry file immediately.
Add its index row at the end of the table for its status, in the same PR.
The pre-push hook runs `uv run python tools/check_decision_log.py --collisions`.
It stops the push when an entry of this tree must change its ID.
Act on each `re-ID:` line. The index [Rules](notes/decisions/README.md#rules) give the steps.
Do not change an ID for a different reason.
Do not keep two index rows with one ID when you resolve a merge conflict.
Do not rewrite the body of an entry that is not `proposed`.
Four edits are allowed: a link or anchor repair, a typo fix that keeps the meaning, the redaction of
private data, and a change of ID with the repair of its citations.
Each of these edits adds an `_Edited_` line with the date and the PR.
Until the repository has a remote, name the entry that caused the edit in place of the PR.
To change a decision, add a new entry. It restates the rules that stay and supersedes the old entry
in full.
Do not supersede a part of an entry.
Keep the log inside its limits. `uv run pytest tools/tests` checks them.
Cite tracked files and decision entries with relative links.
Cite a commit, or the code of another public repository, with a GitHub permalink.
The permalink must pin a full SHA on the default branch of that repository.
Do not put dated status lines in this file. Put them in the open work or in an entry.
Do not cite or link to `plans/`.
In this repository, `ADR-XXXX` and a bare ID are entries of this log.
Write the repository name before an entry ID of another repository, for example `site 0013`.
Cite an entry of the site log as `site XXXX`, with no link.
Never link to the site repository, and never name its location.
Restate a site rule here only when framework code or framework documents cite it.
Cite a provisional entry of another repository by the repository name, the PR number and the slug.
Do not import a file, a test or a tool from another repository.

## 6. Git Rules

- `plans/` is a local working folder. Git ignores it. Do not commit it (decision
  [0001](notes/decisions/0001-decision-log-agents-md-and-private-data.md)).
- Do not push to a git remote without the approval of the user.
- Ask the user before any other action that is visible outside this machine, for example a PR, a
  PR comment, a release or a published image.
- Open each PR against `main`.
- Put one kind of change in each PR: code, docs or CI.
- Run each workflow on a GitHub-hosted runner. Never use `self-hosted`: a fork PR of a public
  repository can run code on a self-hosted runner.

## 7. Tool Calls

Before a tool call that needs user permission, write a one-line summary of the call.
The summary must tell what the call does and what it changes.
Write the summary in the message text, not only in the tool description.

## 8. Private Data

This repository is public, or it can become public. Git history is permanent (decision
[0001](notes/decisions/0001-decision-log-agents-md-and-private-data.md)).
The rule has no exemption. No folder may hold host values.
Do not write these in a tracked file, a commit message or a PR body:

- a credential, a token, a password or a private key;
- an absolute path in a user folder;
- a hostname, a domain or a user name;
- an email address that is not on the allowlist of `tools/check_private_data.py`;
- a private URL, or an IP address that is not a documentation address;
- a raw dump of `env`, `pip list`, `docker inspect` or `op item get`.

In prose and examples, use a documentation address (`192.0.2.0/24`) or name the variable.
Use paths relative to the repository, for example `notes/decisions/README.md`.
Give a measurement as a summary with its tool and its version.
Text from `plans/` must obey these rules before it goes into a tracked file.
If you find private data in a tracked file, remove it with a redaction edit.
Then tell the user, because git history keeps the data.

`uv run pytest tools/tests` runs `tools/check_private_data.py`.
To also block a hostname or a user name, put it in the file `.private-terms` in the repository root.
Git ignores that file. Do not commit it.
The pre-commit hook runs `gitleaks` and the private-data check.
The pre-push hook runs the collision check of the decision-log IDs.
`.github/workflows/secrets.yml` runs `gitleaks` on each push and PR.
