# Current Status — dome2

## Open

### Pick up here (2026-11-17)

**F04 is closed. F05 and F06 are open.**

- **F05 (consistent, correct launch files) is drafted, and most of its robot
  experiments are done.** See
  `process/03-features/notdone/F05-launch-file-cleanup.md` and
  `process/04-tasks/notdone/TF05-launch-file-cleanup.md`. TF05.1 holds the
  results:
  - **Pass:** `d vi`, `d c`, `d f`, `d y`, and SLAM without Nav2 (`d b`
    plus `slam_toolbox`).
  - **Fail:** `d vo`. `voice_input` has no `openwakeword` module, and the
    voice board is out.
  - **Convention rules:** all DOME launch files use better_launch. A DOME
    package's launch files start only its own nodes (outside packages
    allowed); anything combining DOME packages lives in dome2.
  - **TF05.0 and TF05.1 done.** Verdicts are final in
    `stack/launch_inventory.md`; rules in `stack/launch_conventions.md`.
  - **TF05.2 in progress.** dome_control is done (committed, not pushed);
    next is dome_mission (blocked file, so likely nothing), then dome_nav.
  - **TF05.6 test written early:** `test/test_launch_conventions.py`.
    Unconverted files are strict xfails in `NOT_YET_CONVERTED`; remove each
    entry as its repo is fixed.
- **F06 (build out the sim on the VM) is approved (2026-11-17), not started.** The
  `sim_*` files were never tested. See
  `process/03-features/notdone/F06-simulation.md`. TF06.0 needs the VM.
- **Stack-wide shutdown fix, pushed in all 7 repos.** 11 node `main()`s
  printed an `ExternalShutdownException` traceback on stop. Each is fixed
  and has a regression test. See `chores.md`.
- **SLAM params need a fresh start.** `dome_nav`'s
  `mapper_params_online_async.yaml` has three keys Kilted ignores, and
  `slam_toolbox` sometimes doesn't activate. Both are added to `dome_nav`
  I13 (pushed).

### Next

1. **Run dome_viz's `test_main_shutdown.py` on the VM**, because the Pi has
   no `aiohttp`. It is the last check of the shutdown fix. The dome_control
   nodes stop cleanly on the robot (2026-11-17).
2. **F05, TF05.2**: bring each package's launch files to the convention
   (`stack/launch_conventions.md`), one repo at a time. TF05.1 is settled;
   verdicts are in `stack/launch_inventory.md`.
3. **F06, TF06.0** on the VM. Approved, but don't start until the user says so.
4. **Move the power load test here from `dome_semantic`.** Files:
   `tools/power_load_test.sh`, `tools/power_summary.awk`,
   `test/test_power_load_test.py`, `process/02-doc/power_testing.md`. See
   `dome_semantic`'s `current.md` for the references to update. It overlaps
   with F02.
5. Land `dome_control`'s F19 (dome_mission `/intent` integration). It is
   tracked in that package.
6. Resume F02 (`process/03-features/notdone/F02-full-stack-smoke-test.md`).
   TF02.0 and TF02.1 could start now. TF02.2 and TF02.3 should wait for F19.
   F05's launch commands should come first.

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
