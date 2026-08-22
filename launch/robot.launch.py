#!/usr/bin/env python3
# robot.launch.py — top-level dome2 launcher with profile and subsystem selection
# Author: Pito Salas and Claude Code
# Open Source Under MIT license
#
# Examples:
#   bl dome2 robot.launch.py                              # use $DOME_PROFILE env var
#   bl dome2 robot.launch.py --profile dev                # use $dev env var
#   bl dome2 robot.launch.py --options "d c vi"           # drivers + control + vision
#   bl dome2 robot.launch.py --is_interactive             # confirm each subsystem
#
# Nav/SLAM is launched separately per mode from the dome_nav package:
#   bl dome_nav robot_map.launch.py --map_name <name>     # Mode A: mapping
#   bl dome_nav robot_nav.launch.py                       # Mode B: AMCL nav
#   bl dome_nav robot_explore.launch.py --map_name <name> # Mode E: explore

import logging
import os

import click
from better_launch import BetterLaunch, launch_this

SUBSYSTEMS = ["drivers", "control", "vision", "voice", "foxglove"]

LAUNCH_FILES = {
    "drivers": ("dome2", "gendrv.launch.py"),
    "control": ("dome2", "dome_control.launch.py"),
    "vision": ("dome2", "dome_vision.launch.py"),
    "voice": ("dome2", "dome_voice.launch.py"),
    "foxglove": ("dome2", "foxglove.launch.py"),
}

DEFAULT_PROFILE = os.environ.get("DOME_PROFILE", "robot")


def resolve_tokens(options_str: str) -> list[str]:
    resolved = []
    for token in options_str.split():
        matches = [s for s in SUBSYSTEMS if s.startswith(token.lower())]
        if len(matches) == 1:
            resolved.append(matches[0])
        elif not matches:
            logging.warning(f"Launch option '{token}' matches no subsystem, skipping")
        else:
            logging.warning(
                f"Launch option '{token}' is ambiguous: matches {matches}, skipping"
            )
    return resolved


@launch_this(ui=True)
def start_nav(
    profile: str = DEFAULT_PROFILE,
    options: str = "",
    is_interactive: bool = False,
):
    """Launch dome2 subsystems by profile, token string, or interactively.

    Subsystems (use any unambiguous prefix): drivers, control, vision, voice, foxglove.
    Example: "d c vi" = drivers + control + vision.

    Parameters
    ----------
    profile : str
        Env var name whose value is a token string. Default env var: $robot.
    options : str
        Space-separated subsystem token prefixes. Overrides profile.
    is_interactive : bool
        Prompt yes/no for each subsystem before launching.
    """
    if options:
        token_str = options
    else:
        token_str = os.environ.get(profile)
        if token_str is None:
            raise ValueError(f"Profile '{profile}': no env var '{profile}' found")

    active = set(resolve_tokens(token_str))
    cfg = {s: s in active for s in SUBSYSTEMS}

    if is_interactive:
        logging.info(f"Profile '{profile}' — confirm each subsystem:")
        for name in SUBSYSTEMS:
            cfg[name] = click.confirm(f"  Launch {name}?", default=cfg[name])

    bl = BetterLaunch()
    for name, enabled in cfg.items():
        if enabled:
            pkg, launch_file = LAUNCH_FILES[name]
            bl.include(pkg, launch_file)
