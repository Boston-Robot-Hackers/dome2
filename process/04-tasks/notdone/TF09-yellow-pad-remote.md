# TF09 The Yellow Pad as dome_pad, for Feature F09

**Date Created:** 2026-11-22

Most of this work is in the new `dome_pad` repo (`~/mydev/dome_pad` on the
Mac), cloned from `yellow_pad` so the firmware keeps its history. dome2
changes its launch tables, the stack registry and the docs that list
packages.

## TF09.0 — Create the dome_pad repo and package

**Status**: done (2026-11-22)

**Description**: Clone `yellow_pad`, then restructure: the ROS package moves
to the repo root as ament_python (`setup.py`, `setup.cfg`,
`resource/dome_pad`), `config/yellow_pad.yaml` becomes `config/pad.yaml`,
`NOTES.md` becomes `process/02-doc/notes.md`, and `arrows_v1.cpp` with its
`cyd_v1` env is dropped. Add the j3 process kit (`.claude/`, `process/`,
`CLAUDE.md`, `ruff.toml`, `.githooks/pre-commit`), MIT `LICENSE`, and a
spec. `package.xml` exec-depends on `rclpy`, `std_msgs`, `sensor_msgs`,
`joy`, `teleop_twist_joy` and `rosbridge_server`. Create
`Boston-Robot-Hackers/dome_pad` on GitHub and push.

**Test**: `colcon build --packages-select dome_pad`, then
`ros2 pkg executables dome_pad` lists `pad_buttons`. Manual, on the VM, in
TF09.6. The firmware builds on the Mac (`pio run`: success, 2026-11-22).

## TF09.1 — Button logic, ROS-free

**Status**: done (2026-11-22)

**Description**: `dome_pad/pad_buttons.py`. `BUTTON_TEXTS` maps a joy
button index to the text it sends (`1: "Tell me a robot joke."`).
`ButtonPresses.update` takes each button array and returns the texts for
mapped buttons that went from released to pressed. A `/joy` array shorter
than the largest mapped index raises with the length.

**Test**: `test/test_pad_buttons.py` (9 tests): a press fires once; holding
doesn't repeat; release then press fires again; unmapped buttons do nothing;
a button down in the first message fires; two new presses fire in index
order; a too-short array raises; A asks for a robot joke; button 0 (the
dead-man button) is never mapped. Passing on the Mac.

## TF09.2 — `pad_buttons` node

**Status**: done (2026-11-22)

**Description**: `dome_pad/pad_buttons_node.py`. Subscribes to `/joy`
(`sensor_msgs/Joy`) and publishes each text from `ButtonPresses.update` on
`/voice/llm_text` (`std_msgs/String`). Clean stop per the launch
conventions (`ExternalShutdownException`, `destroy_node`,
`rclpy.try_shutdown`).

**Test**: `test/test_pad_buttons_node.py` (4 tests) with conftest's fake
rclpy: a held A publishes exactly one String with the joke text; a
dead-man-only message publishes nothing; `main()` stops cleanly on
`ExternalShutdownException` and Ctrl-C. Passing on the Mac. Skipped where
real rclpy is installed.

## TF09.3 — Package launch files

**Status**: done (2026-11-22)

**Description**: Two better_launch files following
`stack/launch_conventions.md`:
- `robot.launch.py`: `joy_node` and `teleop_twist_joy`'s `teleop_node`,
  with `config/pad.yaml`. **The old `cmd_vel` remap argument is dropped**:
  dome2 never passed it, and the conventions keep only demonstrated
  configurations.
- `remote.launch.py`: rosbridge (`rosbridge_server`'s
  `rosbridge_websocket_launch.xml`) and `pad_buttons`.

README and `process/02-doc/notes.md` updated to match.

**Test**: dome2's `test/test_launch_conventions.py` passes for both files
(on the Mac, 2026-11-22). Running them is TF09.6.

## TF09.4 — dome2: register and launch dome_pad

**Status**: done (2026-11-22)

**Description**:
- `launch/robot.launch.py`: `yellow` → `pad` = `("dome_pad", "robot.launch.py")`.
- `launch/remote.launch.py`: add `pad` = `("dome_pad", "remote.launch.py")`.
- `package.xml`: exec-depend on `dome_pad` instead of `yellow_pad`.
- `stack/packages.yaml`: add `dome_pad`, `runs_on: both`; the tables in
  `process/02-doc/spec.md` and `stack/README.md` to match. `README.md`'s
  subsystem tables.
- `stack/launch_inventory.md`: a dome_pad section.
- Literate chapters 00, 01, 03 and 04: `yellow` → `pad`, and the remote
  table with `voice` and `pad`. `literate.pdf` not regenerated.

**Test**: `test_launch_profiles.py` and `test_stack_registry.py` updated
(13 packages; `p` resolves to `pad` on both launchers; both `pad` targets).
On the Mac the suite has the same 23 failures before and after this change,
all from stale or missing checkouts of other packages; 7 more tests pass.

## TF09.5 — Firmware: ROS tab points at the VM

**Status**: done in source (2026-11-22); not flashed

**Description**: `secrets.h.sample` names the remote computer (the VM,
192.168.4.83) as `ROSBRIDGE_HOST`, not the Pi; the user's git-ignored
`secrets.h` in dome_pad is set the same way. Flash with
`cd firmware && uvx --from platformio pio run -t upload`.

**Test**: manual. It's hardware; covered by the demo's step 2.

## TF09.6 — Run on the robot and the VM

**Status**: in progress

**Results so far**:
- 2026-11-22: firmware flashed (1314224 bytes, hash verified). With rosbridge
  not yet started, the ROS tab sat at "Connecting to 192.168.4.83..."; the
  Mac confirmed port 9090 refused. After the VM side was started, **the ROS
  tab connects** (user), and port 9090 accepts from the Mac.
- Still to record: driving through `pad` on the Pi, and button A
  (`/voice/llm_text`, `/voice/llm_reply`, `/announcement`).

**Description**: On both computers: `make pull` (dome_voice must have F14's
`llm_node`), `make clone` for dome_pad, `rosdep install`, `colcon build`.
On the Pi, remove `~/ros2_ws/src/yellow_joy` first. Run both test suites,
then the F09 demo, and record the commands and results here.

**Test**: this task is the test run. The demo is manual (Bluetooth,
speaker, motion).
