# NTK9 — Roles are generic; host values come from the inventory of the site

**Status:** proposed, 2026-10-25 (agent); accepted, 2026-10-29 (user).

This entry restates the generic rules of site 0002. Site 0047 restates its site rules and
supersedes site 0002.

## Decision

1. **No host values in a role.** A role holds no hostname, domain, CIDR, IP address, host path, port
   or vault name. These values come from the inventory of the site.
2. **Role defaults.** Each value that a role reads comes from the inventory or from the
   `defaults/main.yml` of that role. It is never a literal in `tasks/` or `templates/`. A host can
   override a default in the inventory. A role default must be one of these:
   - a constant that is correct on each supported host (for example a Debian 13 package name or
     path);
   - the "off" value of an opt-in behaviour (for example `updates_automatic_reboot: false`);
   - a value that has no effect until an opt-in switch is on (for example `updates_reboot_time`).
3. **Required values.** Each other value is required, and it has no role default (for example a
   hostname, a CIDR or a vault name). The role asserts it at the start, and fails with a clear message
   when the value is not defined, or when it is still a placeholder (`CHANGEME`, `CONFIRM`).
4. **CI checks rules 2 and 3.** A test runs the required-value assertions of each role against an
   empty inventory, and expects each one to fail with its message. A second check fails when a
   feature switch or an opt-in boolean has a default other than `false`. Review decides whether a
   constant is correct on each supported host.
5. **Feature switches.** A host declares what it is, with switches (`avahi_enabled`,
   `docker_enabled`, `system_mail_enabled`, …). It does not declare how to build it. The playbook
   applies each optional role only when its switch is on. The `base` role has no switch.
6. **Role README.** The README of each role lists the inventory values that it reads, its role
   defaults and its handlers.

## Reason

- The framework is public, and it serves more than one host. A host value in a role publishes that
  value and binds the role to one host.
- A new host is then "copy the template, fill in the values, add an inventory entry".
- A literal in a task hides a value that a reader can need to change. A role default puts it in one
  known place.
- A placeholder that reaches a host is a guess. A failure stops the run before the guess changes the
  host.
- "Safe" alone cannot be checked. The three kinds of default in rule 2 give a reviewer a concrete
  question, and the CI checks of rule 4 test the parts that a script can decide. A default CIDR, for
  example, can clash with the LAN of some host, so it is a required value.

## Consequences

- Each new host value needs a variable in the inventory of the site, before the role can use it.
- A role cannot run without an inventory that supplies its values.
- Today only `docker_engine` asserts its required values. The change that moves the roles adds the
  assertions to each other role, and the two checks to the CI of the framework.

## Alternatives rejected

- **One repository per host.** The baseline is copied, and the hosts drift apart.
- **A single flat playbook.** Past about 200 lines it cannot be reviewed, and nothing is reused.
- **Host configuration with cloud-init and Compose only.** It cannot manage packages, avahi,
  unattended upgrades or systemd units.

## Not repeated

- Do not give a required value a role default. A wrong default is a silent guess.

_Edited 2026-10-29 (ADR-NXK2): re-ID from ntk9._
