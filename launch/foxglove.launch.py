#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this

mode=os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include(
        "foxglove_bridge",
        "foxglove_bridge_launch.xml",
        port="8080"
    )
