# SAB7 — Host templates cite a decision by its ID only

**Status:** proposed, 2026-10-29 (agent); accepted, 2026-10-29 (user).

Its mirror is site ADR-HQ6H.

## Decision

1. A template that a role writes to a host cites a decision by its ID only, for example
   `# See ADR-CVM2`. The comment has no path of the entry.
2. Other code of this repo keeps the path in its `# See ADR-XXXX` comment, as
   [`AGENTS.md` section 4](../../AGENTS.md#4-project-rules) states.
3. The nine `# See ADR-` comments in `roles/*/templates/` change to the ID-only form.

## Reason

- The user decided on 2026-10-29 that a move of the log must not change a file on a host.
- A role copies the comments of a template into a file on the host. A move or a rename of an entry
  then changes that file, and the handler of the file runs. For `containerd-root.conf.j2`,
  containerd and Docker restart, and each container restarts with them.
- On 2026-10-29 the log moved twice, so a path in a host file went out of date twice.
- The ID is enough to find the entry. The index of this log gives its file.

## Consequences

- The next play run on a host changes these files once and runs their handlers. The paths changed
  already, so the run changes them with either form. After that run, a move of the log does not
  change a host file.

## Alternatives rejected

- **Keep the path in the host templates.** Each later move or rename of an entry changes the host
  files again, and it can restart Docker.
