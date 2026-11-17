# Current Status — dome2

## Open

### Pick up here (2026-11-17)

**Two features are open.**

- **F04 (ask for subsystems when no profile is set)** is built and pushed.
  Only TF04.3's manual run on the VM is left.
- **F05 (consistent, correct launch files) is drafted, and most of its robot
  experiments are done.** See
  `process/03-features/notdone/F05-launch-file-cleanup.md` and
  `process/04-tasks/notdone/TF05-launch-file-cleanup.md`. TF05.1 holds the
  results:
  - **Pass:** `d vi`, `d c`, `d f`, `d y`, and SLAM without Nav2 (`d b`
    plus `slam_toolbox`).
  - **Fail:** `d vo`. `voice_input` has no `openwakeword` module, and the
    voice board is out.
  - **New convention rule:** all DOME launch files use better_launch. They
    may include external ROS launch files.
- **Stack-wide shutdown fix, uncommitted.** 11 node `main()`s across 7 repos
  printed an `ExternalShutdownException` traceback on stop. Each is fixed
  and has a regression test. See `chores.md`.
- **SLAM params need a fresh start.** `dome_nav`'s
  `mapper_params_online_async.yaml` has three keys Kilted ignores, and
  `slam_toolbox` sometimes doesn't activate. Both are added to `dome_nav`
  I13, which is also uncommitted there.

### Next

1. **Run TF04.3 on the VM, then close F04.** Run `colcon build
   --packages-select dome2`, then `bl dome2 remote.launch.py` with `remote`
   unset, and answer `v`.
2. **Commit the shutdown fix**: one commit per repo in dome_control,
   dome_mission, dome_nav, dome_telemetry, dome_vision, dome_viz and
   dome_voice. Run dome_viz's `test_main_shutdown.py` on the VM first,
   because the Pi has no `aiohttp`.
3. **Live clean-stop check** of the dome_control nodes: run `d c`, then
   Ctrl-C.
4. **F05, TF05.0**: write `stack/launch_inventory.md`, then settle TF05.1's
   decisions with the user. The `--sim_time` pass-through to dome_viz is one
   of those decisions.
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
