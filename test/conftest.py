#!/usr/bin/env python3
# conftest.py — shared fixtures: load launch files without a ROS runtime
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-16
# Updated: 2026-11-16
# Open Source Under MIT license

import importlib.util
import sys
import types
from pathlib import Path

import pytest

LAUNCH_DIR = Path(__file__).parent.parent / "launch"


def launch_this_stub(*decorator_args, **decorator_kwargs):
    if decorator_args and callable(decorator_args[0]):
        return decorator_args[0]
    return lambda func: func


def install_better_launch_stub():
    bl_stub = types.ModuleType("better_launch")
    bl_stub.BetterLaunch = object
    bl_stub.launch_this = launch_this_stub
    sys.modules.setdefault("better_launch", bl_stub)
    sys.modules.setdefault("click", pytest.importorskip("click"))


def load_launch_file(file_name: str) -> types.ModuleType:
    """Import a launch file as a module with better_launch stubbed out."""
    install_better_launch_stub()
    module_name = file_name.replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, LAUNCH_DIR / file_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def robot_launch():
    return load_launch_file("robot.launch.py")


@pytest.fixture(scope="session")
def remote_launch():
    return load_launch_file("remote.launch.py")
