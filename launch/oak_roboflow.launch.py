#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this

mode=os.environ.get("DOME_MODE", "robot")
camera=os.environ.get("DOME_CAMERA", "oak")
roboflow=os.environ.get("ROBOFLOW_API_KEY", None)

@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    if not (mode == "robot" and camera == "oak"):
        print("Oak camera and robot mode required. Exiting")
    bl.include(
        "oak_roboflow_ros",
        "robot.launch.py",
    )

