#!/usr/bin/env python3
# remote.launch.py — dome2 launcher for the remote computer's side of the stack
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-16
# Updated: 2026-11-16
# Open Source Under MIT license
#
# Examples:
#   bl dome2 remote.launch.py                        # use $DOME_REMOTE_PROFILE env var
#   bl dome2 remote.launch.py --options "v"          # dome_viz map view
#   bl dome2 remote.launch.py --is_interactive       # confirm each subsystem
"""Remote-computer counterpart of `robot.launch.py`, with the same interface.

Subsystems that run off the robot are listed here. It starts with only
dome_viz; functions moved off the robot get an entry here.
"""

import os

from better_launch import launch_this

from dome2.subsystem_launcher import launch_subsystems

# Ordered: this order is the interactive prompt order and the include order.
LAUNCH_FILES = {
    "viz": ("dome_viz", "view.launch.py"),
}

SUBSYSTEMS = list(LAUNCH_FILES)

DEFAULT_PROFILE = os.environ.get("DOME_REMOTE_PROFILE", "remote")


@launch_this(ui=True)
def start_remote(
    profile: str = "",
    options: str = "",
    is_interactive: bool = False,
):
    """Launch remote-side subsystems by profile, token string, or interactively.

    Subsystems (use any unambiguous prefix): viz (dome_viz live map view).

    Parameters
    ----------
    profile : str
        Env var name whose value is a token string. Default: $DOME_REMOTE_PROFILE,
        else the env var named `remote`.
    options : str
        Space-separated subsystem token prefixes. Overrides profile.
    is_interactive : bool
        Prompt yes/no for each subsystem before launching.
    """
    # Literal "" default: bl parses the signature statically and can't evaluate names.
    launch_subsystems(profile or DEFAULT_PROFILE, options, is_interactive, LAUNCH_FILES)
