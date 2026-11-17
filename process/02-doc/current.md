# Current Status — dome2

## Open

### Pick up here (2026-11-17)

**F05 TF05.2 is in progress, and TF05.6 is written early.** Details are in
`process/04-tasks/notdone/TF05-launch-file-cleanup.md`.

- **dome_control: done and verified on the robot.** `spin_survey`'s params
  moved to `config/spin_survey.yaml`. Two unused `mapper_params*` copies
  were deleted (chore).
- **dome_mission: skipped.** Its only file is blocked on I13 and F19.
- **dome_nav: done in code, not yet run.** `robot_map.launch.py` became
  `robot.launch.py --mode slam --map_name <name> [--sim_time]`, with no
  Nav2.
- **TF05.6:** `test/test_launch_conventions.py`. Unconverted files are
  strict xfails in `NOT_YET_CONVERTED`; remove each entry as its repo is
  fixed.
- **slam_toolbox activation stall:** 4 of 31 starts failed. The evidence is
  in `dome_nav` I13; the likely cause is a Fast DDS discovery race. A
  check-and-activate helper was rejected as a kludge; no fix is chosen.
- **The installed `robot_map.launch.py` is stale.** colcon doesn't delete
  files that were removed from the source tree. The clean rebuild after the
  upgrade clears it.

### Next

1. **Upgrade the Kilted apt packages on the Pi and the VM.** 303 are
   pending, including Fast DDS 3.2.5 and foxglove_bridge 3.5.0. Save a
   `dpkg -l 'ros-kilted-*'` snapshot first. Then clean-rebuild the
   workspace, and re-test `d c`, `d f`, `d vi`, `d b` and dome_nav's
   `robot.launch.py`, starting slam_toolbox several times.
2. **Run dome_viz's `test_main_shutdown.py` on the VM**, because the Pi has
   no `aiohttp`. It is the last check of the shutdown fix. The dome_control
   nodes stop cleanly on the robot (2026-11-17).
3. **F05, TF05.2**: carry on with dome_semantic (`semantic.launch.py` →
   `robot.launch.py`), then dome_telemetry, dome_vision, dome_viz and
   dome_voice. Remove each from `NOT_YET_CONVERTED` as it is done.
4. **F06, TF06.0** on the VM. Approved, but don't start until the user says so.
5. **Move the power load test here from `dome_semantic`.** Files:
   `tools/power_load_test.sh`, `tools/power_summary.awk`,
   `test/test_power_load_test.py`, `process/02-doc/power_testing.md`. See
   `dome_semantic`'s `current.md` for the references to update. It overlaps
   with F02.
6. Land `dome_control`'s F19 (dome_mission `/intent` integration). It is
   tracked in that package.
7. Resume F02 (`process/03-features/notdone/F02-full-stack-smoke-test.md`).
   TF02.0 and TF02.1 could start now. TF02.2 and TF02.3 should wait for F19.
   F05's launch commands should come first.

### Decisions pending

- **`dome_control`'s `control.yaml` is parked by the user.** It lives in
  `~/.dome/config`, untracked, and `config set` rewrites it. The repo copy,
  `config/control-config.yaml`, is used by nothing. The design options are
  in this session's history entry.

### Caveats

- **`uv` isn't installed on the Pi or the VM**, so `/checkpoint`'s `uv run`
  steps fail. Use `/usr/bin/python3 -m pytest`. For ruff, use
  `~/.local/bin/ruff` on the VM and
  `~/ros2_ws/src/dome_vision/.ruff-venv/bin/ruff` on the Pi.
- `package.xml` exec-depends on `yellow_pad` and `dome_telemetry`, which
  aren't on the remote computer. `rosdep install` there will complain;
  `colcon build` won't.

### Blocked

- **F02 is parked pending `dome_control`'s F19.** `behavior_manager` and
  `mission_node` both subscribe to `/intent` with no coordination. See
  `dome_control`'s `03-features/notdone/F19-dome-mission-intent-integration.md`.
- **Nav2 modes (B, E) and `mission_explore` are blocked on `dome_nav` I13**,
  so F05 leaves them alone.

### Open issues

- I01: wheel/EKF odometry drifts a lot (`map → odom` reached about 1 m).
- I02: the EKF stalled once for 10.65 s (2026-11-12); cause unknown. E3 saw
  a 0.33 s `/odom` gap.
