# Current Status — dome2

## Open

### Pick up here (2026-11-16)

**F03 (dome2 as the stack hub) is closed.** It was verified on the robot and
the VM: `make clone`, `make pull`, and `bl dome2 remote.launch.py --options "v"`
serving dome_viz at `http://192.168.4.83:8080/`. 51 tests pass.

- **VM build gotcha:** a package that moved repos can leave a stale
  `build/<pkg>` cache pointing at its old source folder (seen with
  `dome_telemetry_msgs`, which moved out of `dome_vision`). Delete
  `build/<pkg>` and `install/<pkg>`, then rebuild.
- **Open follow-up:** `bl.include` passes `remote.launch.py`'s own arguments
  on to `view.launch.py`, so dome_viz's `--sim_time` can't be set through
  the remote launcher yet. That only matters for replaying recorded data.

### Next

1. **Move the power load test here from `dome_semantic`.** Files:
   `tools/power_load_test.sh`, `tools/power_summary.awk`,
   `test/test_power_load_test.py`, `process/02-doc/power_testing.md`. See
   `dome_semantic`'s `current.md` for the references to update. It overlaps
   with F02, so consider merging the two. The stack-wide parts could go in
   `stack/`.
2. Land `dome_control`'s F19 (dome_mission `/intent` integration). It is
   tracked in that package.
3. Resume F02 (`process/03-features/notdone/F02-full-stack-smoke-test.md`).
   TF02.0 and TF02.1 are pure and could start before F19. TF02.2/TF02.3
   should wait for F19.

### Caveats

- **`uv` and `ruff` aren't installed on the Pi.** The post-edit ruff hook
  does nothing here, `/checkpoint`'s `uv run` steps will fail, and F03's
  code has not been linted.
- `package.xml` exec-depends on `yellow_pad` and `dome_telemetry`, which
  aren't on the remote computer. `rosdep install` there will complain;
  `colcon build` won't.
- The robot runs ROS 2 **Kilted**; some package docs still say Jazzy.

### Blocked

- **F02 is parked pending `dome_control`'s F19.** `behavior_manager` and
  `mission_node` both subscribe to `/intent` with no coordination. See
  `dome_control`'s `03-features/notdone/F19-dome-mission-intent-integration.md`.

### Open issues

- I01: wheel/EKF odometry drifts a lot (`map → odom` reached about 1 m).
- I02: the EKF stalled once for 10.65 s (2026-11-12); cause unknown.
