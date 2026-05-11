# dome2

Top-level ROS2 launch orchestrator for the Dome robot. Composes the full system from
independent subsystem packages: drive/nav, vision (OAK-D + YOLO), voice control, and
Foxglove telemetry.

## System overview

```
dome2  (this package — launch orchestration only)
├── dome_control      — high-level robot control and CLI
├── dome_vision       — OAK-D camera + Roboflow YOLO inference
├── dome_voice        — wake-word → STT → intent → cmd_vel
├── linorobot2_bringup — base driver (ESP32 via micro-ROS), EKF, URDF
└── foxglove_bridge   — WebSocket telemetry on port 8765
```

## Launch files

| File | Purpose |
|---|---|
| `robot.launch.py` | Full system: all subsystems in one command |
| `dome_control.launch.py` | Drive/nav only (robot or remote mode) |
| `dome_vision.launch.py` | OAK-D vision pipeline only |
| `dome_voice.launch.py` | Voice control pipeline (robot mode only) |
| `foxglove.launch.py` | Foxglove bridge only |
| `gendrv.launch.py` | Base driver + EKF + URDF state publisher |

## Environment variables

| Variable | Default | Values |
|---|---|---|
| `DOME_MODE` | `robot` | `robot` — run on hardware; `remote` — run on laptop |
| `DOME_CAMERA` | `oak` | `oak` — OAK-D required |
| `ROBOFLOW_API_KEY` | _(none)_ | API key for Roboflow model download |

## Prerequisites

- ROS2 Humble
- `better_launch` package in workspace
- `linorobot2_bringup` in workspace
- `foxglove_bridge` installed
- Hardware: ESP32 base at `/dev/esp32`, OAK-D camera (for vision)

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select dome2
source install/setup.bash
```

## Usage

```bash
# Full robot bring-up
ros2 launch dome2 robot.launch.py

# Drive/nav only
ros2 launch dome2 dome_control.launch.py

# Vision only (requires OAK-D, DOME_MODE=robot)
ros2 launch dome2 dome_vision.launch.py

# Remote mode (laptop-side nav)
DOME_MODE=remote ros2 launch dome2 dome_control.launch.py
```

## Config files

| File | Purpose |
|---|---|
| `config/dome3.urdf` | Robot URDF description |
| `config/ekf.yaml` | `robot_localization` EKF parameters (50 Hz, 2D mode) |

## License

MIT — see [LICENSE](LICENSE)
