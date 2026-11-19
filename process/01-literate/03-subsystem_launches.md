---
version: "2.0"
generated: "2026-11-19"
---

# Subsystems: What Each Entry Starts

## No more wrappers

Until 2026-11-19, dome2 had a thin wrapper file per subsystem: `dome_control.launch.py`, `dome_vision.launch.py`, `dome_voice.launch.py` and `foxglove.launch.py`. Each did little more than `bl.include(...)` another package's file. Some also read `DOME_MODE`.

F05 deleted all four. **`robot.launch.py`'s table now names the package files directly:**

```python
LAUNCH_FILES = {
    "drivers": ("dome2", "gendrv.launch.py"),
    "control": ("dome_control", "robot.launch.py"),
    "vision": ("dome_vision_ros", "robot.launch.py"),
    "voice": ("dome_voice", "robot.launch.py"),
    "foxglove": ("foxglove_bridge", "foxglove_bridge_launch.xml"),
    "battery": ("dome_telemetry", "robot.launch.py"),
    "yellow": ("yellow_pad", "yellow_pad.launch.py"),
}
```

### Why the wrappers went

- **They added a hop and nothing else.** Reading a wrapper told you nothing the table couldn't.
- **They hid mode logic.** `DOME_MODE` checks were spread over several files. With one table per computer, the check isn't needed.
- **They made each package's file name a second time.** Every rename had to be made twice.

## What each subsystem starts

| Token | Starts | Config |
|---|---|---|
| `drivers` | `linorobot2_bringup`: micro-ROS agent, EKF, `robot_state_publisher` (chapter 2) | `dome3.urdf`, `ekf.yaml` in dome2 |
| `control` | `behavior_manager`, `telemetry`, `spin_survey` | `spin_survey.yaml` in dome_control |
| `vision` | `dome_vision`, a lifecycle node driven to `active` | `roboflow_oak.yaml` in dome_vision_ros |
| `voice` | `voice_input`, `speech_output` | `voice.yaml` in dome_voice |
| `foxglove` | the Foxglove WebSocket bridge, on port 8765 | the bridge's defaults |
| `battery` | battery telemetry | in dome_telemetry |
| `yellow` | Yellow Pad joystick teleop | in yellow_pad |

**Each package finds its own config** with `bl.find`, per `stack/config_conventions.md`. dome2 passes none of these paths.

### Two entries worth a note

- **`foxglove` includes the bridge's XML launch file directly.** The old wrapper passed `port="8765"`, which is the bridge's own default, so nothing is lost.
- **`control` includes `spin_survey`.** It sits idle until something calls `/survey/start`; dome_control's command-line `survey` command is the only caller. It can still publish `/cmd_vel` once started, like any controller.

## Selecting them

Tokens are unique prefixes of these names (chapter 4):

```bash
bl dome2 robot.launch.py --options "d c"     # drivers + control
bl dome2 robot.launch.py --options "d vi"    # drivers + vision
bl dome2 robot.launch.py --options "vo"      # voice alone
```

Each package's file also runs on its own, which is the fastest way to test one subsystem:

```bash
bl dome_vision_ros robot.launch.py --depth false
```

## Observations

1. **One file per package is now the only way in.** Variants (raw images, experiment setups) are arguments of that file, not extra files.
2. **Subsystem arguments can't be set from dome2 yet.** `bl dome2 robot.launch.py` has no way to pass `--depth false` through to vision. TF05.4 adds pass-through for `--sim_time` and `--map_name`.
3. **Startup isn't sequenced.** Every selected subsystem starts at once, so the OAK's highest current draw coincides with every other node's startup (dome_vision I02).
