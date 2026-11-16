---
version: "1.1"
generated: "2026-05-13"
---

# Hardware Bringup: gendrv.launch.py

## The Role of gendrv

`gendrv.launch.py` is the lowest-level launch file in `dome2`. It starts the hardware drivers — the nodes that talk directly to physical devices. Everything else in the robot depends on what this file brings up.

"gendrv" is short for *generic driver* (or possibly *general driver*), reflecting that this file configures a general-purpose hardware bringup stack rather than a custom one. The actual work is delegated to `linorobot2_bringup`, a community ROS2 package for differential-drive robots.

## Mode Guard

```python
mode = os.environ.get("DOME_MODE", "robot")

@launch_this(ui=True)
def start_nav():
    if mode != "robot":
        logging.warning("DOME_MODE != robot, skipping hardware driver bringup")
        return
    bl = BetterLaunch()
```

Hardware can only be launched on the robot itself. If `DOME_MODE` is not `robot`, the function logs a warning and returns early — `linorobot2_bringup` is never started. This is important because the bringup tries to open serial devices that don't exist on a dev machine. The early `return` before constructing `BetterLaunch` ensures no partial launch state is created.

## Path Resolution

Two external config files must be resolved to absolute paths before being passed as launch arguments:

```python
urdf_path = bl.find("dome2", "dome3.urdf")
ekf_config_path = bl.find("dome2", "ekf.yaml")
```

These files live in the `dome2` package itself. `bl.find()` resolves them to the installed share path at launch time rather than at package build time, so the paths survive `colcon build` reinstalls.

## The linorobot2_bringup Arguments

```python
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

Each argument reflects a deliberate hardware decision:

| Argument | Value | Why |
|----------|-------|-----|
| `rviz` | `False` | No display on the robot; visualization runs remotely via Foxglove |
| `sim` | `False` | Real hardware, not Gazebo |
| `base_serial_port` | `/dev/esp32` | Robot base MCU is an ESP32, connected via USB serial with a udev rule that gives it this stable name |
| `micro_ros_baudrate` | `921600` | High baud rate for micro-ROS; must match firmware setting |
| `madgwick` | `false` | Madgwick filter disabled — IMU fusion is handled by the EKF instead |
| `orientation_stddev` | `0.01` | Low orientation noise assumption; tuned for the robot's IMU quality |
| `joy` | `false` | Joystick input disabled; robot is commanded via software, not a gamepad |
| `urdf` | resolved path | Robot model used by `robot_state_publisher` |
| `ekf_config_path` | resolved path | Extended Kalman Filter config for odometry + IMU fusion |

## The ESP32 / micro-ROS Architecture

```mermaid
graph LR
    ESP32["ESP32<br/>/dev/esp32<br/>921600 baud"]
    microros["micro-ROS agent<br/>(linorobot2_bringup)"]
    ekf["robot_localization EKF<br/>(ekf.yaml)"]
    odom["/odom topic"]
    imu["/imu/data topic"]
    
    ESP32 -->|"micro-ROS serial"| microros
    microros --> odom
    microros --> imu
    odom --> ekf
    imu --> ekf
    ekf --> |"/odometry/filtered"| ROS2[ROS2 Nav Stack]
```

The ESP32 runs micro-ROS firmware that publishes wheel odometry and IMU data. The `linorobot2_bringup` launch starts a micro-ROS agent that bridges the serial connection into ROS2 topics. The EKF then fuses odometry and IMU to produce a filtered pose estimate used by navigation.

Disabling Madgwick (`madgwick=false`) means orientation from the IMU goes directly into the EKF rather than through a separate complementary filter — the EKF itself handles sensor fusion, which is cleaner when the EKF is already tuned for the IMU's noise characteristics.
