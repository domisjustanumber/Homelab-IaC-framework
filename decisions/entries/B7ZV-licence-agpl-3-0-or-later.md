# B7ZV — The framework is licensed under the GNU AGPL, version 3 only

**Status:** proposed, 2026-10-25 (agent); recorded again 2026-11-04 (user: version 3 only).

## Decision

1. **Licence.** The framework is licensed under the GNU Affero General Public License, version 3
   only (SPDX `AGPL-3.0-only`).
2. **Licence file.** [`LICENSE`](../../LICENSE) holds the full text of the AGPL version 3, unchanged.
3. **Contributions.** Each contribution is licensed under the same terms.

## Reason

- The user asked for the most copyleft licence (2026-10-25).
- The user chose version 3 only (2026-11-04). A later AGPL version applies only when the copyright
  holders decide it. The licence does not give that choice to each user.
- The AGPL has all the copyleft terms of the GPL version 3. It also covers network use: a person who
  runs a changed version as a network service must offer its source to the users of that service.
- The AGPL version 3 is an open-source licence (OSI) and a free-software licence (FSF).
- AGPL version 3 code can be combined with GPL version 3 code (AGPL section 13). `ansible-core` is
  licensed under the GPL version 3 or later.

## Consequences

- A person who changes the framework and distributes it, or runs it as a network service, must
  publish the changed source under the same licence.
- Some organisations do not allow AGPL code. They cannot use the framework.
- Private use needs no publication. The site uses the framework privately, and it does not
  distribute it or offer it to others as a network service.
- A move to a later AGPL version needs the consent of each copyright holder. Today the owner is the
  only one.
- On acceptance, the `license` field in `meta/main.yml` of each role changes from
  `AGPL-3.0-or-later` to `AGPL-3.0-only`.

## Alternatives rejected

- **AGPL version 3 or later.** Each user can then choose any later AGPL version. The user wants the
  copyright holders to make that choice.
- **GPL version 3.** It has no term for network use, so it is less copyleft.
- **LGPL, MPL or EUPL.** Weaker copyleft: they let a larger work use other terms.
- **MIT or Apache 2.0.** Permissive, not copyleft.
- **SSPL.** It has a wider copyleft term, but it is not an open-source licence (the OSI did not
  approve it).
