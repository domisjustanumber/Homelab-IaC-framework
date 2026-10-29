# The lint image (ADR-NXK2). Ansible runs only on Linux, so on the Windows
# controller the Ansible checks run here (see tools/lint.sh). yamllint and
# shellcheck run from the uv venv, not here.
# The image installs the locked ansible group of uv.lock, with no own version
# list. A change of that group or of requirements.yml => bump IMAGE in
# tools/lint.sh.
FROM python:3.13.17-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /usr/local/bin/uv

RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

ENV UV_PROJECT_ENVIRONMENT=/opt/lint \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy
WORKDIR /tmp/lint
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --only-group ansible --no-install-project --no-cache \
      --python /usr/local/bin/python3
ENV PATH=/opt/lint/bin:$PATH

COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml -p /usr/share/ansible/collections

# A bind-mounted Windows checkout is world-writable, and Ansible ignores an
# ansible.cfg it discovers in a world-writable directory. Name it explicitly.
ENV ANSIBLE_CONFIG=/repo/ansible.cfg
WORKDIR /repo
