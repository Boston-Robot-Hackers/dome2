#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this

mode=os.environ.get("DOME_MODE", "robot")

@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    if mode == "remote":
        launch_file = "remote.launch.py"
    else:
        launch_file = "robot.launch.py"
    print(f"********** Launching control with mode {mode} and launch file {launch_file} ")
    bl.include(
        "control",
        launch_file,
        )
    
