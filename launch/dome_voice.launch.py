#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
import logging

from better_launch import BetterLaunch, launch_this

mode = os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    if mode != "robot":
        logging.info("Skipping dome_voice launch: DOME_MODE=%s, robot mode is required", mode)
        return
    bl.include(
        "dome_voice",
        "robot.launch.py",
    )
