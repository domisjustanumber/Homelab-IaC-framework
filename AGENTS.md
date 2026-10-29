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
| `decisions/` | Decision log ([`README.md`](decisions/README.md)) and its open work ([`open-work.md`](decisions/open-work.md)) |
| `roles/` | Generic, host-agnostic Ansible roles |
| `ansible.cfg`, `requirements.yml` | The Ansible config of the lint run, and the pinned collections |
| `tools/` | The doc checks: `check_decision_log.py`, `check_links.py`, `check_private_data.py` and `check_ai_attribution.py`. Their tests are in `tools/tests/`. The lint container: `lint.sh` and `lint/`. |
| `pyproject.toml` | The dev tools of the doc checks only (`pytest`, `pre-commit`) |
| `.github/workflows/` | The doc checks, the lint suite and the secret scan in CI |
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
It installs the pre-commit hooks, the commit-msg hook and the pre-push hook.
Run it again in each clone after `.pre-commit-config.yaml` changes.
Use `uv run` for project commands.
Do not depend on an activated virtual environment.

Ansible, `ansible-lint`, `yamllint` and `shellcheck` do not run natively on a Windows controller.
Run them in the pinned lint container:

```sh
tools/lint.sh                      # yamllint, ansible-lint, the role checks and shellcheck
tools/lint.sh ansible-lint roles/base
```

The image (`tools/lint/Dockerfile`) pins ansible-core, the linters and the collections from
`requirements.yml`.
When either changes, bump `IMAGE` in `tools/lint.sh`.
A site builds the same image from its `framework/` submodule.

Run `uv run pytest` and `tools/lint.sh`.
These checks must pass.
Run `uv run pytest tools/tests` to run only the doc checks.
The doc checks test the decision log, the relative links, the private-data rule and the
AI-attribution check.
Report each new test failure to the user.
Fix the failures of one root cause in one PR.

## 4. Project Rules

Each role follows [ADR-NTK9](decisions/NTK9-generic-roles-and-host-values.md).
A role holds no host value.
A role reads each value from the inventory of the site or from its `defaults/main.yml`.
Each role lists its required values and its opt-in values in `vars/main.yml`.
`tools/lint/check_roles.py` tests these lists.
Add a `# See ADR-XXXX` comment where a line exists because of a decision, with the path of the entry.
The rules for playbooks, modules and stacks are not written yet.
Do not invent them. Ask the user.
Do not change code that your task does not need.

## 5. Decision Log

