"""Check the role contract of framework NTK9 rule 4. Runs in the lint container.

Each role declares two lists in vars/main.yml:
<role>_required_values and <role>_opt_in_values.

1. The assertions of each role fail for each required value when the inventory
   is empty, and when each value is a placeholder (CHANGEME).
2. A required value has no role default. An opt-in value and a feature switch
   (*_enabled) have the default false.
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROLES = Path("roles")
PLAYBOOK = "tools/lint/required-values.yml"


def load(path):
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def run_assertions(role, extra_vars):
    cmd = [
        "ansible-playbook", "-i", "localhost,", PLAYBOOK,
        "-e", f"role_under_test={role}",
        "-e", json.dumps(extra_vars),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout + result.stderr


def check_role(role_dir):
    role = role_dir.name
    errors = []
    names = load(role_dir / "vars" / "main.yml")
    required = names.get(f"{role}_required_values")
    opt_in = names.get(f"{role}_opt_in_values")
    if required is None or opt_in is None:
        return [f"{role}: vars/main.yml must define {role}_required_values and {role}_opt_in_values"]
    defaults = load(role_dir / "defaults" / "main.yml")

    for name in required:
        if name in defaults:
            errors.append(f"{role}: required value {name} has a role default")
        if name in opt_in:
            errors.append(f"{role}: {name} is both required and opt-in")
    for name in opt_in:
        if defaults.get(name, None) is not False:
            errors.append(f"{role}: opt-in value {name} must have the default false")
    for name, value in defaults.items():
        if name.endswith("_enabled") and value is not False:
            errors.append(f"{role}: feature switch {name} must have the default false")

    if not required:
        return errors
    main = load_list(role_dir / "tasks" / "main.yml")
    if not main or main[0].get("ansible.builtin.import_tasks") != "assert.yml":
        errors.append(f"{role}: the first task of tasks/main.yml must import assert.yml")
    cases = {
        "empty inventory": {},
        "placeholders": {name: "CHANGEME" for name in required},
        "empty values": {name: None for name in required},
    }
    for case, extra_vars in cases.items():
        code, output = run_assertions(role, extra_vars)
        if code == 0:
            errors.append(f"{role}: the assertions pass with {case}")
        for name in required:
            if f"{name} is required" not in output:
                errors.append(f"{role}: no failure for {name} with {case}")
    return errors


def load_list(path):
    if not path.is_file():
        return []
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


def main():
    errors = []
    for role_dir in sorted(p for p in ROLES.iterdir() if p.is_dir()):
        errors.extend(check_role(role_dir))
    for error in errors:
        print(f"error: {error}")
    if errors:
        return 1
    print("role checks: pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
