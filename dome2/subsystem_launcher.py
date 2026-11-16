#!/usr/bin/env python3
# subsystem_launcher — include the chosen subsystems' launch files
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-16
# Updated: 2026-11-16
# Open Source Under MIT license
"""The better_launch side of dome2's launchers.

`robot.launch.py` and `remote.launch.py` each declare an ordered
`LAUNCH_FILES` table (subsystem name → package and launch file) and call
`launch_subsystems`. It resolves the profile or options with
`launch_options`, optionally asks yes/no per subsystem, and includes the
launch file of each enabled one.
"""

import logging
import os

import click
from better_launch import BetterLaunch

from dome2.launch_options import resolve_tokens, token_string


def launch_subsystems(
    profile: str,
    options: str,
    is_interactive: bool,
    launch_files: dict[str, tuple[str, str]],
):
    subsystems = list(launch_files)
    active = set(resolve_tokens(token_string(profile, options, os.environ), subsystems))
    cfg = {name: name in active for name in subsystems}

    if is_interactive:
        logging.info(f"Profile '{profile}' — confirm each subsystem:")
        for name in subsystems:
            cfg[name] = click.confirm(f"  Launch {name}?", default=cfg[name])

    bl = BetterLaunch()
    for name, is_enabled in cfg.items():
        if is_enabled:
            pkg, launch_file = launch_files[name]
            bl.include(pkg, launch_file)
