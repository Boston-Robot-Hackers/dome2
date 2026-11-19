#!/usr/bin/env python3
# test_stack_ops.py — tests for the cross-package stack tool, git mocked
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-16
# Updated: 2026-11-19
# Open Source Under MIT license

import subprocess
from pathlib import Path

import pytest

from dome2 import stack_ops
from dome2.stack_ops import (
    PackageResult,
    clone_package,
    main,
    pull_package,
    run_operation,
    status_lines,
    status_package,
    summary_lines,
)
from dome2.stack_registry import StackPackage

REGISTRY_TEXT = """
packages:
  - {name: dome_a, repo: git@example:dome_a.git, runs_on: robot}
  - {name: dome_b, repo: git@example:dome_b.git, runs_on: both}
  - {name: dome_c, repo: git@example:dome_c.git, runs_on: remote}
"""

PACKAGE_A = StackPackage("dome_a", "git@example:dome_a.git", "robot")


@pytest.fixture
def workspace(tmp_path):
    """A registry file plus a src/ dir holding dome_a and dome_b, not dome_c."""
    registry_path = tmp_path / "packages.yaml"
    registry_path.write_text(REGISTRY_TEXT)
    src_dir = tmp_path / "src"
    for name in ("dome_a", "dome_b"):
        (src_dir / name).mkdir(parents=True)
    return registry_path, src_dir


@pytest.fixture
def git_calls(monkeypatch):
    """Record git argument lists; a call mentioning a name in `failing` exits 1."""
    calls = {"args": [], "failing": set()}

    def fake_run(cmd, **kwargs):
        git_args = cmd[1:]
        calls["args"].append(git_args)
        is_failing = any(name in arg for arg in git_args for name in calls["failing"])
        output = "Already up to date.\n"
        return subprocess.CompletedProcess(cmd, int(is_failing), output, "")

    monkeypatch.setattr(stack_ops.subprocess, "run", fake_run)
    return calls


class TestGitDetailLine:
    @pytest.mark.parametrize(
        ("returncode", "output", "expected"),
        [
            (0, "Updating 1a2b..3c4d\nFast-forward\n 2 files changed", "Updating 1a2b"),
            (1, "hint: x\nfatal: Not possible to fast-forward", "fatal: Not possible"),
            (0, "", ""),
        ],
    )
    def test_detail_line(self, monkeypatch, tmp_path, returncode, output, expected):
        def fake_run(cmd, **kwargs):
            return subprocess.CompletedProcess(cmd, returncode, output, "")

        monkeypatch.setattr(stack_ops.subprocess, "run", fake_run)
        (tmp_path / "dome_a").mkdir()
        result = pull_package(PACKAGE_A, tmp_path)
        assert result.is_ok == (returncode == 0)
        assert result.detail.startswith(expected)


class TestPullPackage:
    def test_pulls_with_ff_only(self, tmp_path, git_calls):
        (tmp_path / "dome_a").mkdir()
        assert pull_package(PACKAGE_A, tmp_path).is_ok
        assert git_calls["args"] == [
            ["-C", str(tmp_path / "dome_a"), "pull", "--ff-only"]
        ]

    def test_missing_package_fails_and_points_to_clone(self, tmp_path, git_calls):
        result = pull_package(PACKAGE_A, tmp_path)
        assert not result.is_ok
        assert "make clone" in result.detail
        assert git_calls["args"] == []


class TestClonePackage:
    def test_missing_package_is_cloned_as_peer(self, tmp_path, git_calls):
        assert clone_package(PACKAGE_A, tmp_path).is_ok
        assert git_calls["args"] == [
            ["clone", "git@example:dome_a.git", str(tmp_path / "dome_a")]
        ]

    def test_present_package_is_left_alone(self, tmp_path, git_calls):
        (tmp_path / "dome_a").mkdir()
        assert clone_package(PACKAGE_A, tmp_path).is_ok
        assert git_calls["args"] == []

    def test_present_file_is_left_alone_too(self, tmp_path, git_calls):
        (tmp_path / "dome_a").write_text("")
        assert clone_package(PACKAGE_A, tmp_path).is_ok
        assert git_calls["args"] == []


class TestSummaryLines:
    def test_all_ok(self):
        lines = summary_lines([PackageResult("dome_a", True, "")], "pull")
        assert len(lines) == 2
        assert lines[-1].startswith("pull")

    def test_failures_are_named(self):
        results = [
            PackageResult("dome_a", True, ""),
            PackageResult("dome_b", False, "x"),
        ]
        last_line = summary_lines(results, "clone")[-1]
        assert "dome_b" in last_line
        assert "dome_a" not in last_line


