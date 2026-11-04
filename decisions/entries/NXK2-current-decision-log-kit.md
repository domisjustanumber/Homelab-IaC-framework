# NXK2 — The current decision-log kit, and linters in a uv venv

**Status:** proposed, 2026-10-29 (agent); recorded again 2026-10-29 (user: the second kit version); accepted, 2026-10-29 (user); superseded by [E7ZX](E7ZX-all-checks-in-the-lint-image-in-ci.md), 2026-11-04 (E7ZX).

Supersedes [ADR-0001](0001-decision-log-agents-md-and-private-data.md) in full. Its mirror is
site ADR-EB4N.

## Decision

These rules of 0001 stay:

1. **Own IDs.** The IDs of this log are independent of the site log. Entries 0001 to 0005 keep their
   numbers. Each new entry gets a random ID from `tools/check_decision_log.py --new`.
2. **Site entries.** No file links to the site repository or names its location. A site rule
   becomes an entry of this log only when framework code or framework documents cite it. The entry
   restates the rule without site values and supersedes the site entry in full. When the site entry
   also holds site values, a new site entry restates those values and supersedes the site entry
   instead.
3. **Status.** An agent writes a new entry as `proposed`. Only the user changes it to `accepted` or
   `rejected`.
4. **One instructions file.** [`AGENTS.md`](../../AGENTS.md) is the single instructions file for
   coding agents. `CLAUDE.md` only imports it: its full content is `@AGENTS.md`. Agent procedures
   are skills in `.claude/skills/`. Git tracks that folder and ignores the rest of `.claude/`.
5. **`plans/`.** [`AGENTS.md` section 6](../../AGENTS.md#6-git-rules) states the rule.
6. **Private data.** [`AGENTS.md` section 8](../../AGENTS.md#8-private-data) states the rule. It
   has no exemption: no folder may hold host values.
7. **Runners.** `AGENTS.md` section 6 states the rule: each workflow runs on a GitHub-hosted runner.
8. **Log rules.** The [Rules](../README.md#rules) of the index, [template.md](../template.md),
   [`AGENTS.md` section 5](../../AGENTS.md#5-decision-log) and the docstring of
   `tools/check_decision_log.py` state the other rules. The site log uses the same rules, with its
   own copy of the rules and the tools.

These rules change:

9. **Essential Rules.** The Rules keep only the rules that no other absorb document states. The
   docstring of a tool is an absorb document for the rules that the tool checks.
   [The cut list](../evidence/NXK2-rules-cut-list.md) gives the new place of each moved rule.
10. **Folder.** The log is in `decisions/` at the repo root. Each entry file is in
    `decisions/entries/`, and an index row links `entries/<ID>-<slug>.md`. A script of an entry goes
    in `decisions/scripts/`. `OLD_LOG_DIRS` names the old folder under `notes/`, so `--new` still
    reads old branches, also in the flat layout.
11. **IDs.** A new ID uses upper-case Crockford base32. It has at least one digit and at least one
    letter, in any position, and it does not read as a number such as `1E23`. The older IDs stay
    valid. The ten lower-case IDs of this log change to upper case.
12. **Citations.** Cite an entry of this log as a Markdown link with `ADR-<ID>` as the link text,
    in each text that an agent writes. Cite a site entry as `site ADR-<ID>`, with no link. Older
    text with `site XXXX` stays valid. A status line holds the bare ID. A commit subject that adds or
    changes an entry ends with `(ADR-<ID>)`. The `Refs ADR-NNNN` form is not used.
13. **No AI attribution.** A commit or a PR has no AI attribution. `tools/check_ai_attribution.py`
    runs in the commit-msg hook. It warns and does not stop the commit.
14. **Links.** `tools/check_links.py` checks the files that git keeps: each `AGENTS.md`, each
    `decisions` folder, `docs/`, `notes/`, `roles/` and `.claude/skills/`. A GitHub link must pin a
    full SHA, except in `docs/` and `roles/`.
15. **Entry limit.** The limit of an entry does not count its status paragraph, up to
    `STATUS_EXEMPTION_LIMIT` characters, and its `_Edited YYYY-MM-DD (<PR>): <kind>._` lines.
16. **Edit lines.** A `re-ID from XXXX` or `citation repair` line goes only on an entry that is on
    `main`. All entries of this log are on `main`, so the lines of the upper-case re-ID stay.
17. **Linters.** Do not build a Docker image to run a tool that runs on Windows. The doc checks,
    `yamllint` and `shellcheck` run from the uv venv. On the Windows controller, `ansible-lint` and
    the role checks run in the lint container. In CI they run from the uv venv, with no Docker. The
    `ansible` group of `pyproject.toml` pins Ansible once, in `uv.lock`.
18. **No modules.** This repo has no modules, so it leaves out the module rules of the kit.

## Reason

- The user decided on 2026-10-29 to adopt the current version of the decision-log kit, in this repo
  and in the site repo.
- Short Rules keep the read path small. A rule that a tool checks has one source: the tool.
- An `entries/` folder keeps the index files apart from the entries.
- An ID with a digit and a letter does not look like a word in prose or in `git log`.
- The `site ADR-` form marks a site entry in prose, and it does not link the site.
- A re-ID line on an entry that is not on `main` records an ID that nobody saw.
- The status paragraph and the edit lines grow after the decision, and a decided body cannot become
  shorter.
- A Docker image for a tool that runs on Windows adds a build and a second copy of the versions.

## Consequences

- Acceptance changes the status of 0001 to `superseded by NXK2`, and moves its row to
  [historical.md](../historical.md). Then the citations of 0001 in `AGENTS.md` change to this entry.
- The site log needs a matching change (site ADR-EB4N).
- A branch made before the move has its entries in the old folder under `notes/`.
- The comments of the role templates name the new path, so the next run of a role writes each
  changed template once.

## Alternatives rejected

- **Keep the full Rules.** Most of them repeat a tool or `AGENTS.md`, and two copies drift.
- **Run Docker in CI.** A GitHub-hosted Linux runner runs Ansible from the uv venv.

## Not repeated

- Do not add rules to `CLAUDE.md`. Add them to `AGENTS.md`.
- Do not run Ansible natively on the Windows controller. It fails at start.
