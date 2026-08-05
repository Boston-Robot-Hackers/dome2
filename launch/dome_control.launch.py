#!/usr/bin/env python3
# dome_control.launch.py — control subsystem wrapper for dome2
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import os

from better_launch import BetterLaunch, launch_this

MODE = os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    launch_file = "remote.launch.py" if MODE == "remote" else "robot.launch.py"
    bl.include("dome_control", launch_file)
