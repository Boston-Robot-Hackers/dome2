#!/usr/bin/env python3
# robot.launch.py — top-level dome2 launcher with profile and subsystem selection
# Author: Pito Salas and Claude Code
# Version: 5
# Created: 2026-11-16
# Updated: 2026-11-23
# Open Source Under MIT license
#
# Usage:
#   bl dome2 robot.launch.py                              # use $DOME_PROFILE env var
#   bl dome2 robot.launch.py --profile dev                # use $dev env var
#   bl dome2 robot.launch.py --options "d c vi"           # drivers + control + vision
#   bl dome2 robot.launch.py --options "d b p"            # drivers + battery + Yellow Pad
#   bl dome2 robot.launch.py --options "d b sl vi se" --map_name <name>  # semantic mapping
#   bl dome2 robot.launch.py --options "d sl n e" --map_name <name>  # explore, all on robot
#   bl dome2 robot.launch.py --options "d sl n" --map_name <name>    # explorer on the remote
#   bl dome2 robot.launch.py --is_interactive             # confirm each subsystem
#
# dome_nav's nav mode (AMCL) returns after dome_nav I13; until then:
#   bl dome_nav robot_nav.launch.py
"""dome2's robot-side launcher: include the chosen subsystems' launch files.

`LAUNCH_FILES` maps each subsystem to the package launch file it includes,
plus any fixed per-entry args: `slam`, `nav2` and `explorer` are three units
of the one `dome_nav robot.launch.py`, picked by `unit` (dome_nav F36). The
selection logic is in `dome2.subsystem_launcher`. `sim_time` and
`map_name` aren't used here: better_launch passes the launcher's arguments to
every included file that declares the same name (`dome_nav`, `dome_semantic`).
"""

import os

from better_launch import launch_this

from dome2.subsystem_launcher import launch_subsystems

# Ordered: this order is the interactive prompt order and the include order.
LAUNCH_FILES = {
    "drivers": ("dome2", "drivers.launch.py"),
    "slam": ("dome_nav", "robot.launch.py", {"unit": "slam"}),
    "nav2": ("dome_nav", "robot.launch.py", {"unit": "nav2"}),
    "explorer": ("dome_nav", "robot.launch.py", {"unit": "explorer"}),
    "control": ("dome_control", "robot.launch.py"),
    "vision": ("dome_vision_ros", "robot.launch.py"),
    "semantic": ("dome_semantic", "robot.launch.py"),
    "voice": ("dome_voice", "robot.launch.py"),
    "foxglove": ("foxglove_bridge", "foxglove_bridge_launch.xml"),
    "battery": ("dome_telemetry", "robot.launch.py"),
    "pad": ("dome_pad", "robot.launch.py"),
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

    Subsystems (use any unambiguous prefix): drivers, slam, nav2, explorer
    (dome_nav units), control, vision, semantic, voice, foxglove, battery
    (battery telemetry), pad (Yellow Pad joystick teleop). Example: "d c vi" =
    drivers + control + vision; "d sl n e" = autonomous exploration.

    Parameters
    ----------
    profile : str
        Env var name whose value is a token string. Default env var: $robot.
    options : str
        Space-separated subsystem token prefixes. Overrides profile.
    is_interactive : bool
        Prompt yes/no for each subsystem before launching.
    sim_time : bool
        Passed to the included files that take it (dome_nav units).
    map_name : str
        Passed to the included files that take it. slam, explorer and semantic
        need it.
    """
    # Literal "" default: bl parses the signature statically and can't evaluate names.
    launch_subsystems(profile or DEFAULT_PROFILE, options, is_interactive, LAUNCH_FILES)
