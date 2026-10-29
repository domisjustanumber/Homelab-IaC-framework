#!/bin/sh
# Validate the repository (AGENTS.md section 3, ADR-NXK2).
#
#   tools/lint.sh                 full suite
#   tools/lint.sh <cmd> [args]    run one command in the lint container,
#                                 e.g. tools/lint.sh ansible-lint roles/base
#
# yamllint and shellcheck run from the uv venv. Ansible runs only on Linux, so
# the Ansible checks run in the pinned container (tools/lint/Dockerfile).
# A site builds the same image from its framework/ submodule.
set -eu

IMAGE=homelab-lint:2

cd "$(dirname "$0")/.."

if [ "$#" -eq 0 ]; then
  echo "== yamllint"
  uv run yamllint .
  echo "== shellcheck"
  git ls-files -z '*.sh' | xargs -0 uv run shellcheck
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running. Start Docker Desktop, then run tools/lint.sh again." >&2
  exit 1
fi

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  docker build -q -f tools/lint/Dockerfile -t "$IMAGE" .
fi

# Git Bash needs a C:/ style path for the bind mount; elsewhere pwd is fine.
repo=$(pwd -W 2>/dev/null || pwd)

if [ "$#" -gt 0 ]; then
  MSYS_NO_PATHCONV=1 exec docker run --rm -v "$repo:/repo" -w /repo "$IMAGE" "$@"
fi

MSYS_NO_PATHCONV=1 exec docker run --rm -v "$repo:/repo" -w /repo "$IMAGE" sh tools/lint/check.sh
