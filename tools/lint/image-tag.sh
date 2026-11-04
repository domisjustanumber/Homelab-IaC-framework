#!/bin/sh
# Print the tag of the lint image: a hash of the image inputs.
# See ADR-E7ZX (decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md).
#
#   sh tools/lint/image-tag.sh [<framework root>]
#
# The default root is the repository of this script. A site gives its
# submodule: sh framework/tools/lint/image-tag.sh framework
#
# git hash-object applies the eol=lf rule of .gitattributes, so Windows and
# Linux print the same tag. It also hashes changes that are not committed.
set -eu

root=${1:-$(dirname "$0")/../..}

sum=$(git -C "$root" hash-object tools/lint/Dockerfile pyproject.toml uv.lock requirements.yml \
  | git -C "$root" hash-object --stdin)

echo "homelab-lint:$(printf '%s' "$sum" | cut -c1-12)"
