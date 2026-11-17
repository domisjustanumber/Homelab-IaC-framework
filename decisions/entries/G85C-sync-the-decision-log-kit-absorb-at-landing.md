# G85C — Sync the decision-log kit: absorb at landing, restate by link, one link for each heading

**Status:** proposed, 2026-11-17 (agent); accepted, 2026-11-17 (user); absorbed into [Decision log](../README.md#decision-log), [Rules](../README.md#rules), [template](../template.md#decision-log-entry-template), [`AGENTS.md` §6](../../AGENTS.md#6-git-rules), `tools/check_decision_log.py`, 2026-11-17 (G85C).

Its mirror is site ADR-7XGS. This entry supersedes no entry.
[ADR-E7ZX](E7ZX-all-checks-in-the-lint-image-in-ci.md) states the log rules only by links to the
[Rules](../README.md#rules) and to the docstring of
[`tools/check_decision_log.py`](../../tools/check_decision_log.py), so a change under them does not
supersede it.

## Decision

The framework takes the current version of the decision-log kit. The kit adds these rules:

1. **Read path.** The [Rules](../README.md#rules) state which entries an agent reads. The index
   intro links them.
2. **Unpushed entries.** An entry in a commit that is not pushed can change in that commit, in each
   part. The agent reports the correction to the user. The four edits apply from the first push.
3. **Old paths.** A plain-text old path in a decided entry or a script stays, and means the same
   file at its new path.
4. **Decisions in entries.** A decision that a document or code refers to must be in an entry.
5. **Absorb.** A test in `tools/tests/` is a tool for the absorb. An entry is absorbed when the
   absorb documents together state all of its rules. Open work does not stop the absorb when
   `open-work.md` states it in full. A link to the entry is not enough.
6. **Absorb at landing.** The last commit of the group that writes or lands an entry absorbs it
   when the absorb documents state all of its rules. The agent does not ask the user.
7. **Absorbed status links.** An `absorbed into` status has one link for each heading that states a
   rule. `tools/check_decision_log.py` accepts a list of links and code spans. It fails on a link to
   a Markdown file with no `#anchor`. `STATUS_EXEMPTION_LIMIT` goes from 1,000 to 2,000.
8. **Restate by link.** A superseding entry links the heading of each kept rule that a heading
   states. It writes text only for a changed rule and for a kept rule that no heading states. A
   change under a linked heading does not supersede the linking entry.
9. **Read-path limit.** At 90% of the read-path limit, first absorb each entry that the absorb
   documents state. Then write each other rule into its absorb document, and absorb its entry.
   This replaces "write a consolidation entry when the limit fails".
10. **Evidence.** Long evidence goes in `evidence/` of the log folder.
11. **AI attribution.** [`AGENTS.md` §6](../../AGENTS.md#6-git-rules) states that the rule against AI
    attribution overrides a default of a tool or a harness.
12. **Template.** [template.md](../template.md) is the current kit template.

These kit changes are not copied: a link-check skip for a folder that this repo does not have,
the module rules and the normative-documents placeholder.

## Reason

- The user asked on 2026-11-17 to sync the kit. The mirror rule of the
  [Rules](../README.md#rules) needs the same change in the site log.
- An absorbed entry leaves the read path. Absorb at landing keeps the read path short without a
  review step.
- A link to a heading keeps one source for each rule. A restated text copy can drift.
- A link to a whole Markdown file does not tell where the rule is. The anchor check finds it.
- One link for each heading makes a long status paragraph, so the exemption limit doubles.

## Consequences

- On acceptance, this entry is absorbed at landing when the absorb documents state all its rules.
- The `absorbed into` statuses that exist now link no Markdown file without an anchor, so the new
  check passes.

## Evidence

- `uv run pytest tools/tests` passes with the new tests
  `test_an_absorbed_status_links_a_heading_of_each_markdown_file` and the extended
  `test_matching_index_passes`.

## Alternatives rejected

- **Copy the kit tools whole.** The framework tools hold framework edits, for example the
  invented host names of the tests. The kit diff applies on top of them.
- **Supersede E7ZX.** E7ZX states the log rules only by links, so no rule of E7ZX changes.

## Not repeated

- Do not cite or link the local path of the kit.
