# docker_gc

This role installs the systemd service `docker-gc.service` and the daily timer `docker-gc.timer`.
The service is a oneshot unit with two `ExecStart=` lines.
The first line runs `docker system prune -af --filter until=<retention>`.
The second line runs `docker volume prune -f`.
The rules are in [apg1](../../notes/decisions/apg1-daily-docker-gc.md).

## Inventory values

The inventory of the site supplies these values.
The role asserts the required values at the start
([ntk9](../../notes/decisions/ntk9-generic-roles-and-host-values.md)).

| Variable | Kind | Purpose |
|---|---|---|
| `docker_gc_time` | required | The time (`HH:MM`) when the timer starts the service |
| `docker_gc_image_retention` | required | The `until=` value of `docker system prune` |
| `system_mail_enabled` | feature switch | When `true`, the service gets `OnFailure=status-email@%n.service` ([gee3](../../notes/decisions/gee3-system-mail-through-msmtp.md)) |

## Role defaults

| Variable | Default | Purpose |
|---|---|---|
| `docker_gc_docker_bin` | `/usr/bin/docker` | The path of the Docker CLI |

## Handlers

`Reload systemd for docker_gc` runs `systemctl daemon-reload` when a unit file changes.

## Retention

The `until=` filter applies to stopped containers, unused networks, unused images and the build
cache.
On the containerd image store, `until=` compares the time of the local image record.
The containerd store is the default of a fresh Docker Engine 29 install.
When a pull replaces a tag, the old image becomes a dangling record with the time of that pull.
A superseded image therefore stays for about the retention, plus up to one day.
On the older graph-driver store, `until=` compares the build time.
There, a superseded image normally goes at the next run.
Do not use the retention as a rollback window.

Volume pruning is anonymous-only.
Do not add `-a` to `docker volume prune`, because named volumes then become eligible.
