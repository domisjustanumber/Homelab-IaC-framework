# Pinned validation toolchain. Ansible cannot run natively on a Windows
# controller, so every lint and syntax check runs here (see tools/lint.sh).
# Bump a version here or in requirements.yml => bump IMAGE in tools/lint.sh.
FROM python:3.13.17-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends shellcheck git \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      ansible-core==2.21.5 \
      ansible-lint==26.10.1 \
      yamllint==1.38.0

COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml -p /usr/share/ansible/collections

# A bind-mounted Windows checkout is world-writable, and Ansible ignores an
# ansible.cfg it discovers in a world-writable directory. Name it explicitly.
ENV ANSIBLE_CONFIG=/repo/ansible.cfg
WORKDIR /repo
