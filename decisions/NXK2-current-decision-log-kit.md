# NXK2 — The current decision-log kit, and linters in a uv venv

**Status:** proposed, 2026-10-29 (agent).

Supersedes [ADR-0001](0001-decision-log-agents-md-and-private-data.md) in full. Its mirror is site EB4N.

## Decision

These rules of 0001 stay:

1. **Own IDs.** The IDs of this log are independent of the site log. Entries 0001 to 0005 keep their
   numbers. Each new entry gets a random ID from `tools/check_decision_log.py --new`.
2. **Site entries.** Cite a site entry as `site XXXX`, with no link. No file links to the site
   repository or names its location. A site rule becomes an entry of this log only when framework
   code or framework documents cite it. The entry restates the rule without site values and
   supersedes the site entry in full. When the site entry also holds site values, a new site entry
   restates those values and supersedes the site entry instead.
3. **Status.** An agent writes a new entry as `proposed`. Only the user changes it to `accepted` or
   `rejected`.
4. **One instructions file.** [`AGENTS.md`](../AGENTS.md) is the single instructions file for
   coding agents. `CLAUDE.md` only imports it: its full content is `@AGENTS.md`. Agent procedures
   are skills in `.claude/skills/`. Git tracks that folder and ignores the rest of `.claude/`.
5. **`plans/`.** `plans/` is a local working folder. Git ignores it. A tracked file does not link to
   `plans/` and does not cite its sections, item numbers or local PR labels.
6. **Private data.** [`AGENTS.md` section 8](../AGENTS.md#8-private-data) states the rule. It has
   no exemption: no folder may hold host values.
7. **Runners.** [`AGENTS.md` section 6](../AGENTS.md#6-git-rules) states the rule: each workflow
   runs on a GitHub-hosted runner.
8. **Log rules.** The [Rules](README.md#rules) of the index and [template.md](template.md) state
   the other rules. The site log uses the same rules, with its own copy of the rules and the tools.

These rules change:

9. **Kit rules.** The Rules take the current kit rules. A link to a heading of a normative document
   can restate a rule. A changed proposed entry adds `recorded again` to its status line. An absorbed
   entry can become `superseded by XXXX`. The `XXXX` of a status must be a decided entry. Each tool
   is in `tools/` and has tests. Until a commit is on `main`, cite its PR. When a change has no PR,
   the edit line names the entry that caused it.
10. **Folder.** The log moves from `notes/` to `decisions/` at the repo root, with its history. A
    script of an entry goes in `decisions/scripts/`. `OLD_LOG_DIRS` in `tools/check_decision_log.py`
    names the old folder, so `--new` still reads it on old branches.
11. **Upper-case IDs.** A new ID uses upper-case Crockford base32. The ten lower-case IDs of this log
    change to upper case. IDs that differ only in case are one ID.
12. **Citations.** Cite an entry as a Markdown link with `ADR-<ID>` as the link text, in each text
    that an agent writes. A commit subject that adds or changes an entry ends with `(ADR-<ID>)`. A
    commit body writes `ADR-<ID>` with no link. The `Refs ADR-NNNN` form is not used.
13. **No AI attribution.** A commit or a PR has no AI attribution, for example a `Co-Authored-By:`
    trailer. `tools/check_ai_attribution.py` runs in the commit-msg hook. It warns and does not stop
    the commit.
14. **Links.** `tools/check_links.py` checks the files that git keeps: each `AGENTS.md`, each
    `decisions` folder, `docs/`, `notes/`, `roles/` and `.claude/skills/`. A GitHub link must pin a
    full SHA, except in `docs/` and `roles/`.
15. **Entry limit.** The limit of an entry does not count its status line and its `_Edited` lines.
    The kit counts the full file. The site log must use the same rule.
16. **Linters.** Do not build a Docker image to run a tool that runs on Windows. The doc checks,
    `yamllint` and `shellcheck` run from the uv venv. Ansible runs only on Linux, so on the Windows
    controller `ansible-lint` and the role checks run in the lint container. In CI they run from the
    uv venv, with no Docker. The `ansible` dependency group of `pyproject.toml` pins ansible-core and
    `ansible-lint` once, in `uv.lock`. The image installs that locked group. A plain `uv sync` does
    not install it.
17. **No modules.** This repo has no modules, so the Rules leave out the module rules of the kit.

## Reason

- The user decided on 2026-10-29 to adopt the current version of the decision-log kit, in this repo
  and in the site repo.
- An upper-case ID does not look like a word in prose or in `git log`. `git log` shows no links,
  and `ADR-` marks the ID there.
- A restatement by a link keeps an entry short, and the linked heading stays the one source.
- Agents add AI attribution by default. A hook makes the rule visible at commit time.
- A Docker image for a tool that runs on Windows adds a build, a daemon and a second copy of the
  versions. One lock gives the same versions to the controller, the image and CI.
- The status line and the edit lines grow after the decision, and a decided body cannot become
  shorter. Without rule 15, the re-ID of a long entry fails the check.

## Consequences

- Acceptance changes the status of 0001 to `superseded by NXK2`, and moves its row to
  [historical.md](historical.md). Then the citations of 0001 in `AGENTS.md` change to this entry.
- The site log needs a matching change (site EB4N).
- A branch made before the move has its entries in the old folder under `notes/`.
- A change of the `ansible` group in `uv.lock` or of `requirements.yml` needs a new `IMAGE` tag.

## Alternatives rejected

- **Keep the lower-case IDs.** Two case forms in one log are hard to read and to search.
- **Run Docker in CI.** A GitHub-hosted Linux runner runs Ansible from the uv venv.

## Not repeated

- Do not add rules to `CLAUDE.md`. Add them to `AGENTS.md`.
- Do not commit `.private-terms`. A tracked list publishes the terms.
- Do not run Ansible natively on the Windows controller. It fails at start.
