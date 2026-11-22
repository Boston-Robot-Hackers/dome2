# dome2 — Spec

dome2 is the hub for the DOME software stack. It is checked out and built
on both the robot and the remote computer.

## Scope

- **Launch orchestration.** `robot.launch.py` on the robot and
  `remote.launch.py` on the remote computer, both choosing subsystems with
  the same `--profile` / `--options` / `--is_interactive` interface. No
  robot logic lives here.
- **Global vs package launch files.** A DOME package's launch files start
  only its own nodes, plus any outside (non-DOME) packages they need. They
  never include another DOME package. Anything that combines DOME packages
  is *global* and lives in dome2. That includes the **simulation** of the
  DOME stack on the remote computer.
- **Stack registry.** `stack/packages.yaml` lists every DOME package, its
  repo, and where it runs (`robot`, `remote` or `both`).
- **Cross-package operations.** Tools that act on every package in the
  registry, on either computer: `make clone` and `make pull`.
- **Stack-wide knowledge.** `stack/` holds docs about the whole stack, robot
  and remote. `stack/README.md` is the entry point for agents asked for an
  architectural critique.
- Subsystem launches skip cleanly when hardware is absent.

## Registered packages

| Package | Runs on | Role |
|---|---|---|
| dome2 | both | Stack hub: launchers, registry, cross-package tools, stack docs |
| dome_control | robot | CLI, intent routing, robot movement, behavior manager |
| dome_mission | robot | Mission sequencing; owns `/intent` and composes nav primitives |
| dome_nav | robot | SLAM, map persistence, localization, Nav2 configuration |
| dome_nav_msgs | robot | `ExploreArea` action |
| dome_pad | both | Yellow Pad gamepad: firmware, joy + teleop on the robot, rosbridge + button actions on the remote |
| dome_semantic | both | Semantic map: confirmed object targets in the `map` frame |
| dome_semantic_msgs | both | `SemanticTarget` / `SemanticTargetArray` messages |
| dome_telemetry | robot | Battery telemetry from the INA219 UPS |
| dome_telemetry_msgs | both | `BatteryStats` / `OakStats` messages |
| dome_vision | robot | OAK-D object detection and its ROS bridge |
| dome_viz | remote | Read-only web view of the map as it is built |
| dome_voice | both | Wake word, STT, intent mapping, speech output on the robot; the LLM node (Whisper, Claude) on the remote |

dome2 also launches non-DOME packages: `linorobot2_bringup` (base driver and
EKF) and `foxglove_bridge`. They are not in the registry.

## Key ROS interfaces

See `stack/dome_developer_onboarding.md` for the full topic, service and
message reference.
