#!/usr/bin/env python3
# gendrv.launch.py — hardware driver bringup for dome2 robot
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import logging
import os

from better_launch import BetterLaunch, launch_this

mode = os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    if mode != "robot":
        logging.warning("DOME_MODE != robot, skipping hardware driver bringup")
        return
    bl = BetterLaunch()
    urdf_path = bl.find("dome2", "dome3.urdf")
    ekf_config_path = bl.find("dome2", "ekf.yaml")
    bl.include(
        "linorobot2_bringup",
        "bringup.launch.py",
        rviz=False,
        sim=False,
        base_serial_port="/dev/esp32",
        micro_ros_baudrate="921600",
        madgwick="false",
        orientation_stddev="0.01",
        joy="false",
        urdf=urdf_path,
        ekf_config_path=ekf_config_path,
    )
