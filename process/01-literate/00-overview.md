---
version: "2.0"
generated: "2026-11-19"
---

# dome2: Theory of Operation

## What This Package Is

`dome2` is the top-level orchestration package for DOME, a ROS 2 differential-drive robot with voice control, computer vision and autonomous navigation.

It holds **no nodes**. Its job is composition: deciding which subsystem packages start, on which computer, in which combination.

The packages that do the real work:

| Package | Responsibility |
|---------|---------------|
| `linorobot2_bringup` | Hardware drivers: micro-ROS bridge to the ESP32, EKF odometry fusion |
| `dome_nav` | SLAM mapping (the `slam` subsystem) |
| `dome_semantic` | The semantic map (the `semantic` subsystem) |
| `dome_control` | Behaviour manager, telemetry, spin survey |
| `dome_vision_ros` | OAK-D camera and object detection |
| `dome_voice` | Wake word, speech input and speech output |
| `foxglove_bridge` | WebSocket bridge for Foxglove on the remote computer |
| `dome_telemetry` | Battery telemetry |
| `yellow_pad` | Joystick teleop |
| `dome_viz` | Live map view, on the remote computer |

## The Two-Level Rule

Since F05 (2026-11), the whole stack follows one convention, written up in `stack/launch_conventions.md`:

- **A package's own launch file starts only that package's nodes.**
- **Only dome2 combines packages.**

So dome2 no longer has a wrapper file per subsystem. Its launchers point **straight at each package's `robot.launch.py`** (or `remote.launch.py`). The one launch file dome2 still owns is `drivers.launch.py`, because dome2 owns the driver configuration: the URDF and `ekf.yaml`.

## How to Read This Document

The chapters go from foundations to the top:

1. **Architecture** — better_launch, and how the pieces are wired
2. **Hardware bringup** — `drivers.launch.py`, the drivers everything else depends on
3. **Subsystems** — what each `LAUNCH_FILES` entry starts
4. **Orchestrators** — `robot.launch.py` and `remote.launch.py`: profiles, tokens, interactive mode
5. **Stack tools** — the helper scripts

## Quickstart

On the robot, choose subsystems by prefix:

```bash
cd ~/ros2_ws && source install/setup.bash
bl dome2 robot.launch.py --options "d c vi"    # drivers + control + vision
```

Or set a profile once and launch with no arguments:

```bash
export robot="d c vi vo f"
bl dome2 robot.launch.py
```

On the remote computer:

```bash
bl dome2 remote.launch.py --options "v"        # dome_viz map view
```

Connect Foxglove to `ws://<robot-ip>:8765` to see the topics live.

## Key Design Decisions

- **Selection lives in one place.** Which subsystems run is decided by `robot.launch.py`'s table and the token string, not by guards scattered through wrapper files. The old `DOME_MODE` variable is gone: the choice of computer is the choice of launcher.
- **Configuration lives in the subsystem.** Each package finds its own installed config with `bl.find` (`stack/config_conventions.md`). dome2 passes no config paths and reads no config-path environment variables.
- **The environment holds only profiles and secrets.** `DOME_PROFILE`, `DOME_REMOTE_PROFILE` and the profile variables they name select subsystems. `ROBOFLOW_API_KEY` stays out of argument lists and logs.
