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
| `tools/` | The doc checks: `check_decision_log.py`, `check_links.py`, `check_private_data.py` and `check_ai_attribution.py`. Their tests are in `tools/tests/`. The lint suite: `lint.sh`, and the lint container in `lint/`, with its tag script `lint/image-tag.sh` and its CI script `lint/ci.sh`. `tools/tests/` also tests the file checks of `lint/check_roles.py`. |
| `pyproject.toml`, `uv.lock` | The dev tools (`pytest`, `pre-commit`, `yamllint`, `shellcheck`) and the `ansible` group of the lint container |
| `.github/workflows/` | All checks in the lint image (`lint.yml`) and the secret scan (`secrets.yml`) in CI |
| `plans/` | A local working folder. Git ignores it. |

## 2. Skills

Load the skill that matches the task.
If your agent does not support skills, read the file `.claude/skills/<skill>/SKILL.md`.
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

On the Windows controller, do not build a Docker image to run a tool that runs on Windows.
Run it from the uv venv with `uv run`.
On the Windows controller, the doc checks, `yamllint`, `shellcheck` and the hooks run from the uv
venv ([ADR-E7ZX](decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md)).
Ansible runs only on Linux.
Do not run `uv run ansible-*` on the Windows controller.
On the Windows controller, the Ansible checks run in the pinned lint container:

```sh
tools/lint.sh                      # yamllint and shellcheck, then ansible-lint and the role checks
tools/lint.sh ansible-lint roles/base
```

`tools/lint.sh` runs `yamllint` and `shellcheck` from the uv venv first.
Then it runs the Ansible checks in the container.
If Docker is not running, `tools/lint.sh` stops with a message.
Then ask the user to start Docker.
`tools/lint.sh <cmd> [args]` runs one command in the container.
The `ansible` dependency group of `pyproject.toml` pins ansible-core and `ansible-lint`, in
`uv.lock`.
A plain `uv sync` does not install that group.
The image (`tools/lint/Dockerfile`) installs the locked `ansible` group and the collections from
`requirements.yml`.
The image tag is a hash of `tools/lint/Dockerfile`, `pyproject.toml`, `uv.lock` and
`requirements.yml`.
`tools/lint/image-tag.sh` prints it.
Do not bump the tag by hand.
After a change of these files, the next run of `tools/lint.sh` builds the new image.
A site builds the same image from its `framework/` submodule.
The site gets the tag from `framework/tools/lint/image-tag.sh`.

In CI, `.github/workflows/lint.yml` builds the image and runs `tools/lint/ci.sh` in it.
`ci.sh` runs all checks: `yamllint`, `shellcheck`, the doc checks, `ansible-lint` and the role
checks.
It syncs the `dev` group of `uv.lock` into a second venv, on the Python of the image.
A site runs `framework/tools/lint/ci.sh` in its own checkout.
The `FROM python:<version>` line of `tools/lint/Dockerfile` is the one Python version that gates
a merge.
A workflow must not set `python-version`.
`requires-python` is only the lower bound of the controller venv.
Dependabot bumps the `FROM` lines and `uv.lock`.
CI then runs each check on the new versions.

Run `uv run pytest` and `tools/lint.sh`.
These checks must pass.
Run `uv run pytest tools/tests` to run only the doc checks.
The doc checks test the decision log, the relative links, the private-data rule and the
AI-attribution check.
They also test the file checks of `tools/lint/check_roles.py`, with a fake for the Ansible run.
Report each new test failure to the user.
Fix the failures of one root cause in one PR.

## 4. Project Rules

Each role follows [ADR-NTK9](decisions/entries/NTK9-generic-roles-and-host-values.md).
A role holds no host value.
A role reads each value from the inventory of the site or from its `defaults/main.yml`.
Each role lists its required values and its opt-in values in `vars/main.yml`.
`tools/lint/check_roles.py` tests these lists.
Add a `# See ADR-XXXX` comment where a line exists because of a decision, with the path of the entry.
In a template that a role writes to a host, write the ID only, for example `# See ADR-CVM2`
([ADR-SAB7](decisions/entries/SAB7-host-templates-cite-decisions-by-id.md)).
The rules for playbooks, modules and stacks are not written yet.
Do not invent them. Ask the user.
Do not change code that your task does not need.

