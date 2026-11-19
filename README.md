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

dome2 owns only the top-level launchers and the driver bringup. Every other subsystem is a package's own `robot.launch.py`, included directly ([`stack/launch_conventions.md`](stack/launch_conventions.md)).

| File | Purpose |
|---|---|
| `robot.launch.py` | The robot: chosen subsystems in one command |
| `remote.launch.py` | The remote computer: the `viz` subsystem (dome_viz) |
| `gendrv.launch.py` | Base driver + EKF + URDF state publisher (the `drivers` subsystem) |

`robot.launch.py`'s subsystems, chosen with `--options` (any unambiguous prefix):

| Subsystem | Launches |
|---|---|
| `drivers` | `dome2 gendrv.launch.py` |
| `control` | `dome_control robot.launch.py` |
| `vision` | `dome_vision_ros robot.launch.py` |
| `voice` | `dome_voice robot.launch.py` |
| `foxglove` | `foxglove_bridge foxglove_bridge_launch.xml` (port 8765) |
| `battery` | `dome_telemetry robot.launch.py` |
| `yellow` | `yellow_pad yellow_pad.launch.py` |

## Environment variables

| Variable | Default | Values |
|---|---|---|
| `DOME_PROFILE` | `robot` | name of an env var holding a subsystem token string |
| `DOME_CAMERA` | `oak` | `oak` — OAK-D required |
| `ROBOFLOW_API_KEY` | _(none)_ | API key for Roboflow model download |

Config files are not chosen by environment variable ([`stack/config_conventions.md`](stack/config_conventions.md)).

## Prerequisites

- ROS 2 Kilted
- `better_launch` package in workspace
- `linorobot2_bringup` in workspace
- `foxglove_bridge` installed
- Hardware: ESP32 base at `/dev/esp32`, OAK-D camera (for vision)

## Build

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select dome2
source install/setup.bash
```

## Usage

```bash
bl dome2 robot.launch.py --options "d c vi"   # drivers + control + vision
bl dome2 robot.launch.py --options "d f"      # drivers + Foxglove bridge
bl dome2 robot.launch.py                      # subsystems from $DOME_PROFILE
bl dome2 remote.launch.py --options "v"       # on the remote computer: the viewer
```

## Config files

| File | Purpose |
|---|---|
| `config/dome3.urdf` | Robot URDF description |
| `config/ekf.yaml` | `robot_localization` EKF parameters (50 Hz, 2D mode) |

## License

MIT — see [LICENSE](LICENSE)
