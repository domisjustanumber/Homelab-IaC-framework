# Decision log: historical entries

These entries are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX` or `done`. They are not in the read path. Read an entry here only to find
the reason for a decision. The [index](README.md) has the Active and Proposed entries and the
[Rules](README.md#rules).

### Historical

| # | Decision | Status |
|---|----------|--------|
| [S3XT](entries/S3XT-storage-layout-and-bind-mounted-state.md) | Docker hosts keep state apart from image churn; containerd and Docker roots on the churn unit; mounts enforced; state bind-mounted | superseded by CVM2 |
| [0001](entries/0001-decision-log-agents-md-and-private-data.md) | Decision log of the framework and its rules; own IDs; restate a site rule only when cited; `AGENTS.md` only; no private data | superseded by NXK2 |
| [NXK2](entries/NXK2-current-decision-log-kit.md) | The current decision-log kit: essential Rules, `decisions/entries/`, upper-case IDs with a digit, `ADR-` citations, no AI attribution, linters in a uv venv | superseded by E7ZX |
