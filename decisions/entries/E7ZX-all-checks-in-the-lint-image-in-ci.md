# E7ZX — In CI, all checks run in the lint image; on the controller, the uv venv stays

**Status:** proposed, 2026-11-04 (agent).

Supersedes [ADR-NXK2](NXK2-current-decision-log-kit.md) in full. Its mirror is site ADR-C7J4.

## Decision

These rules replace rule 17 of NXK2:

1. **CI in the image.** In CI, each check runs in the lint image that `tools/lint/Dockerfile`
   builds: `ansible-lint`, the role checks, `yamllint`, `shellcheck` and the doc checks. The
   gitleaks scan stays as it is. A site builds the same image from its `framework/` submodule.
2. **The controller.** Do not build a Docker image to run a tool that runs on Windows. On the
   Windows controller, the doc checks, `yamllint`, `shellcheck` and the hooks run from the uv venv.
   Only `ansible-lint` and the role checks run in the lint container.
3. **One Python.** The `FROM python:<version>` line of `tools/lint/Dockerfile` is the one Python
   version that gates a merge. A workflow must not set `python-version`. `requires-python` is only
   the lower bound of the controller venv. The `ansible` group pins Ansible once, in `uv.lock`.
4. **Updates.** Dependabot `docker` bumps the `FROM` lines of the lint image, minor versions
   included, with no patch-only `ignore`. Dependabot `uv` bumps `uv.lock`. CI runs each check on
   the new versions before a human merges.
5. **Image tag.** `IMAGE` is a hash of `tools/lint/Dockerfile`, `pyproject.toml`, `uv.lock` and
   `requirements.yml`. Do not bump it by hand. After a merged bump, the next run of
   `tools/lint.sh` builds the new image. A site gets the tag from a framework script.

These rules of NXK2 stay. Each link goes to the heading or the tool that states the rule:

6. **Log.** [`AGENTS.md` section 5](../../AGENTS.md#5-decision-log), the
   [Rules](../README.md#rules), [template.md](../template.md) and the docstring of
   [`tools/check_decision_log.py`](../../tools/check_decision_log.py) state the other log rules.
   The Rules keep only the rules that no other absorb document states. Do not use the
   `Refs ADR-NNNN` form.
7. **Instructions.** [Section 1](../../AGENTS.md#1-purpose) and
   [section 2](../../AGENTS.md#2-skills) state `AGENTS.md`, `CLAUDE.md` and the skills. Git tracks
   `.claude/skills/` and ignores the rest of `.claude/`.
8. **Git and private data.** [Section 6](../../AGENTS.md#6-git-rules) states `plans/`, the
   GitHub-hosted runners and no AI attribution. [Section 8](../../AGENTS.md#8-private-data) states
   the private-data rule, with no exemption, and the commit-msg warning. The warning does not stop a
   commit.
9. **Links.** `tools/check_links.py` checks each `AGENTS.md`, each `decisions` folder, `docs/`,
   `notes/`, `roles/` and `.claude/skills/`. A GitHub link must pin a full SHA, except in `docs/`
   and `roles/`.

## Reason

- PR #1 (`python:3.13.17-slim` to `3.15.0-slim`) passed CI and tested nothing. CI ran from the uv
  venv on Python 3.13, and it never built the image. Four Python pins disagree.
- NXK2 rejected Docker in CI. Then CI never tests the Python of the image.
- A manual `IMAGE` bump is easy to forget, and the controller then keeps the old image.
- The reasons of NXK2 for the rules that stay are still true.

## Consequences

- On acceptance, NXK2 becomes `superseded by E7ZX`, and its row moves to
  [historical.md](../historical.md). The live citations of NXK2 change to this entry. Decided
  entries keep theirs.
- `AGENTS.md` section 3 replaces the manual `IMAGE` bump and the CI sentence.
- `tools/lint.sh` reads `IMAGE` from a new `tools/lint/image-tag.sh`. A new `tools/lint/ci.sh` runs
  all checks in the image. It syncs the `dev` group of the checked repo into a second venv and sets
  `UV_NO_SYNC=1`, so `/opt/lint` keeps the locked `ansible` group.
- The Dockerfile sets `safe.directory` for `/repo`. It copies uv from a `FROM ... AS uv` stage,
  because Dependabot does not read `COPY --from`.
- `lint.yml` builds the image and runs `ci.sh`. `doc-checks.yml` goes.
- `dependabot.yml` adds a `uv` entry.
- PR #1 needs a rebase.
- The site changes after the framework is public (site ADR-C7J4).

## Evidence

- Pins: `tools/lint/Dockerfile:7` `3.13.17`, `lint.yml:25` `"3.13"`, `doc-checks.yml:22` `"3.12"`,
  `pyproject.toml:7` `>=3.12`.
- Dependabot `docker` reads only `FROM` lines (`FROM_LINE`). `github_actions` reads only `uses`,
  not `python-version`. `uv` reads `.python-version` only as the resolver Python:
  <https://github.com/dependabot/dependabot-core/blob/eda07d97d87762779406f5a5beec86fec139e78f/docker/lib/dependabot/docker/file_parser.rb>,
  <https://github.com/dependabot/dependabot-core/blob/eda07d97d87762779406f5a5beec86fec139e78f/github_actions/lib/dependabot/github_actions/file_parser.rb>,
  <https://github.com/dependabot/dependabot-core/blob/eda07d97d87762779406f5a5beec86fec139e78f/uv/lib/dependabot/uv/file_parser/python_requirement_parser.rb>.
- Dependabot supports `uv`:
  <https://github.blog/changelog/2025-03-13-dependabot-version-updates-now-support-uv-in-general-availability/>.

## Alternatives rejected

- **All checks in Docker on the controller too.** Each commit needs Docker Desktop, and
  `pre-commit` is a Python tool, so uv stays.
- **`.python-version`, a patch-only ignore and a drift test.** Dependabot cannot bump
  `.python-version` or a `python-version` input, so it proposes no minor release.
- **Build and test the image only when its inputs change.** Two Pythons still gate a merge.
- **Keep NXK2.** A Python bump merges untested.
- **Keep the full Rules.** Most of them repeat a tool or `AGENTS.md`, and two copies drift.

## Not repeated

- Do not add rules to `CLAUDE.md`. Add them to `AGENTS.md`.
- Do not run Ansible natively on the Windows controller. It fails at start.
