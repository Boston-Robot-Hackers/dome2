#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this

mode=os.environ.get("DOME_MODE", "robot")

@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    if not (mode == "robot"):
        print("Robot mode required because voice control is only onboard. Exiting")
    bl.include(
        "robot_voice",
        "robot.launch.py",
    )