Read [`decisions/README.md`](decisions/README.md) and
[`decisions/open-work.md`](decisions/open-work.md) before you change a role, a
playbook, a module, a stack or these instructions.
The log records decisions and the evidence behind them.
Then read the Active entries of the index that apply to your task.
Read a Proposed entry only for work in its section, or when a skill tells you to.
Read an entry of [`historical.md`](decisions/historical.md) only to find the reason for a
decision.
Add one entry for each new decision or measurement.
Write a new entry as `proposed`.
Only the user changes an entry to `accepted` or `rejected`.
An entry has a random upper-case ID of 4 characters, for example `K7M2`.
Before you add an entry, run `git fetch` when you can.
Then run `uv run python tools/check_decision_log.py --new`.
Give the entry the ID of the `new:` line.
Create the entry file immediately.
Add its index row at the end of the table for its status, in the same PR.
The pre-push hook runs `uv run python tools/check_decision_log.py --collisions`.
It stops the push when an entry of this tree must change its ID.
Act on each `re-ID:` line. The index [Rules](decisions/README.md#rules) give the steps.
Do not change an ID for a different reason.
Do not keep two index rows with one ID when you resolve a merge conflict.
Do not rewrite the body of an entry that is not `proposed`.
Four edits are allowed: a link or anchor repair, a typo fix that keeps the meaning, the redaction of
private data, and a change of ID with the repair of its citations.
Each of these edits adds an `_Edited_` line with the date and the PR.
When a change has no PR, name the entry that caused the edit in place of the PR.
To change a decision, add a new entry. It restates the rules that stay, in full or by a link to a
heading that states the rule, and supersedes the old entry in full.
A later change under that heading does not supersede the linking entry.
Do not supersede a part of an entry.
Keep the log inside its limits. `uv run pytest tools/tests` checks them.
Cite tracked files and decision entries with relative links.
Cite a commit, or the code of another public repository, with a GitHub permalink.
The permalink must pin a full SHA on the default branch of that repository.
Do not put dated status lines in this file. Put them in the open work or in an entry.
Do not cite or link to `plans/`.
Cite an entry of this repository as a Markdown link with `ADR-<ID>` as the link text.
Write the ID in upper case.
This rule applies to each text that you write: a tracked file, a plan, a PR body and a reply to the
user. In a reply or a plan, the path is relative to the repository root or to the file.
Write the repository name before an entry ID of another repository, for example `site 0013`.
Cite an entry of the site log as `site XXXX`, with no link.
Never link to the site repository, and never name its location.
An entry of another public repository can be on the default branch of that repository.
Then also link it with a GitHub permalink that pins a full SHA.
An ID without a repository name is an entry of this repository.
Restate a site rule here only when framework code or framework documents cite it.
Do not use the prefix in a file name, an entry heading, an index row, a status line or a YAML value.
End each commit subject that adds or changes an entry with `(ADR-<ID>)`.
A commit message cannot hold a working link. In the commit body, write `ADR-<ID>` with no link.
Cite a provisional entry of another repository by the repository name, the PR number and the slug.
Do not import a file, a test or a tool from another repository.

## 6. Git Rules

- `plans/` is a local working folder. Git ignores it. Do not commit it
  ([ADR-0001](decisions/0001-decision-log-agents-md-and-private-data.md)).
- Do not push to a git remote without the approval of the user. One approval for a PR covers its
  push, its draft PR and its description.
- Ask the user before any other action that is visible outside this machine, for example a PR
  comment, a later change to a PR description, a change of a draft PR to ready, a release or a
  published image. A force-push is a new push. It needs its own approval.
- Do not add AI attribution, for example a `Co-Authored-By:` trailer, to a commit or a PR.
- Open each PR against `main`.
- Put one kind of change in each PR: code, docs or CI.
- Run each workflow on a GitHub-hosted runner. Never use `self-hosted`: a fork PR of a public
  repository can run code on a self-hosted runner.

## 7. Tool Calls

Before a tool call that needs user permission, write a one-line summary of the call.
The summary must tell what the call does and what it changes.
Write the summary in the message text, not only in the tool description.

## 8. Private Data

This repository is public, or it can become public. Git history is permanent
([ADR-0001](decisions/0001-decision-log-agents-md-and-private-data.md)).
The rule has no exemption. No folder may hold host values.
Do not write these in a tracked file, a commit message or a PR body:

- a credential, a token, a password or a private key;
- an absolute path in a user folder;
- a hostname, a domain or a user name;
- an email address that is not on the allowlist of `tools/check_private_data.py`;
- a private URL, or an IP address that is not a documentation address;
- a raw dump of `env`, `pip list`, `docker inspect` or `op item get`.

In prose and examples, use a documentation address (`192.0.2.0/24`) or name the variable.
Use paths relative to the repository, for example `decisions/README.md`.
Give a measurement as a summary with its tool and its version.
Text from `plans/` must obey these rules before it goes into a tracked file.
If you find private data in a tracked file, remove it with a redaction edit.
Then tell the user, because git history keeps the data.
Also revoke a leaked credential.

`uv run pytest tools/tests` runs `tools/check_private_data.py`.
To also block a hostname or a user name, put it in the file `.private-terms` in the repository root.
Git ignores that file. Do not commit it.
The pre-commit hook runs `gitleaks` and the private-data check.
The pre-push hook runs the collision check of the decision-log IDs.
The commit-msg hook runs `tools/check_ai_attribution.py`. It warns about AI attribution
([section 6](#6-git-rules)). It does not stop the commit.
If you are an AI agent and you see this warning, tell the user.
`.github/workflows/secrets.yml` runs `gitleaks` on each push and PR.
`.gitleaks.toml` holds the reviewed false positives.
Turn on secret scanning and push protection for a private repository on the day that it becomes
public.
