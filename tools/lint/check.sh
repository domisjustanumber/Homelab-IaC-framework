#!/bin/sh
# The Ansible checks (ADR-E7ZX). Ansible runs only on Linux, so they run in the
# lint container: tools/lint.sh starts it on the controller, and
# tools/lint/ci.sh runs them in CI.
set -eu

echo "== ansible-lint"
ansible-lint

echo "== role checks"
python3 tools/lint/check_roles.py
