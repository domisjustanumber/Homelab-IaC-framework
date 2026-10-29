#!/bin/sh
# The Ansible checks (ADR-NXK2). Ansible runs only on Linux: in the lint
# container (started by tools/lint.sh) or in CI from the uv venv.
set -eu

echo "== ansible-lint"
ansible-lint

echo "== role checks"
python3 tools/lint/check_roles.py
