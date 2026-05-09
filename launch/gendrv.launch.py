#!/usr/bin/env python3
# This is my version of launching the slam launch file from linorobot2

import os
from better_launch import BetterLaunch, launch_this

mode=os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    if mode != "robot":
        print("Not in robot mode, skipping nav launch")
    urdf_path = bl.find("dome", "dome3.urdf")
    ekf_config_path = bl.find("dome", "ekf.yaml")
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