class TestRunOperation:
    def test_pull_every_package_whatever_its_runs_on(self, workspace, git_calls):
        registry_path, src_dir = workspace
        (src_dir / "dome_c").mkdir()
        assert run_operation("pull", registry_path, src_dir) == 0
        assert len(git_calls["args"]) == 3

    def test_pull_failure_does_not_stop_the_rest(self, workspace, git_calls):
        registry_path, src_dir = workspace
        (src_dir / "dome_c").mkdir()
        git_calls["failing"].add("dome_a")
        assert run_operation("pull", registry_path, src_dir) == 1
        assert len(git_calls["args"]) == 3

    def test_pull_reports_missing_package(self, workspace, git_calls, capsys):
        registry_path, src_dir = workspace
        assert run_operation("pull", registry_path, src_dir) == 1
        assert len(git_calls["args"]) == 2
        assert "dome_c" in capsys.readouterr().out

    def test_clone_only_clones_missing(self, workspace, git_calls):
        registry_path, src_dir = workspace
        assert run_operation("clone", registry_path, src_dir) == 0
        assert git_calls["args"] == [
            ["clone", "git@example:dome_c.git", str(src_dir / "dome_c")]
        ]

    def test_clone_failure_does_not_stop_the_rest(self, tmp_path, git_calls):
        registry_path = tmp_path / "packages.yaml"
        registry_path.write_text(REGISTRY_TEXT)
        git_calls["failing"].add("dome_a")
        assert run_operation("clone", registry_path, tmp_path / "src") == 1
        assert len(git_calls["args"]) == 3


class TestMain:
    def test_unknown_operation_exits(self, workspace):
        registry_path, src_dir = workspace
        with pytest.raises(SystemExit):
            main(["build", "--registry", str(registry_path), "--src", str(src_dir)])


@pytest.fixture
def scripted_git(monkeypatch):
    """Answer git by subcommand; `answers[(repo, subcommand)]` overrides a default.

    A default repo is clean and in step with its upstream. Each answer is
    (returncode, stdout). Calls are recorded as (repo, git args after -C dir).
    """
    defaults = {"status": (0, ""), "rev-list": (0, "0\t0\n")}
    state = {"answers": {}, "calls": []}

    def fake_run(cmd, **kwargs):
        repo = Path(cmd[2]).name
        git_args = cmd[3:]
        state["calls"].append((repo, git_args))
        subcommand = git_args[0]
        answer = state["answers"].get((repo, subcommand))
        returncode, stdout = answer or defaults.get(subcommand, (0, ""))
        return subprocess.CompletedProcess(cmd, returncode, stdout, "")

    monkeypatch.setattr(stack_ops.subprocess, "run", fake_run)
    return state


def subcommands(state, repo="dome_a"):
    return [args[0] for name, args in state["calls"] if name == repo]


class TestStatusPackage:
    @pytest.fixture
    def repo_dir(self, tmp_path):
        (tmp_path / "dome_a").mkdir()
        return tmp_path

    def test_clean_repo(self, repo_dir, scripted_git):
        result = status_package(PACKAGE_A, repo_dir)
        assert result.is_ok
        assert result.detail == "clean"
        assert subcommands(scripted_git)[0] == "fetch"

    def test_counts_uncommitted_push_and_pull(self, repo_dir, scripted_git):
        scripted_git["answers"][("dome_a", "status")] = (0, " M a\n?? b\n")
        scripted_git["answers"][("dome_a", "rev-list")] = (0, "3\t1\n")
        result = status_package(PACKAGE_A, repo_dir)
        assert result.is_ok
        for expected in ("2 uncommitted", "1 to push", "3 to pull"):
            assert expected in result.detail

    def test_no_upstream_fails(self, repo_dir, scripted_git):
        scripted_git["answers"][("dome_a", "rev-list")] = (128, "")
        assert not status_package(PACKAGE_A, repo_dir).is_ok

    def test_fetch_failure_fails(self, repo_dir, scripted_git):
        scripted_git["answers"][("dome_a", "fetch")] = (1, "")
        assert not status_package(PACKAGE_A, repo_dir).is_ok
        assert subcommands(scripted_git) == ["fetch"]

    def test_missing_package_points_to_clone(self, tmp_path, scripted_git):
        result = status_package(PACKAGE_A, tmp_path)
        assert not result.is_ok
        assert "make clone" in result.detail
        assert scripted_git["calls"] == []


class TestStatusLines:
    def test_one_line_per_repo_labelled_clean_dirty_or_fail(self):
        results = [
            PackageResult("dome_a", True, stack_ops.CLEAN_DETAIL),
            PackageResult("dome_b", True, "1 to push"),
            PackageResult("dome_c", False, "no upstream branch"),
        ]
        lines = status_lines(results)
        assert [line.split()[:2] for line in lines] == [
            ["CLEAN", "dome_a"],
            ["DIRTY", "dome_b"],
            ["FAIL", "dome_c:"],
        ]

    def test_status_prints_only_the_repo_lines(self, workspace, scripted_git, capsys):
        registry_path, src_dir = workspace
        (src_dir / "dome_c").mkdir()
        scripted_git["answers"][("dome_b", "status")] = (0, " M a\n")
        assert run_operation("status", registry_path, src_dir) == 0
        assert capsys.readouterr().out.splitlines() == [
            "CLEAN  dome_a",
            "DIRTY  dome_b",
            "CLEAN  dome_c",
        ]

    def test_failure_sets_exit_status(self, workspace, scripted_git):
        registry_path, src_dir = workspace
        assert run_operation("status", registry_path, src_dir) == 1


class TestMakefile:
    MAKEFILE = Path(__file__).parent.parent / "Makefile"

    def test_help_lists_status_repos(self):
        completed = subprocess.run(
            ["make", "-f", str(self.MAKEFILE), "help"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "status-repos" in completed.stdout
