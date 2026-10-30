# docker_engine

Installs Docker CE from the Docker apt repository for Debian (deb822 source).
First, it removes the distribution packages (`docker.io`, `containerd`, `runc`, ...).
It renders `/etc/docker/daemon.json`.
It adds a drop-in with `RequiresMountsFor=` to `containerd.service` and to `docker.service`.
A second drop-in on `containerd.service` sets the containerd root with `--root`.
The role does not change `/etc/containerd/config.toml`.

## Inventory values

| Variable | Required | Purpose |
|---|---|---|
| `docker_default_address_pool_cidr` | yes | The `default-address-pools` base. It must not overlap the LAN or another CIDR of the host. Check the routes and the Docker networks before you set it. |
| `docker_dir` | yes | The state unit. The drop-ins require its mount. |
| `docker_storage_mounts` | no | More mounts that the drop-ins require. The default is `[]`. |

The role asserts each required value first.
A value that is not set, or that is `CHANGEME` or `CONFIRM`, stops the run.

## Role defaults

| Variable | Default |
|---|---|
| `docker_engine_data_root` | `/var/lib/docker` (`data-root` in `daemon.json`) |
| `docker_engine_containerd_root` | `<data-root>/containerd-root` (`--root` of containerd) |
| `docker_engine_containerd_bin` | `/usr/bin/containerd` (the `ExecStart=` of the drop-in) |
| `docker_engine_required_mounts` | the containerd root, the data-root, `docker_dir` and `docker_storage_mounts` |
| `docker_engine_packages`, `docker_engine_conflicting_packages` | the package lists |
| `docker_engine_repo_url`, `docker_engine_key_url`, `docker_engine_key_path`, `docker_engine_arch_map` | the apt repository |
| `docker_engine_log_max_size`, `docker_engine_log_max_file` | `50m`, `3` (`json-file` log options) |
| `docker_engine_address_pool_size` | `24` |
| `docker_engine_metrics_addr` | `""`: no metrics listener. Set an address, for example `127.0.0.1:9323`, to turn it on. |

The containerd root and the data-root must be on the churn unit
([CVM2](../../decisions/entries/CVM2-storage-layout-containerd-root-by-flag.md) rule 3).
`dockerd` uses `<data-root>/containerd` only for a containerd that it starts itself.
The role uses the containerd of the `containerd.io` package, so `containerd-root` is not used by `dockerd`.
`config.toml` is a conffile of `containerd.io`. A changed conffile can hold the package back in unattended upgrades, so the role sets the root with a flag.

## Handlers

- `Reload systemd for docker_engine` runs when a drop-in changes.
- `Restart containerd` runs when the containerd root drop-in changes.
- `Restart docker` runs when the containerd root drop-in or `daemon.json` changes.
  `live-restore` is off, so a restart stops each container
  ([EQ0Z](../../decisions/entries/EQ0Z-unattended-upgrades-and-reboots.md) rule 6).

## Decisions

- [CVM2](../../decisions/entries/CVM2-storage-layout-containerd-root-by-flag.md): the containerd root,
  the data-root and the drop-ins.
- [EQ0Z](../../decisions/entries/EQ0Z-unattended-upgrades-and-reboots.md): `live-restore` is off.
  The Docker apt origin must stay `origin=Docker,label=Docker CE`, because unattended upgrades match it.
- [0003](../../decisions/entries/0003-controller-pushes-stacks.md) (proposed): the play deploys stacks
  with `community.docker.docker_compose_v2`, so the role installs `docker-compose-plugin`.
