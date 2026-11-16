---
version: "1.1"
generated: "2026-08-05"
---

# Appendix: foxglove.launch.py

The Foxglove bridge provides a WebSocket server that exposes all ROS2 topics to the Foxglove Studio desktop/web app for visualization and monitoring.

```python
mode = os.environ.get("DOME_MODE", "robot")


@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include("foxglove_bridge", "foxglove_bridge_launch.xml", port="8765")
```

`DOME_MODE` is read but never used — the bridge runs regardless of mode. This makes sense: Foxglove is useful both on the robot (forwarding to a remote viewer) and on a dev machine. The dead variable is leftover from the file template.

Port `8765` is Foxglove's default WebSocket port. Connect Foxglove Studio to `ws://<robot-ip>:8765` to see live topic data, transforms, and camera feeds.

This file is included by `robot.launch.py` and can also be launched standalone when you want monitoring without the full robot stack.
