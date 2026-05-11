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
        "control.launch.py"
    )
    bl.include(
        "dome2",
        "foxglove.launch.py"
    )
    bl.include(
        "dome2",
        "oak_roboflow.launch.py"
    )
    bl.include(
        "dome2",
        "robot_voice.launch.py"
    )

    