#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this

@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include(
        "dome2",
        "gendrv.launch.py",
    )
    bl.include(
        "dome2",
        "dome_control.launch.py"
    )
    bl.include(
        "dome2",
        "foxglove.launch.py"
    )
    bl.include(
        "dome2",
        "dome_vision.launch.py"
    )
    bl.include(
        "dome2",
        "dome_voice.launch.py"
    )

    