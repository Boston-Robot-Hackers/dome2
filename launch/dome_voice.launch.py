#!/usr/bin/env python3
# dome_voice.launch.py — voice subsystem wrapper for dome2
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from better_launch import BetterLaunch, launch_this


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include("dome_voice", "robot.launch.py")
