#!/usr/bin/env python3
# test_launch_profiles.py — tests for robot.launch.py profile and token logic
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import importlib.util
import inspect
import logging
import os
import sys

# Load resolve_tokens and constants directly from the launch file without
# executing the @launch_this decorated function (which requires a ROS runtime).
import types

import pytest

launch_path = os.path.join(os.path.dirname(__file__), "..", "launch", "robot.launch.py")
launch_spec = importlib.util.spec_from_file_location("robot_launch", launch_path)
launch_mod = importlib.util.module_from_spec(launch_spec)

# Stub out better_launch so the module loads without ROS
bl_stub = types.ModuleType("better_launch")
bl_stub.BetterLaunch = object


def identity_decorator(func):
    return func


def launch_this_stub(*decorator_args, **decorator_kwargs):
    return decorator_args[0] if decorator_args else identity_decorator


bl_stub.launch_this = launch_this_stub
sys.modules.setdefault("better_launch", bl_stub)
sys.modules.setdefault("click", pytest.importorskip("click"))

launch_spec.loader.exec_module(launch_mod)

resolve_tokens = launch_mod.resolve_tokens
SUBSYSTEMS = launch_mod.SUBSYSTEMS


class TestResolveTokens:
    def test_exact_match(self):
        assert resolve_tokens("drivers") == ["drivers"]

    def test_prefix_match(self):
        assert resolve_tokens("d") == ["drivers"]
        assert resolve_tokens("c") == ["control"]
        assert resolve_tokens("f") == ["foxglove"]

    def test_disambiguating_prefix(self):
        assert resolve_tokens("vi") == ["vision"]
        assert resolve_tokens("vo") == ["voice"]

    def test_ambiguous_warns_and_skips(self, caplog):
        with caplog.at_level(logging.WARNING):
            result = resolve_tokens("v")
        assert result == []
        assert "ambiguous" in caplog.text.lower()

    def test_unknown_warns_and_skips(self, caplog):
        with caplog.at_level(logging.WARNING):
            result = resolve_tokens("xyz")
        assert result == []
        assert "matches no subsystem" in caplog.text.lower()

    def test_empty_string(self):
        assert resolve_tokens("") == []

    def test_multiple_tokens(self):
        assert resolve_tokens("c f") == ["control", "foxglove"]

    def test_mixed_valid_and_invalid(self, caplog):
        with caplog.at_level(logging.WARNING):
            result = resolve_tokens("c xyz f")
        assert result == ["control", "foxglove"]
        assert "matches no subsystem" in caplog.text.lower()


class TestProfiles:
    def test_profile_reads_env_var(self, monkeypatch):
        monkeypatch.setenv("robot", "d c vi vo f")
        token_str = os.environ.get("robot")
        active = set(resolve_tokens(token_str))
        assert {"drivers", "control", "vision", "voice", "foxglove"} == active

    def test_dev_control_env_var(self, monkeypatch):
        monkeypatch.setenv("dev-control", "c")
        active = set(resolve_tokens(os.environ["dev-control"]))
        assert active == {"control"}

    def test_remote_env_var(self, monkeypatch):
        monkeypatch.setenv("remote", "c f")
        active = set(resolve_tokens(os.environ["remote"]))
        assert "drivers" not in active
        assert "control" in active
        assert "foxglove" in active

    def test_missing_profile_env_var_raises(self):
        os.environ.pop("no-such-profile", None)
        assert os.environ.get("no-such-profile") is None

    def test_robot_nav_env_var(self, monkeypatch):
        monkeypatch.setenv("robot-nav", "d c vi vo f")
        active = set(resolve_tokens(os.environ["robot-nav"]))
        assert active == {"drivers", "control", "vision", "voice", "foxglove"}


class TestStartNavSignature:
    def test_param_annotations_are_plain_types(self):
        # better_launch passes each parameter's annotation straight to
        # click.Option(type=...), which cannot build an option from a
        # union (e.g. `str | None`) — regression check for that crash.
        start_nav = launch_mod.start_nav
        for param in inspect.signature(start_nav).parameters.values():
            assert isinstance(param.annotation, type), (
                f"{param.name} annotation {param.annotation!r} is not a plain "
                "type; better_launch's click bridge can't consume a union"
            )
