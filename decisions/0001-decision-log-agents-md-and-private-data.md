# 0001 — Decision log, `AGENTS.md`, `plans/` and private data

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-25 (user).

## Decision

1. **Decision log.** This repo keeps its decisions in `decisions/`. The [index](README.md) has
   the Active and Proposed tables and the rules. [`historical.md`](historical.md) has the
   Historical table. [`template.md`](template.md) has the entry template.
   [`open-work.md`](open-work.md) has the open work. A decision that code or a document refers to
   must be in an entry.
2. **Own IDs.** This log starts at 0001. Its IDs are independent of the site log. Entries 0001 to
   0005 keep their numbers. Each new entry gets a random ID from `tools/check_decision_log.py --new`.
3. **Citation form.** In this repo, `ADR-XXXX` and a bare ID are always entries of this log. A site
   entry is cited as `site XXXX`, with no link. No file links to the site repository or names its
   location.
4. **Restate only when cited.** A site rule becomes an entry of this log only when framework code or
   framework documents cite it. The entry restates the rule without site values and supersedes the
   site entry in full. When the site entry also holds site values, a new site entry restates those
   values and supersedes the site entry instead. Then the entry of this log supersedes nothing.
5. **Status.** An agent writes a new entry as `proposed`. Only the user changes it to `accepted` or
   `rejected`.
6. **One instructions file.** [`AGENTS.md`](../AGENTS.md) is the single instructions file for
   coding agents. `CLAUDE.md` only imports it: its full content is `@AGENTS.md`. Do not put
   instructions in `CLAUDE.md` or in a second instructions file. Agent procedures are skills in
   `.claude/skills/`. Git tracks that folder and ignores the rest of `.claude/`.
7. **`plans/`.** `plans/` is a local working folder. Git ignores it. Do not commit it. A tracked file
   does not link to `plans/` and does not cite its sections, item numbers or local PR labels.
8. **Log rules.** The [Rules](README.md#rules) of the index apply: allowed edits only, complete
   supersession, status forms, Proposed entries off the read path, absorption, `done`, consolidation,
   random IDs, permalinks and the size limits. `tools/check_decision_log.py` checks the index, the IDs
   and the limits. The site log must use the same rules, with its own copy of the rules and the
   tools.
9. **Private data.** [`AGENTS.md`](../AGENTS.md#8-private-data) gives the rule. This repo becomes
   public, so the rule has no exemption: no folder may hold host values.
   `tools/check_private_data.py` checks the tracked files. The pre-commit hook and the workflow
   `.github/workflows/secrets.yml` run `gitleaks`. `.private-terms` is a local, untracked list of
   terms to block.
10. **Links.** `tools/check_links.py` checks the relative links and their anchors. A GitHub link in
    `AGENTS.md`, `notes/` or `.claude/skills/` must pin a full SHA.
11. **Doc checks.** `pyproject.toml` holds only the dev tools of the doc checks (`pytest`,
    `pre-commit`). The workflows run on GitHub-hosted runners only.

## Reason

- Plans are working notes for a session. They go out of date, and a clone does not have them. A
  decision that code refers to must be in a tracked file.
- The framework becomes public and the site stays private. One log cannot be in both. Own IDs let
  each log grow without a gap or a collision in the other.
- Two branches can take the same next number. A random ID removes that collision. A random ID starts
  with a letter, so it is never mistaken for a site number.
- A restatement of every site entry would copy site history and site values into a public repo. A
  restatement on demand copies only the rules that framework code needs.
- A link to a private repo fails for each public reader, and its URL names the owner.
- Two instruction files can disagree. The import gives all agents the same text.
- Agents read the log before each task. Without limits and status tables, the part that they read
  grows with each entry, also when the number of rules does not grow.
- A partial supersession makes a reader join two or three entries to find the current rule.
- Git history is permanent. A pasted command output can hold paths, user names and tokens.
- A self-hosted runner on a public repo lets a fork PR run code on that runner.
- A test makes each rule a check that CI runs. A written rule alone does not stop a mistake.

## Consequences

- Each decision costs one entry and one index row.
- A rule that both repos need has one live authority. Until the site log allows a status line that
  names an entry of another repo, an entry of this log cannot supersede a site entry.
- Each entry of this log must be readable without the site log.
- The first `pre-commit` run on a clone downloads Go to build `gitleaks`.

## Alternatives rejected

- **Copy the site series into both repos.** It makes two different entries with the same number,
  and it copies site values into the public repo.
- **Prefixed identifiers for all entries.** A rename of existing site entries breaks the rule that an
  ID never changes without a collision.
- **Sequential numbers for new entries.** Parallel branches take the same number, and git shows no
  conflict.

## Not repeated

- Do not link to the site repository. Write `site XXXX`.
- Do not copy a site value into an entry. Use a documentation address (`192.0.2.0/24`) or name the
  variable.
- Do not link to `plans/` from a tracked file. Link to a decision entry.
- Do not add rules to `CLAUDE.md`. Add them to `AGENTS.md`.
- Do not commit `.private-terms`. A tracked list publishes the terms.

_Edited 2026-10-29 (ADR-NXK2): link repair._
