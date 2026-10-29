# avahi

The role publishes the host over mDNS with `avahi-daemon`.
It also enables `.local` name resolution through nsswitch.
The playbook applies the role only when `avahi_enabled` is on
([NTK9](../../decisions/NTK9-generic-roles-and-host-values.md)).

The role supports Debian 13 hosts
([BQXN](../../decisions/BQXN-debian-hosts-and-the-base-role.md)).
It makes no change for an LXC container.
In an unprivileged LXC, `avahi-daemon` can need dbus and AppArmor changes.

## Inventory values

The inventory of the site must supply these values.
The role stops at the start when a value is not set, or when it is `CHANGEME` or `CONFIRM`.

- `avahi_hostname` (required): the mDNS name. The role removes a `.local` suffix for `host-name`.
- `lan_interface` (required): the LAN interface, for `allow-interfaces`.

## Role defaults

`avahi_packages`, `avahi_config_path`, `avahi_nsswitch_hosts`.

## Handlers

`Restart avahi-daemon`.

## Notes

The role configures no firewall rule for 5353/udp.
A firewall needs its own entry
([BQXN](../../decisions/BQXN-debian-hosts-and-the-base-role.md)).
`allow-interfaces` limits `avahi-daemon` to the LAN interface.
