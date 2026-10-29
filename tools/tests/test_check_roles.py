"""The role contract check of `tools/lint/check_roles.py` (framework NTK9 rule 4).

The assertion runs need `ansible-playbook`, which runs only on Linux. These tests replace
`run_assertions` with a fake, so they test the file checks on each platform. The lint container and
CI run the real assertions.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("check_roles", REPO_ROOT / "tools" / "lint" / "check_roles.py")
assert SPEC is not None and SPEC.loader is not None
check_roles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_roles)

ASSERT_FIRST = "---\n- ansible.builtin.import_tasks: assert.yml\n"


def make_role(root: Path, name: str, vars_text: str, defaults_text: str = "", tasks_text: str = ASSERT_FIRST) -> Path:
    role = root / name
    for folder, text in (("vars", vars_text), ("defaults", defaults_text), ("tasks", tasks_text)):
        (role / folder).mkdir(parents=True)
        if text:
            (role / folder / "main.yml").write_text(text, encoding="utf-8")
    return role


def assertions_fail(names: list[str]):
    """A fake run that fails and names each required value, as the real assertions do."""

    def run(role: str, extra_vars: dict) -> tuple[int, str]:
        return 2, "\n".join(f"{name} is required" for name in names)

    return run


def test_role_without_the_two_lists_fails(tmp_path: Path) -> None:
    role = make_role(tmp_path, "demo", "---\ndemo_required_values: []\n")
    assert check_roles.check_role(role) == [
        "demo: vars/main.yml must define demo_required_values and demo_opt_in_values"
    ]


def test_role_with_empty_lists_passes(tmp_path: Path) -> None:
    role = make_role(tmp_path, "demo", "---\ndemo_required_values: []\ndemo_opt_in_values: []\n")
    assert check_roles.check_role(role) == []


def test_required_value_with_a_role_default_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_roles, "run_assertions", assertions_fail(["demo_port"]))
    role = make_role(
        tmp_path,
        "demo",
        "---\ndemo_required_values: [demo_port]\ndemo_opt_in_values: []\n",
        "---\ndemo_port: 25\n",
    )
    assert check_roles.check_role(role) == ["demo: required value demo_port has a role default"]


def test_value_that_is_required_and_opt_in_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_roles, "run_assertions", assertions_fail(["demo_port"]))
    role = make_role(
        tmp_path,
        "demo",
        "---\ndemo_required_values: [demo_port]\ndemo_opt_in_values: [demo_port]\n",
        "---\ndemo_port: false\n",
    )
    assert "demo: demo_port is both required and opt-in" in check_roles.check_role(role)


@pytest.mark.parametrize("default", ["true", "0", "null"])
def test_opt_in_value_must_default_to_false(tmp_path: Path, default: str) -> None:
    role = make_role(
        tmp_path,
        "demo",
        "---\ndemo_required_values: []\ndemo_opt_in_values: [demo_full]\n",
        f"---\ndemo_full: {default}\n",
    )
    assert check_roles.check_role(role) == ["demo: opt-in value demo_full must have the default false"]


def test_missing_opt_in_default_fails(tmp_path: Path) -> None:
    role = make_role(tmp_path, "demo", "---\ndemo_required_values: []\ndemo_opt_in_values: [demo_full]\n")
    assert check_roles.check_role(role) == ["demo: opt-in value demo_full must have the default false"]


def test_feature_switch_must_default_to_false(tmp_path: Path) -> None:
    role = make_role(
        tmp_path,
        "demo",
        "---\ndemo_required_values: []\ndemo_opt_in_values: []\n",
        "---\ndemo_enabled: true\ndemo_other: true\n",
    )
    assert check_roles.check_role(role) == ["demo: feature switch demo_enabled must have the default false"]


def test_first_task_must_import_assert(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_roles, "run_assertions", assertions_fail(["demo_port"]))
    role = make_role(
        tmp_path,
        "demo",
        "---\ndemo_required_values: [demo_port]\ndemo_opt_in_values: []\n",
        tasks_text="---\n- ansible.builtin.debug:\n    msg: first\n",
    )
    assert check_roles.check_role(role) == ["demo: the first task of tasks/main.yml must import assert.yml"]


def test_assertions_that_pass_are_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_roles, "run_assertions", lambda role, extra_vars: (0, "ok"))
    role = make_role(tmp_path, "demo", "---\ndemo_required_values: [demo_port]\ndemo_opt_in_values: []\n")
    errors = check_roles.check_role(role)
    for case in ("empty inventory", "placeholders", "empty values"):
        assert f"demo: the assertions pass with {case}" in errors
        assert f"demo: no failure for demo_port with {case}" in errors


def test_assertion_cases_use_empty_placeholder_and_null_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[dict] = []

    def run(role: str, extra_vars: dict) -> tuple[int, str]:
        seen.append(extra_vars)
        return 2, "demo_port is required"

    monkeypatch.setattr(check_roles, "run_assertions", run)
    role = make_role(tmp_path, "demo", "---\ndemo_required_values: [demo_port]\ndemo_opt_in_values: []\n")
    assert check_roles.check_role(role) == []
    assert seen == [{}, {"demo_port": "CHANGEME"}, {"demo_port": None}]


@pytest.mark.parametrize(
    "role",
    sorted(p for p in (REPO_ROOT / "roles").iterdir() if p.is_dir()),
    ids=lambda p: p.name,
)
def test_each_role_passes_the_file_checks(role: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    names = check_roles.load(role / "vars" / "main.yml").get(f"{role.name}_required_values") or []
    monkeypatch.setattr(check_roles, "run_assertions", assertions_fail(names))
    assert check_roles.check_role(role) == []
