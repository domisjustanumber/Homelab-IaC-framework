# 3EV6 — Renovate proposes each version bump; Dependabot goes

**Status:** proposed, 2026-11-17 (agent); accepted, 2026-11-17 (user).

Supersedes [ADR-E7ZX](E7ZX-all-checks-in-the-lint-image-in-ci.md) in full. Its mirror is site
ADR-HD03.

## Decision

These rules replace rule 4 of E7ZX:

1. **One bot.** Renovate proposes each version bump of this repo as a PR. It replaces Dependabot.
   `.github/dependabot.yml` goes.
2. **What it bumps.** The `FROM` lines of `tools/lint/Dockerfile`, minor versions included, with no
   patch-only rule. `uv.lock`. The actions in `.github/workflows/`. A regex manager bumps each
   binary that a role pins in its `defaults/main.yml`: the version and its sha256 when upstream
   publishes a checksum file, or else the version only.
3. **Install check.** A role that pins a version only checks the upstream signature of the download
   at install time. A role that pins a sha256 checks the sha256.
4. **Config.** `renovate.json` in the repo root extends `config:recommended`, with a weekly
   schedule and the Dependency Dashboard. Each update is its own PR. Renovate merges nothing until
   an entry allows it.
5. **Where it runs.** This repo holds no Renovate workflow and no Renovate token. A Renovate run
   outside this repo applies `renovate.json`. CI runs each check on the new versions before a human
   merges.

These rules of E7ZX stay:

6. **CI in the image, the controller, one Python, the image tag.**
   [`AGENTS.md` section 3](../../AGENTS.md#3-install-and-test) states rules 1, 2, 3 and 5 of E7ZX.
7. **Log.** [`AGENTS.md` section 5](../../AGENTS.md#5-decision-log), the
   [Rules](../README.md#rules), [template.md](../template.md) and the docstring of
   [`tools/check_decision_log.py`](../../tools/check_decision_log.py) state the other log rules.
   Do not use the `Refs ADR-NNNN` form.
8. **Instructions.** [Section 1](../../AGENTS.md#1-purpose) and
   [section 2](../../AGENTS.md#2-skills) state `AGENTS.md`, `CLAUDE.md` and the skills. Git tracks
   `.claude/skills/` and ignores the rest of `.claude/`.
9. **Git and private data.** [Section 6](../../AGENTS.md#6-git-rules) and
   [section 8](../../AGENTS.md#8-private-data) state `plans/`, the GitHub-hosted runners, no AI
   attribution, the private-data rule and the commit-msg warning.
10. **Links.** `tools/check_links.py` checks each `AGENTS.md`, each `decisions` folder, `docs/`,
    `notes/`, `roles/` and `.claude/skills/`. A GitHub link must pin a full SHA, except in `docs/`
    and `roles/`.

## Reason

- Dependabot has no regex or generic updater. It cannot bump a binary that a role pins. Its
  `opentofu` ecosystem bumps only modules and providers.
- Renovate covers each Dependabot job of this repo, so one bot is enough. Two bots on one
  dependency open two PRs.
- Renovate can bump a version and the sha256 next to it.
- The reasons of E7ZX for the rules that stay are still true.

## Consequences

- On acceptance, E7ZX becomes `superseded by 3EV6`, and its row moves to
  [historical.md](../historical.md). The live citations of E7ZX change to this entry. Decided
  entries keep theirs.
- `AGENTS.md` section 3 replaces the Dependabot sentence.
- The CI change adds `renovate.json` and deletes `.github/dependabot.yml`. The open Dependabot PRs
  close, and Renovate opens them again. The Python 3.15 PR comes back red, until an ansible-core
  release supports Python 3.15.
- The regex managers come with the first role that pins a binary.
- A site must run Renovate for this repo. Site ADR-HD03 states how this site does it.

## Evidence

- Dependabot ecosystems, with no generic updater:
  <https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories>.
- The Renovate regex manager captures `currentValue` and `currentDigest`:
  <https://docs.renovatebot.com/modules/manager/regex/>.
- `github-release-attachments` reads the new digest from a small checksum asset:
  <https://github.com/renovatebot/renovate/blob/64fe4b3debb8b9f1fb64de323f7bdf780b2665dc/lib/modules/datasource/github-release-attachments/index.ts>.
  `tofu_1.13.9_SHA256SUMS` is 3,734 bytes (GitHub API, 2026-11-17).
- Renovate updates `uv.lock` with the `pep621` manager, and git submodules with an opt-in manager:
  <https://docs.renovatebot.com/modules/manager/pep621/>,
  <https://docs.renovatebot.com/modules/manager/git-submodules/>.
- 1Password publishes no checksum for the `op` download:
  <https://www.1password.dev/cli/install-server/>.

## Alternatives rejected

- **Dependabot and a Dockerfile that only holds versions.** It is an odd file, and tofu then has
  no sha256 pin.
- **Renovate for the role binaries only.** Two bots and two configs.
- **Hand bumps.** A bump is easy to forget.

## Not repeated

- Do not set `python-version` in a workflow to steer Renovate. The `FROM` line gates a merge.
