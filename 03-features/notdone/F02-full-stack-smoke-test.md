# F02 — Full-Stack Smoke Test

**Priority**: High
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: A repeatable, ordered bring-up procedure that walks the entire
real-robot stack up in stages — dome2 drivers, dome2 control, dome_nav
(SLAM + Nav2 + explorer), dome_mission (`mission_node`) — checking each stage
against its expected nodes/topics/actions before advancing to the next. Lets
an operator on the Pi find out exactly which layer broke since the stack last
ran end-to-end, instead of launching everything at once and guessing.

Not a CI test (needs real hardware and, for later stages, actual motor
motion); it is an operator-run tool. Health checks and the stage list are
pure/testable in isolation; the orchestration loop itself is runtime-only.

## Stages

| # | stage | brings up | how (existing launch files) |
|---|---|---|---|
| 1 | drivers | ESP32 base, IMU, lidar, EKF odom | `dome2 gendrv.launch.py` |
| 2 | control | `behavior_manager`, `telemetry_node`, `spin_survey_node` | `dome2 dome_control.launch.py` |
| 3 | nav | `slam_toolbox`, Nav2, `slam_manager_node`, `explorer_manager_node` | `dome_nav robot_map.launch.py` or `robot_explore.launch.py` (operator picks mapping vs. explore) |
| 4 | mission | `mission_node` (`/intent` front end, `ExploreArea` client) | `ros2 run dome_mission mission_node` |

Vision/voice/foxglove are out of scope for this feature — `dome_semantic`'s
`/semantic/targets` publisher isn't built yet (dome_mission I-note), so
anything downstream of it has nothing to verify.

## Behavior per stage

1. Launch the stage.
2. Wait for a settle time, then collect `ros2 node list` / `topic list` /
   `action list`.
3. Compare against that stage's expected set; report pass/fail and what's
   missing.
4. Pause for operator confirm before advancing (reuses the confirm-prompt
   pattern already used by `robot.launch.py --is_interactive`); on fail, stop
   and leave prior stages running so the operator can inspect them.

## How to Demo

**Setup**: robot on the floor or a stand, clear space, charged, e-stop
reachable; workspace built and sourced; `bl` available; a `map_name` decided
(existing map to re-verify localization, or a new name for a fresh mapping
run).

**Steps**:
1. Run the smoke-test tool with no stage filter — it starts at "drivers" and
   pauses after each stage's check.
2. At each pause, confirm to advance or stop to inspect a failing stage.
3. Reach stage 4 ("mission") and confirm `mission_node` is the sole
   `/intent` subscriber and `ExploreArea` client.

**Expected output**: a per-stage pass/fail report; on full success, all four
stages report pass and the operator can confidently send a real `/intent`
next (a follow-up, not part of this feature).
