# 0001 — Decision log of the framework

**Status:** proposed, 2026-10-25 (agent).

## Decision

1. **Decision log.** This repository keeps its decisions in `notes/decisions/`, one numbered entry
   for each decision or measurement. The [index](README.md) has the Active, Deferred and Historical
   tables, the rules and the entry template. [`open-work.md`](open-work.md) has the open work.
2. **Own numbering.** This log starts at 0001. Its numbers are independent of the site log. The site
   log keeps its own entries and numbers.
3. **Restate only when cited.** A site rule becomes a framework entry only when framework code or
   framework documents must cite it. The framework entry restates the rule without site values and
   supersedes the site entry in full. When the site entry also holds site values, a new site entry
   restates those values and supersedes the site entry instead. Then the framework entry supersedes
   nothing.
4. **Citation form.** In this repository, `ADR-NNNN` and a bare number are always entries of this
   log. A site entry is cited as `site NNNN`, with no link.
5. **No link to the site.** The site repository is private. No file of this repository links to it
   or names its location.
6. **Status.** An agent writes a new entry as `proposed`. Only the user changes it to `accepted` or
   `rejected`.
7. **Log rules.** The [Rules](README.md#rules) of the index apply: allowed edits only, supersession in
   full, status forms, Deferred proposals after 183 days, absorption, consolidation, permalinks and
   the size limits.
8. **Public data only.** This repository becomes public. No file holds a credential, a host name, a
   domain, an IP address other than a documentation address, an email address, a user name or a path
   in a user folder. The rule has no exemption.

## Reason

- The framework becomes public and the site stays private. One log cannot be in both.
- Separate numbering lets each log grow without a gap or a collision in the other.
- A restatement of every site entry would copy site history and site values into a public
  repository. A restatement on demand copies only the rules that framework code needs.
- A link to a private repository fails for each public reader, and its URL names the owner.
- The site log already has these rules. The same rules in both logs keep one way of work.

## Consequences

- A rule that both repositories need has one live authority. Until the site log allows a status line
  that names an entry of another repository, a framework entry cannot supersede a site entry.
- Each framework entry must be readable without the site log.

## Alternatives rejected

- **Copy the site series into both repositories.** It makes two different entries with the same
  number, and it copies site values into the public repository.
- **Prefixed identifiers for all entries.** A rename of existing site entries breaks the rule that a
  number never changes.

## Not repeated

- Do not link to the site repository. Write `site NNNN`.
- Do not copy a site value into an entry. Use a documentation address (`192.0.2.0/24`) or name the
  variable.
