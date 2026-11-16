# Current Status — dome2

## Open

### Pick up here (2026-11-16)

**F03 (dome2 as the stack hub) is built; only TF03.6's manual runs are left.**
Nothing is committed yet. That includes the `.claude/` sync with the `j3`
kit and the move to `process/` from earlier this session.

- **New:** `stack/packages.yaml` (12 packages and where each runs),
  `make clone` (clones any missing package next to dome2), `make pull`, `launch/remote.launch.py` (subsystem `viz`), and
  `stack/README.md` as the starting point for stack-wide docs.
- **`make pull` pulls all 12 packages on either computer.** The first
  version selected packages by a `DOME_ROLE` host role; you asked for all of
  them, so the role code and the `.bashrc` export are gone. `runs_on` only
  records where a package runs. Verified on the robot: all 12 ok.
- **Shared code:** both launchers use `dome2/launch_options.py` (pure) and
  `dome2/subsystem_launcher.py`.
- **Moved:** the onboarding guide is now `stack/dome_developer_onboarding.md`.
- **Tests:** 51 pass with `python3 -m pytest test`. `setup.cfg` puts the
  source tree first, so tests don't pick up the installed dome2.
- **Still to run (TF03.6):** on the VM, clone dome2, `make clone`, build,
  then `bl dome2 remote.launch.py --options "v"` (`stack/README.md`).
  Writing a critique is not part of F03.

### Next

0. Finish TF03.6 on the VM, then close F03.
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
