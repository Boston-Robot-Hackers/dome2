---
version: "1.1"
generated: "2026-07-08"
---

# Subsystem Launch Files: Control, Vision, Voice, and Drivers

The subsystem launch files in dome2 — `dome_control.launch.py`, `dome_vision.launch.py`,
`dome_voice.launch.py`, and `gendrv.launch.py` — are intentionally thin wrappers.
Their job is to delegate to the owning subsystem package; policy about *when* to launch
a subsystem lives in the top-level orchestrator (`robot.launch.py`), not here.

This separation keeps each file trivially auditable and makes the intent of the
`robot.launch.py` profile system legible without hunting through conditionals scattered
across multiple files.

## dome_control: Mode-Aware Control Delegation

Control is the one subsystem that has a meaningful mode distinction: the robot can run
locally (`robot.launch.py`) or remotely (`remote.launch.py`). That choice is expressed
once, at module level, via `DOME_MODE`.

```python
MODE = os.environ.get("DOME_MODE", "robot")

@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    launch_file = "remote.launch.py" if MODE == "remote" else "robot.launch.py"
    bl.include("dome_control", launch_file)
```

The ternary replaces the old `if/else` block. Because `MODE` is read once at import time
(a module-level constant), there is no risk of the environment changing between the check
and the `bl.include` call.

## dome_vision and dome_voice: Unconditional Wrappers

Vision and voice previously included mode guards (`DOME_MODE`, `DOME_CAMERA`). Those
guards were removed because the top-level orchestrator now decides whether to include
a subsystem at all. A wrapper that does nothing but `bl.include(…)` is still useful: it
gives the subsystem a stable ROS2 entry point that the orchestrator can reference by name.

```python
# dome_vision.launch.py
@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include("dome_vision_ros", "robot.launch.py")
```

```python
# dome_voice.launch.py
@launch_this(ui=True)
def start_nav():
    bl = BetterLaunch()
    bl.include("dome_voice", "robot.launch.py")
```

## gendrv: Hardware Driver Bringup

`gendrv.launch.py` brings up the physical robot: URDF, EKF config, serial port to the
ESP32 microcontroller, and the linorobot2 bringup stack.

```python
@launch_this(ui=True)
def start_nav():
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
```

The explicit keyword arguments serve as documentation of the non-default choices: no
RViz, no simulation, no joystick, no Madgwick filter. These are robot-specific policy
decisions that should be visible at a glance.

## Design Observations

- **Mode gating moved up.** The old pattern of each wrapper checking `DOME_MODE` before
  deciding to do anything created duplicated conditional logic and made the overall
  launch profile impossible to reason about in one place. Moving selection to
  `robot.launch.py` is cleaner.
- **`gendrv` is the one file with real config.** If hardware params change (port, baud
  rate, URDF path), this is the only file that needs updating.
- **`start_nav` naming is inherited.** All four files use `start_nav` as the function
  name even though most don't navigate. This is a `better_launch` convention; changing
  it would break the launcher decorator.
