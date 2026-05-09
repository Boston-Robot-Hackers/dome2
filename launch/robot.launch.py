#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this
mode=os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include(
        "dome2",
        "gendrv.launch.py",
        port="8080",
        mode=mode,
    )
    bl.include(
        "dome2",
        "foxglove.launch.py"
    )
    