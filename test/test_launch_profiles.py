#!/usr/bin/env python3
# test_launch_profiles.py — tests for the launchers' profile and token logic
# Author: Pito Salas and Claude Code
# Version: 6
# Created: 2026-11-16
# Updated: 2026-11-19
# Open Source Under MIT license

import ast
import inspect
import logging
from pathlib import Path
from unittest.mock import Mock

import pytest
from conftest import install_better_launch_stub

from dome2.launch_options import (
    missing_profile_message,
    resolve_tokens,
    token_string,
)

LAUNCH_DIR = Path(__file__).parent.parent / "launch"

ROBOT_SUBSYSTEMS = [
    "drivers",
    "slam",
    "control",
    "vision",
    "semantic",
    "voice",
    "foxglove",
    "battery",
    "yellow",
]


def robot_tokens(options_str):
    return resolve_tokens(options_str, ROBOT_SUBSYSTEMS)


class TestResolveTokens:
    def test_exact_match(self):
        assert robot_tokens("drivers") == ["drivers"]

    def test_prefix_match(self):
        assert robot_tokens("d") == ["drivers"]
        assert robot_tokens("c") == ["control"]
        assert robot_tokens("f") == ["foxglove"]
        assert robot_tokens("b") == ["battery"]
        assert robot_tokens("y") == ["yellow"]

    def test_disambiguating_prefix(self):
        assert robot_tokens("vi") == ["vision"]
        assert robot_tokens("vo") == ["voice"]

    def test_uppercase_token_matches(self):
        assert robot_tokens("D") == ["drivers"]

    def test_ambiguous_warns_and_skips(self, caplog):
        with caplog.at_level(logging.WARNING):
            assert robot_tokens("v") == []
        assert caplog.records

    def test_unknown_warns_and_skips(self, caplog):
        with caplog.at_level(logging.WARNING):
            assert robot_tokens("xyz") == []
        assert caplog.records

    def test_empty_string(self):
        assert robot_tokens("") == []

    def test_multiple_tokens_keep_order(self):
        assert robot_tokens("f c") == ["foxglove", "control"]

    def test_mixed_valid_and_invalid(self, caplog):
        with caplog.at_level(logging.WARNING):
            assert robot_tokens("c xyz f") == ["control", "foxglove"]
        assert len(caplog.records) == 1


class TestTokenString:
    def test_options_override_profile(self):
        assert token_string("robot", "d", {"robot": "c f"}) == "d"

    def test_profile_reads_env_var(self):
        assert token_string("dev-control", "", {"dev-control": "c"}) == "c"

    def test_missing_profile_env_var_raises(self):
        with pytest.raises(ValueError, match="no-such-profile"):
            token_string("no-such-profile", "", {})

    def test_empty_env_var_is_an_empty_selection(self):
        assert token_string("robot", "", {"robot": ""}) == ""


class TestMissingProfileMessage:
    def test_names_the_profile(self):
        assert "remote" in missing_profile_message("remote", ["viz"])

    def test_lists_every_subsystem(self):
        msg = missing_profile_message("robot", ["drive", "control"])
        assert all(name in msg for name in ["drive", "control"])

    def test_hint_uses_first_subsystem_prefix(self):
        assert 'remote="v"' in missing_profile_message("remote", ["viz"])


class TestLaunchSubsystemsWithoutProfile:
    """With no --options and no profile env var, the launcher shuts down."""

    @pytest.fixture
    def launcher(self, monkeypatch):
        install_better_launch_stub()
        from dome2 import subsystem_launcher

        monkeypatch.delenv("remote", raising=False)
        bl_class = Mock()
        monkeypatch.setattr(subsystem_launcher, "BetterLaunch", bl_class)
        return subsystem_launcher, bl_class

    @pytest.mark.parametrize("is_interactive", [False, True])
    def test_shuts_down_without_launching(self, launcher, is_interactive):
        # sys.exit would end only the UI's worker thread, so the launcher
        # shuts the BetterLaunch instance down, which makes the UI quit.
        subsystem_launcher, bl_class = launcher
        launch_files = {"viz": ("dome_viz", "remote.launch.py")}
        subsystem_launcher.launch_subsystems("remote", "", is_interactive, launch_files)
        bl_instance = bl_class.return_value
        bl_instance.shutdown.assert_called_once()
        bl_instance.include.assert_not_called()

    def test_logs_the_available_subsystems(self, launcher, caplog):
        subsystem_launcher, _ = launcher
        launch_files = {"viz": ("dome_viz", "remote.launch.py")}
        with caplog.at_level(logging.ERROR):
            subsystem_launcher.launch_subsystems("remote", "", False, launch_files)
        assert "viz" in caplog.text


class TestRobotLaunch:
    def test_subsystems_match_launch_table(self, robot_launch):
        assert robot_launch.SUBSYSTEMS == ROBOT_SUBSYSTEMS

    def test_every_token_prefix_resolves(self, robot_launch):
        assert robot_tokens("d sl c vi se vo f b y") == robot_launch.SUBSYSTEMS


class TestRemoteLaunch:
    def test_viz_is_the_only_subsystem(self, remote_launch):
        assert remote_launch.SUBSYSTEMS == ["viz"]
        assert remote_launch.LAUNCH_FILES["viz"] == ("dome_viz", "remote.launch.py")

    def test_v_resolves_to_viz(self, remote_launch):
        assert resolve_tokens("v", remote_launch.SUBSYSTEMS) == ["viz"]

    def test_robot_token_is_unknown_on_remote(self, remote_launch, caplog):
        with caplog.at_level(logging.WARNING):
            assert resolve_tokens("d", remote_launch.SUBSYSTEMS) == []
        assert caplog.records


LAUNCHERS = [("robot.launch.py", "robot_launch"), ("remote.launch.py", "remote_launch")]


@pytest.mark.parametrize(("file_name", "func_name"), LAUNCHERS)
class TestLauncherSignature:
    def test_param_annotations_are_plain_types(
        self, file_name, func_name, robot_launch, remote_launch
    ):
        # better_launch passes each annotation straight to click.Option(type=...),
        # which cannot build an option from a union such as `str | None`.
        module = robot_launch if file_name == "robot.launch.py" else remote_launch
        func = getattr(module, func_name)
        for param in inspect.signature(func).parameters.values():
            assert isinstance(param.annotation, type), param.name

    def test_defaults_are_literals(self, file_name, func_name):
        # bl reads launch arguments by parsing the source, not by running it,
        # so a default like `DEFAULT_PROFILE` (a name) can't be evaluated.
        tree = ast.parse((LAUNCH_DIR / file_name).read_text())
        func = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == func_name
        )
        for default in func.args.defaults:
            assert isinstance(default, ast.Constant), ast.dump(default)
