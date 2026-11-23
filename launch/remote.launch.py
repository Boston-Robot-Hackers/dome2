#!/usr/bin/env python3
# remote.launch.py — dome2 launcher for the remote computer's side of the stack
# Author: Pito Salas and Claude Code
# Version: 6
# Created: 2026-11-16
# Updated: 2026-11-23
# Open Source Under MIT license
#
# Examples:
#   bl dome2 remote.launch.py                        # use $DOME_REMOTE_PROFILE env var
#   bl dome2 remote.launch.py --options "vi"         # dome_viz map view
#   bl dome2 remote.launch.py --options "vo"         # dome_voice LLM node (Whisper + Claude)
#   bl dome2 remote.launch.py --options "vi vo"      # both
#   bl dome2 remote.launch.py --options "vo p"       # LLM node + Yellow Pad (rosbridge, buttons)
#   bl dome2 remote.launch.py --options "vi" --sim_time True  # bag replay or simulator
#   bl dome2 remote.launch.py --options "e" --map_name <name> # dome_nav explorer, off-robot
#   bl dome2 remote.launch.py --is_interactive       # confirm each subsystem
"""Remote-computer counterpart of `robot.launch.py`, with the same interface.

Subsystems that run off the robot are listed here: dome_viz's map view,
dome_voice's LLM node (F14), dome_pad's rosbridge and button node (F09), and
dome_nav's remote-capable units `slam` and `explorer` (dome_nav F36), which
also appear in `robot.launch.py`: the operator picks the side (stack launch
conventions, *Placement*). `v` alone is ambiguous between viz and voice; use
`vi` or `vo`. `sim_time` and `map_name` aren't used here: better_launch
passes them to every included file that declares them.
"""

import os

from better_launch import launch_this

from dome2.subsystem_launcher import launch_subsystems

# Ordered: this order is the interactive prompt order and the include order.
LAUNCH_FILES = {
    "viz": ("dome_viz", "remote.launch.py"),
    "voice": ("dome_voice", "remote.launch.py"),
    "pad": ("dome_pad", "remote.launch.py"),
    "slam": ("dome_nav", "remote.launch.py", {"unit": "slam"}),
    "explorer": ("dome_nav", "remote.launch.py", {"unit": "explorer"}),
}

SUBSYSTEMS = list(LAUNCH_FILES)

DEFAULT_PROFILE = os.environ.get("DOME_REMOTE_PROFILE", "remote")


@launch_this(ui=True)
def remote_launch(
    profile: str = "",
    options: str = "",
    is_interactive: bool = False,
    sim_time: bool = False,
    map_name: str = "",
):
    """Launch remote-side subsystems by profile, token string, or interactively.

    Subsystems (use any unambiguous prefix): viz (dome_viz live map view),
    voice (dome_voice LLM node: Whisper and Claude), pad (rosbridge for the
    Yellow Pad's ROS tab, and pad_buttons: A asks the LLM for a robot joke),
    slam and explorer (dome_nav units, also offered on the robot).

    Parameters
    ----------
    profile : str
        Env var name whose value is a token string. Default: $DOME_REMOTE_PROFILE,
        else the env var named `remote`.
    options : str
        Space-separated subsystem token prefixes. Overrides profile.
    is_interactive : bool
        Prompt yes/no for each subsystem before launching.
    sim_time : bool
        Passed to the included files that take it (viz, dome_nav units).
    map_name : str
        Passed to the included files that take it. slam and explorer need it.
    """
    # Literal "" default: bl parses the signature statically and can't evaluate names.
    launch_subsystems(profile or DEFAULT_PROFILE, options, is_interactive, LAUNCH_FILES)
