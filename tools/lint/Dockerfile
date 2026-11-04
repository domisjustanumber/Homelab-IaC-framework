# The lint image (ADR-E7ZX). Ansible runs only on Linux, so on the Windows
# controller the Ansible checks run here (see tools/lint.sh). In CI, all checks
# run here (see tools/lint/ci.sh).
# The image installs the locked ansible group of uv.lock, with no own version
# list. The tag is a hash of this file, pyproject.toml, uv.lock and
# requirements.yml (tools/lint/image-tag.sh). Do not bump it by hand.
# The FROM line of python is the one Python version that gates a merge.
# uv comes from a stage, because Dependabot reads only FROM lines.
FROM ghcr.io/astral-sh/uv:0.13.7 AS uv

FROM python:3.13.17-slim
COPY --from=uv /uv /usr/local/bin/uv

# CI mounts a checkout that another user owns. Git refuses such a repository
# unless safe.directory names it. A site checks its framework/ submodule too.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/* \
 && git config --system --add safe.directory /repo \
 && git config --system --add safe.directory /repo/framework

ENV UV_PROJECT_ENVIRONMENT=/opt/lint \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy
WORKDIR /tmp/lint
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --only-group ansible --no-install-project --no-cache \
      --python /usr/local/bin/python3
# A uv run in /repo must not sync /opt/lint to the default groups.
ENV PATH=/opt/lint/bin:$PATH \
    UV_NO_SYNC=1

COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml -p /usr/share/ansible/collections

# A bind-mounted Windows checkout is world-writable, and Ansible ignores an
# ansible.cfg it discovers in a world-writable directory. Name it explicitly.
# CI mounts the checkout at /repo too.
ENV ANSIBLE_CONFIG=/repo/ansible.cfg
WORKDIR /repo
