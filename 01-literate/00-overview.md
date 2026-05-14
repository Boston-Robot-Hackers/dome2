---
version: "1.0"
generated: "2026-05-12"
---

# dome2: Theory of Operation

## What This Package Is

`dome2` is the top-level orchestration package for the Dome robot — a ROS2-based differential-drive robot with voice control, computer vision, and autonomous navigation. The package contains no nodes of its own. Its entire purpose is launch-file composition: wiring together the subsystem packages that do the real work.

The name `dome2` reflects a generational convention. Earlier iterations lived in a `dome` package that holds the robot's physical description (URDF, sensor configs). `dome2` is the second-generation orchestration layer.

## Theory of Operation

The robot's software is organized into independent subsystem packages:

| Package | Responsibility |
|---------|---------------|
| `linorobot2_bringup` | Hardware drivers — micro-ROS bridge to ESP32, EKF odometry fusion |
| `dome_control` | Navigation and motion control |
| `dome_voice` | Speech input and output |
| `dome_vision_ros` | OAK-D camera, object detection via Roboflow |
| `foxglove_bridge` | WebSocket bridge for remote visualization |

`dome2` sits above all of these. It provides one launch file per subsystem (for selective bringup) plus a single top-level `robot.launch.py` that composes everything into a running robot.

## How to Read This Document

The chapters follow dependency order — foundational first, highest-level last:

1. **Architecture** — the `BetterLaunch` abstraction and `DOME_MODE` environment variable that thread through every launch file
2. **Hardware Bringup** — `gendrv.launch.py`, which starts the ESP32 hardware drivers and is a prerequisite for everything else
3. **Subsystem Launches** — the three mid-level launch files (control, voice, vision) and their mode constraints
4. **Robot Orchestrator** — `robot.launch.py`, the single entry point that composes all of the above

## Quickstart

Full robot on the robot hardware:

```bash
DOME_MODE=robot ros2 launch dome2 robot.launch.py
```

Remote machine (control only, no vision/voice hardware):

```bash
DOME_MODE=remote ros2 launch dome2 robot.launch.py
```

Connect Foxglove Studio to `ws://<robot-ip>:8765` to monitor all topics live.

## Key Design Decisions

**Environment variables over launch arguments.** `DOME_MODE`, `DOME_CAMERA`, and `ROBOFLOW_API_KEY` are read from the shell environment rather than passed as ROS2 launch arguments. This keeps the launch invocation simple and keeps secrets (API keys) out of process argument lists and logs.

**Soft mode guards.** Each subsystem checks preconditions and prints warnings, but does not hard-abort when conditions aren't met. Failed subsystems surface as runtime errors rather than launch-time rejections. This is pragmatic for a robot platform under active development.

**Delegation, not duplication.** Each `dome2` launch file is a one-screen delegation to a subsystem package. Configuration lives in the subsystem, not in `dome2`. When you need to understand how control works, read `dome_control` — `dome2` only decides whether to start it.
