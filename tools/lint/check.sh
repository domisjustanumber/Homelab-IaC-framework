#!/bin/sh
# Runs inside the lint container (started by tools/lint.sh).
set -eu

echo "== yamllint"
yamllint .

echo "== ansible-lint"
ansible-lint

echo "== role checks"
python3 tools/lint/check_roles.py

echo "== shellcheck"
find tools -name '*.sh' -type f -exec shellcheck {} +
