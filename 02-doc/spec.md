# dome2 — Spec

dome2 is the top-level ROS2 launch orchestrator for the Dome robot system.
It composes subsystem launch files for dome_control, dome_voice, dome_vision,
base drivers, EKF, URDF state publisher, and Foxglove telemetry.

## Scope

- Launch orchestration only — no robot logic lives here.
- Supports robot-mode and remote-mode launch variants.
- Gated subsystem launches skip cleanly when hardware is absent.

## Subsystems composed

| Package | Role |
|---|---|
| dome_control | CLI, intent routing, robot movement, behavior manager |
| dome_voice | Wake word, offline STT, intent mapping, speech output |
| dome_vision | OAK-D vision, ROS bridge, semantic map, scene services |
| linorobot2_bringup | Base driver and EKF |
| foxglove_bridge | Telemetry visualization |

## Key ROS interfaces

See `02-doc/dome_developer_onboarding.md` for full topic/service/message reference.
