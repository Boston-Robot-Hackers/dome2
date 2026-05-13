#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
import logging

from better_launch import BetterLaunch, launch_this

mode = os.environ.get("DOME_MODE", "robot")
camera = os.environ.get("DOME_CAMERA", "oak")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    if mode != "robot" or camera != "oak":
        logging.info(
            "Skipping dome_vision launch: DOME_MODE=%s, DOME_CAMERA=%s; robot mode with oak camera is required",
            mode,
            camera,
        )
        return
    bl.include(
        "dome_vision_ros",
        "robot.launch.py",
    )
