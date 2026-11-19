#!/usr/bin/env python3
# robot.launch.py — top-level dome2 launcher with profile and subsystem selection
# Author: Pito Salas and Claude Code
# Version: 4
# Created: 2026-11-16
# Updated: 2026-11-19
# Open Source Under MIT license
#
# Usage:
#   bl dome2 robot.launch.py                              # use $DOME_PROFILE env var
#   bl dome2 robot.launch.py --profile dev                # use $dev env var
#   bl dome2 robot.launch.py --options "d c vi"           # drivers + control + vision
#   bl dome2 robot.launch.py --options "d b y"            # drivers + battery + yellow pad
#   bl dome2 robot.launch.py --options "d b sl vi se" --map_name <name>  # semantic mapping
#   bl dome2 robot.launch.py --is_interactive             # confirm each subsystem
#
# The Nav2 modes are launched separately from dome_nav until dome_nav I13:
#   bl dome_nav robot_nav.launch.py                       # Mode B: AMCL nav
#   bl dome_nav robot_explore.launch.py --map_name <name> # Mode E: explore
"""dome2's robot-side launcher: include the chosen subsystems' launch files.

`LAUNCH_FILES` maps each subsystem to the package launch file it includes;
the selection logic is in `dome2.subsystem_launcher`. `sim_time` and
`map_name` aren't used here: better_launch passes the launcher's arguments to
every included file that declares the same name (`dome_nav`, `dome_semantic`).
"""

import os

from better_launch import launch_this

from dome2.subsystem_launcher import launch_subsystems

# Ordered: this order is the interactive prompt order and the include order.
LAUNCH_FILES = {
    "drivers": ("dome2", "drivers.launch.py"),
    "slam": ("dome_nav", "robot.launch.py"),
    "control": ("dome_control", "robot.launch.py"),
    "vision": ("dome_vision_ros", "robot.launch.py"),
    "semantic": ("dome_semantic", "robot.launch.py"),
    "voice": ("dome_voice", "robot.launch.py"),
    "foxglove": ("foxglove_bridge", "foxglove_bridge_launch.xml"),
    "battery": ("dome_telemetry", "robot.launch.py"),
    "yellow": ("yellow_pad", "yellow_pad.launch.py"),
}

SUBSYSTEMS = list(LAUNCH_FILES)

DEFAULT_PROFILE = os.environ.get("DOME_PROFILE", "robot")


@launch_this(ui=True)
def robot_launch(
    profile: str = "",
    options: str = "",
    is_interactive: bool = False,
    sim_time: bool = False,
    map_name: str = "",
):
    """Launch dome2 subsystems by profile, token string, or interactively.

    Subsystems (use any unambiguous prefix): drivers, slam, control, vision,
    semantic, voice, foxglove, battery (battery telemetry), yellow (Yellow Pad
    joystick teleop). Example: "d c vi" = drivers + control + vision.

    Parameters
    ----------
    profile : str
        Env var name whose value is a token string. Default env var: $robot.
    options : str
        Space-separated subsystem token prefixes. Overrides profile.
    is_interactive : bool
        Prompt yes/no for each subsystem before launching.
    sim_time : bool
        Passed to the included files that take it (slam).
    map_name : str
        Passed to the included files that take it. slam and semantic need it.
    """
    # Literal "" default: bl parses the signature statically and can't evaluate names.
    launch_subsystems(profile or DEFAULT_PROFILE, options, is_interactive, LAUNCH_FILES)