## 5. Decision Log

Read [`decisions/README.md`](decisions/README.md) and
[`open-work.md`](decisions/open-work.md) before you change a role, a playbook, a module, a stack or
these instructions.
This repository has no modules, so it has one log, in `decisions/`.
The log has a `README.md` with an Active table, a Proposed table and `## Open work`, a
`historical.md`, an `open-work.md`, `template.md` and its entry files in `entries/`.
Each entry goes in `decisions/entries/`.
A tool is code that a test, a hook, a CI job, a skill or a workflow step runs, or code that writes a
tracked file. It is in `tools/`. It has tests.
A script made the evidence for an entry or did its one-off job, and the entry names it. It is in
`decisions/scripts/`. Its own tests, if any, are in `decisions/scripts/tests/`.
A script does not change after its entry is decided. When a step starts to run it, move it to
`tools/` and add a test.
The [Rules](decisions/README.md#rules) of the index give the allowed edits, the status changes and
the rules that no tool checks. `tools/check_decision_log.py` checks the tables, the IDs and the
limits.
Add one entry for each new decision or measurement.
Write a new entry as `proposed`.
Only the user changes an entry to `accepted` or `rejected`.
Before you add an entry, run `git fetch` when you can.
Get its ID from `uv run python tools/check_decision_log.py --new`.
Create the entry file immediately.
Add its index row at the end of the table for its status, in the same change.
End each commit subject that adds or changes an entry with `(ADR-<ID>)`.
Cite each entry as a Markdown link with `ADR-<ID>` as the link text, in upper case, for example
[ADR-E7ZX](decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md).
This rule applies to each text that you write: a tracked file, a plan, a PR body and a reply to the
user. In a reply or a plan, the path is relative to the repository root or to the file.
A commit message cannot hold a working link. In the commit body, write `ADR-<ID>` with no link.
Cite a tracked file with a relative link.
Cite a commit, or the code of another public repository, with a GitHub permalink that pins a full
SHA on the default branch of that repository.
Cite an entry of the site log with the repository name and `ADR-<ID>`, for example
`site ADR-0013`, with no link.
Never link to the site repository, and never name its location.
Older text that cites a site entry as `site 0013` stays valid.
Cite an entry of another public repository with the repository name and `ADR-<ID>`. Also link it
with a full-SHA permalink when the entry is on the default branch of that repository
(see the [Rules](decisions/README.md#rules)).
Restate a site rule here only when framework code or framework documents cite it.

## 6. Git Rules

- `plans/` is a local working folder. Git ignores it. Do not commit it. Do not cite or link to
  `plans/`, or cite the content of a plan
  ([ADR-E7ZX](decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md)).
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
([ADR-E7ZX](decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md)).
The rule has no exemption. No folder may hold host values.
Do not write these in a tracked file, a commit message or a PR body:

- a credential, a token, a password or a private key;
- an absolute path in a user folder;
- a hostname, a domain or a user name;
- an email address that is not on the allowlist of `tools/check_private_data.py`;
- a private URL, or an IP address that is not a documentation address;
- a raw dump of `env`, `pip list`, `docker inspect` or `op item get`.

- In prose and examples, use a documentation address (`192.0.2.0/24`) or name the variable.
- Use paths relative to the repository, for example `decisions/README.md`.
- Give a measurement as a summary with its tool and its version.
- A report field or a test fake can contain a hostname. In this repo, it must be an invented name,
  for example `myhost`.
- Text from `plans/` must obey these rules before it goes into a tracked file.
- To also block a hostname or a user name, put it in `.private-terms` in the repository root. Git
  ignores that file. Do not commit it.
- If you find private data in a tracked file, remove it with a redaction edit. Then tell the user,
  because git history keeps the data. Also revoke a leaked credential.
- The pre-commit hook runs `gitleaks` and `tools/check_private_data.py`. CI runs `gitleaks` on each
  push and PR. `.gitleaks.toml` holds the reviewed false positives.
- The commit-msg hook warns about AI attribution. If you are an AI agent and you see
  this warning, tell the user.
- Turn on secret scanning and push protection for a private repository on the day that it becomes
  public.
