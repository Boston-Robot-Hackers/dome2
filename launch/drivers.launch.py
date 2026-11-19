#!/usr/bin/env python3
# drivers.launch.py — hardware driver bringup for the DOME robot
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-19
# Updated: 2026-11-19
# Open Source Under MIT license
#
# Usage:
#   bl dome2 drivers.launch.py                      # the drivers alone
#   bl dome2 robot.launch.py --options "d"          # via the "drivers" subsystem
"""Start linorobot2_bringup with dome2's URDF and EKF config.

That brings up the micro-ROS agent for the ESP32 on /dev/esp32, the EKF and
robot_state_publisher. dome2 owns this file, rather than a subsystem package,
because dome2 owns `dome3.urdf` and `ekf.yaml`. It runs only on the robot:
nothing else lists it.
"""

from better_launch import BetterLaunch, launch_this


@launch_this(ui=True)
def drivers_launch():
    """Start the hardware drivers. Takes no arguments."""
    bl = BetterLaunch()
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
        urdf=bl.find("dome2", "dome3.urdf"),
        ekf_config_path=bl.find("dome2", "ekf.yaml"),
    )
