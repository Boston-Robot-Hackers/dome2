#!/usr/bin/env python3
# robot.launch.py — top-level dome2 launcher with profile and subsystem selection
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-16
# Updated: 2026-11-17
# Open Source Under MIT license
#
# Examples:
#   bl dome2 robot.launch.py                              # use $DOME_PROFILE env var
#   bl dome2 robot.launch.py --profile dev                # use $dev env var
#   bl dome2 robot.launch.py --options "d c vi"           # drivers + control + vision
#   bl dome2 robot.launch.py --options "d b y"            # drivers + battery + yellow pad
#   bl dome2 robot.launch.py --is_interactive             # confirm each subsystem
#
# Nav/SLAM is launched separately per mode from the dome_nav package:
#   bl dome_nav robot.launch.py --map_name <name>         # Mode A: SLAM mapping
#   bl dome_nav robot_nav.launch.py                       # Mode B: AMCL nav
#   bl dome_nav robot_explore.launch.py --map_name <name> # Mode E: explore

import os

from better_launch import launch_this

from dome2.subsystem_launcher import launch_subsystems

# Ordered: this order is the interactive prompt order and the include order.
LAUNCH_FILES = {
    "drivers": ("dome2", "gendrv.launch.py"),
    "control": ("dome2", "dome_control.launch.py"),
    "vision": ("dome2", "dome_vision.launch.py"),
    "voice": ("dome2", "dome_voice.launch.py"),
    "foxglove": ("dome2", "foxglove.launch.py"),
    "battery": ("dome_telemetry", "robot.launch.py"),
    "yellow": ("yellow_pad", "yellow_pad.launch.py"),
}

SUBSYSTEMS = list(LAUNCH_FILES)

DEFAULT_PROFILE = os.environ.get("DOME_PROFILE", "robot")


@launch_this(ui=True)
def start_nav(
    profile: str = "",
    options: str = "",
    is_interactive: bool = False,
):
    """Launch dome2 subsystems by profile, token string, or interactively.

    Subsystems (use any unambiguous prefix): drivers, control, vision, voice, foxglove,
    battery (battery telemetry), yellow (Yellow Pad joystick teleop).
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
    # Literal "" default: bl parses the signature statically and can't evaluate names.
    launch_subsystems(profile or DEFAULT_PROFILE, options, is_interactive, LAUNCH_FILES)
