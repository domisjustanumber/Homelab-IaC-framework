#!/bin/sh
# All checks, in the lint image. CI runs this script in the checkout of the
# repository that it checks. A site runs framework/tools/lint/ci.sh.
# The controller runs tools/lint.sh instead.
# See ADR-E7ZX (decisions/entries/E7ZX-all-checks-in-the-lint-image-in-ci.md).
#
# The dev group of the checked repository goes into a second venv, on the
# Python of the image. The image sets UV_PROJECT_ENVIRONMENT=/opt/lint. With
# UV_NO_SYNC=1, /opt/lint keeps only the locked ansible group.
set -eu
export UV_NO_SYNC=1

dev=/tmp/dev

echo "== dev group of uv.lock, on the Python of the image"
UV_PROJECT_ENVIRONMENT=$dev uv sync --locked --no-install-project \
  --python /usr/local/bin/python3

echo "== yamllint"
"$dev/bin/yamllint" .

echo "== shellcheck"
git ls-files -z '*.sh' | xargs -0 "$dev/bin/shellcheck"

echo "== doc checks"
PYTHONDONTWRITEBYTECODE=1 "$dev/bin/python" -m pytest -p no:cacheprovider tools/tests

# ansible-lint and the other Ansible checks of the checked repository, from /opt/lint.
sh tools/lint/check.sh
