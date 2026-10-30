# NXK2: where each moved rule is now

Evidence for [ADR-NXK2](../entries/NXK2-current-decision-log-kit.md). The second kit version keeps
only the essential rules in the [Rules](../README.md#rules) of the index. This list gives the new
place of each rule that left the Rules, `decisions/template.md` or section 5 of `AGENTS.md` in
the change of 2026-10-29 that adopts the second kit version. The rules are those of the first
kit version, from the change before it.

"Kept" means that the rule stays in the Rules. "Docstring" means the docstring of
`tools/check_decision_log.py`, which is an absorb document for the rules that the tool checks.
"Intro" means the two paragraphs above `## Index` in `decisions/README.md`.

## Rules of the index

| Rule | Place now |
|---|---|
| One entry for each decision or measurement | [`AGENTS.md` section 5](../../AGENTS.md#5-decision-log) |
| Use `template.md` | Intro |
| The four allowed edits and the `_Edited` line | Kept |
| The list of edit kinds | Kept: the edit names and the `re-ID from XXXX` and `citation repair` lines |
| The edit line names the entry when a change has no PR | Kept |
| A `proposed` entry can change | Kept: the edit rule applies only to an entry that is not `proposed`; `template.md` (Status) |
| An agent writes `proposed`; only the user accepts or rejects | `AGENTS.md` section 5 |
| `recorded again` | Kept |
| To change a decision, add a new entry that supersedes the old entry in full | Intro |
| Do not supersede a part of an entry | Intro ("in full") |
| A link to a heading can restate a rule | Kept |
| The commit that changes a linked heading cites its entry | Kept |
| A change under a linked heading does not supersede the linking entry | Intro |
| A change of a rule that an entry states in its own text supersedes it in full | Intro |
| The allowed status changes, with date and PR | Kept |
| An absorbed entry becomes `superseded by XXXX` | Kept (allowed status change) |
| Change the index row in the same change | Kept |
| The tables and their status forms | Docstring |
| The Status cell holds only a form of its table | Docstring |
| `XXXX` is a decided entry | Docstring |
| The Decision cell limit (160) | Docstring (`DECISION_CELL_LIMIT`) |
| The Section cell of a Proposed row | Docstring |
| `evidence; used by XXXX` | Kept |
| Absorption and the absorb documents | Kept, with the docstring of a tool added |
| `done` | Kept |
| Consolidation entry | Kept |
| Delete a done open-work item | Kept |
| The size limits | Docstring (`INDEX_LIMIT`, `OPEN_WORK_LIMIT`, `ENTRY_LIMIT`, `READ_PATH_LIMIT`) |
| The entry limit leaves out the status line and the `_Edited` lines | Changed: docstring (status paragraph up to `STATUS_EXEMPTION_LIMIT`, strict `_Edited` form) |
| Proposed and Historical entries are not in the read path | Docstring; Intro |
| Long evidence in a tracked file | Kept |
| The tool shows the read path and the 80% warnings; the doc tests run it | Docstring; `AGENTS.md` section 3 |
| CRLF to LF; what the tool checks; a warning does not fail; an entry does not warn | Docstring |
| A PR can lower a limit; a PR that raises a limit adds an entry | Kept |
| The ID alphabet | Docstring |
| A new ID starts with a letter | Changed: docstring (a digit and a letter in any position) |
| Upper-case IDs | `template.md`; `AGENTS.md` section 5; docstring |
| IDs that differ only in case are one ID | Docstring |
| Entries 0001 to 0005 keep their numbers; no new all-digit ID | Docstring |
| The IDs are independent of the site log | Kept |
| `git fetch` before `--new` | `AGENTS.md` section 5 |
| Give the entry the `new:` ID | `AGENTS.md` section 5 |
| Create the file immediately; the index row at the end of its table, in the same change | `AGENTS.md` section 5 |
| The pre-push hook and the collision verdicts | Docstring |
| An ID changes only on a `re-ID:` line | Kept |
| Rename the file, the heading and the index row on a re-ID; repair the citations | Docstring; Kept (edit rule) |
| Ask the user before a PR title or body change | [`AGENTS.md` section 6](../../AGENTS.md#6-git-rules) |
| The re-ID and citation-repair lines only on an entry on `main` | Kept |
| Do not reuse an ID; no two index rows with one ID | Docstring |
| What a tool is; what a script is; where each one goes | `AGENTS.md` section 5 |
| Cite a tracked file with a relative link; a commit with a full-SHA permalink | `AGENTS.md` section 5; `tools/check_links.py` |
| Do not cite or link `plans/` | `AGENTS.md` section 6 |
| Until a commit is on `main`, cite its PR | Kept |
| Cite an entry as a link with `ADR-<ID>`, in upper case, in each text | `AGENTS.md` section 5 |
| The repo name before the ID of another repo; a permalink for a public repo | `AGENTS.md` section 5 |
| A bare ID is an entry of this log | Kept |
| No prefix in a file name, a heading, an index row, a status line or a YAML value | Kept |
| The commit subject ends with `(ADR-<ID>)`; the commit body has no link | `AGENTS.md` section 5 |
| An ID in YAML is in quotes | Kept |
| A provisional entry of another repo | Kept |
| Cite a site entry with no link; never link or name the site repository | Changed: `AGENTS.md` section 5 (`site ADR-<ID>`) |
| Restate a site rule only when framework code or documents cite it | `AGENTS.md` section 5 |
| The split of a site entry with generic rules and site values | Kept |
| The `**Depends on:**` line | `template.md`; Kept (no permalink for a site entry) |
| The mirror rule | Kept, with the `site ADR-<ID>` citation of the mirror entry |
| The public repo and the private-data rule | [`AGENTS.md` section 8](../../AGENTS.md#8-private-data) |
| ASD-STE100 | `AGENTS.md`, first paragraph |

## `template.md`

`template.md` is now a plain copy of the kit template.

| Rule | Place now |
|---|---|
| The `Supersedes site XXXX in full.` line | Kept (split rule) |
| The Supersedes bullet: the status line of the old entry records a supersession in this log | Kept (split rule) |
| The source can be `agent` | `AGENTS.md` section 5 (an agent writes `proposed`) |
| A `**Depends on:**` permalink only for a public repo; no link for a site entry | Kept; `AGENTS.md` section 5 |
| The script of an entry in the `scripts/` folder of the log | `template.md`; `AGENTS.md` section 5 (`decisions/scripts/`) |
| Cite upstream docs or code for each claim | Kept |

## Section 5 of `AGENTS.md`

| Rule | Place now |
|---|---|
| The log records decisions and their evidence; read the Active entries; Proposed and Historical | Intro |
| A random upper-case ID of 4 characters | Docstring |
| The pre-push hook runs `--collisions` and stops the push | Docstring; `.pre-commit-config.yaml` |
| Act on each `re-ID:` line; do not change an ID for a different reason | Kept |
| No two index rows with one ID in a merge | Docstring |
| The allowed edits and the edit line | Kept |
| A new entry supersedes in full; a link can restate a rule; no partial supersession | Intro; Kept |
| Keep the log inside its limits | Docstring; `AGENTS.md` section 3 |
| No dated status lines in `AGENTS.md` | Kept |
| An ID without a repo name is an entry of this repo | Kept |
| Do not import a file, a test or a tool from another repo | Kept (mirror rule) |

## Section 8 of `AGENTS.md`

The section keeps each rule as a list item. These sentences moved:

| Rule | Place now |
|---|---|
| `uv run pytest tools/tests` runs the private-data check | `AGENTS.md` section 3 |
| The pre-push hook runs the collision check | Docstring |
| The commit-msg hook runs `tools/check_ai_attribution.py` and does not stop the commit | The docstring of `tools/check_ai_attribution.py` |
| `.github/workflows/secrets.yml` runs `gitleaks` | `AGENTS.md` section 8 ("CI runs `gitleaks`") |
