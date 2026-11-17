#!/bin/sh
# Build or update the controller on the machine that runs this script (ADR-0002 rule 7).
#
#   cd <the root of the site checkout> && sh framework/roles/controller/files/seed.sh
#
# Run it as root on the controller. The site checkout must hold the framework submodule and
# playbooks/controller.yml, with a play tagged `controller` and a play tagged `host`.
# The script installs uv at its pinned version and checks the sha256, makes a temporary venv from
# the locked `ansible` group, and asks for each token that is not on disk yet. Then it runs the
# playbook two times, each time with one token (ADR-0004 rule 4): the `controller` play with the
# controller token, then the `host` play with the hosts token.
# Run it again to apply a change. A second run must report changed=0.
set -eu

framework=framework
defaults=$framework/roles/controller/defaults/main.yml
playbook=playbooks/controller.yml

fail() { echo "seed.sh: $*" >&2; exit 1; }

[ "$(id -u)" -eq 0 ] || fail "run it as root"
[ -f "$defaults" ] || fail "run it from the root of the site checkout, with the framework submodule"
[ -f "$playbook" ] || fail "$playbook is missing"

# The value of one top-level key of the role defaults, with or without quotes.
pin() { sed -n "s/^$1: *\"\{0,1\}\([^\" ]*\)\"\{0,1\}.*\$/\1/p" "$defaults"; }
uv_version=$(pin controller_uv_version)
uv_sha256=$(pin controller_uv_sha256)
# shortcut: reads the role defaults only; a site that overrides controller_token_dir must change this line.
token_dir=$(pin controller_token_dir)
[ -n "$uv_version" ] && [ -n "$uv_sha256" ] && [ -n "$token_dir" ] || fail "no pins in $defaults"

work=$(mktemp -d)
trap 'stty echo 2>/dev/null || true; rm -rf "$work"' EXIT
trap 'exit 1' HUP INT TERM

apt-get update -q
apt-get install -y -q ca-certificates curl git python3

curl -fsSL -o "$work/uv.tar.gz" \
  "https://github.com/astral-sh/uv/releases/download/$uv_version/uv-x86_64-unknown-linux-gnu.tar.gz"
echo "$uv_sha256  $work/uv.tar.gz" | sha256sum -c --quiet - || fail "the sha256 of uv $uv_version does not match"
tar -xzf "$work/uv.tar.gz" -C "$work" --strip-components=1

(cd "$framework" && UV_PROJECT_ENVIRONMENT="$work/venv" UV_PYTHON_DOWNLOADS=never \
  "$work/uv" sync --frozen --only-group ansible --no-install-project --python /usr/bin/python3)
"$work/venv/bin/ansible-galaxy" collection install \
  -r "$framework/requirements.yml" -p /usr/share/ansible/collections

# Only root can read a token (ADR-0004 rule 4). A token never goes on a command line.
# shortcut: the token names of controller_run_users are fixed here; add a name when a run user is added.
install -d -m 0700 -o root -g root "$token_dir"
for name in controller hosts; do
  file=$token_dir/$name
  [ -s "$file" ] && continue
  printf 'Paste the %s service-account token, then press Enter: ' "$name"
  stty -echo
  IFS= read -r token
  stty echo
  echo
  [ -n "$token" ] || fail "the $name token is empty"
  (umask 077 && printf '%s\n' "$token" > "$file")
  token=
done

run() { # <token> <tag>
  OP_SERVICE_ACCOUNT_TOKEN=$(cat "$token_dir/$1") \
    "$work/venv/bin/ansible-playbook" "$playbook" --tags "$2"
}
run controller controller
run hosts host
