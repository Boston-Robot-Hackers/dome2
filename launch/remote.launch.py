#!/usr/bin/env python3
# remote.launch.py — dome2 launcher for the remote computer's side of the stack
# Author: Pito Salas and Claude Code
# Version: 5
# Created: 2026-11-16
# Updated: 2026-11-20
# Open Source Under MIT license
#
# Examples:
#   bl dome2 remote.launch.py                        # use $DOME_REMOTE_PROFILE env var
#   bl dome2 remote.launch.py --options "vi"         # dome_viz map view
#   bl dome2 remote.launch.py --options "vo"         # dome_voice LLM node (Whisper + Claude)
#   bl dome2 remote.launch.py --options "vi vo"      # both
#   bl dome2 remote.launch.py --options "vo p"       # LLM node + Yellow Pad (rosbridge, buttons)
#   bl dome2 remote.launch.py --options "vi" --sim_time True  # bag replay or simulator
#   bl dome2 remote.launch.py --is_interactive       # confirm each subsystem
"""Remote-computer counterpart of `robot.launch.py`, with the same interface.

Subsystems that run off the robot are listed here: dome_viz's map view,
dome_voice's LLM node (F14), and dome_pad's rosbridge and button node (F09).
`v` alone is ambiguous between viz and voice; use `vi` or `vo`. `sim_time`
isn't used here: better_launch passes it to every included file that
declares it (`dome_viz`).
"""

import os

from better_launch import launch_this

from dome2.subsystem_launcher import launch_subsystems

# Ordered: this order is the interactive prompt order and the include order.
LAUNCH_FILES = {
    "viz": ("dome_viz", "remote.launch.py"),
    "voice": ("dome_voice", "remote.launch.py"),
    "pad": ("dome_pad", "remote.launch.py"),
}

SUBSYSTEMS = list(LAUNCH_FILES)

DEFAULT_PROFILE = os.environ.get("DOME_REMOTE_PROFILE", "remote")


@launch_this(ui=True)
def remote_launch(
    profile: str = "",
    options: str = "",
    is_interactive: bool = False,
    sim_time: bool = False,
):
    """Launch remote-side subsystems by profile, token string, or interactively.

    Subsystems (use any unambiguous prefix): viz (dome_viz live map view),
    voice (dome_voice LLM node: Whisper and Claude), pad (rosbridge for the
    Yellow Pad's ROS tab, and pad_buttons: A asks the LLM for a robot joke).

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
        Passed to the included files that take it (viz).
    """
    # Literal "" default: bl parses the signature statically and can't evaluate names.
    launch_subsystems(profile or DEFAULT_PROFILE, options, is_interactive, LAUNCH_FILES)
