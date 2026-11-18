# Current Status — dome2

## Open

### Pick up here (2026-11-18)

**Checkpointed across seven repos:** dome2, dome_telemetry, dome_nav,
dome_semantic, dome_vision, dome_viz and j3. Details are in `history.md`
and TF05.

- **Kilted upgrade verified.** slam_toolbox activated in 4 of 4 starts, and
  `d c`, `d f` and `d vi` pass. `d b` waits on the UPS I2C.
- **TF05.2:** dome_telemetry is converted. Next are dome_vision, dome_viz
  and dome_voice.
- **dome_telemetry now uses the j3 layout**: its docs are under `process/`,
  its `.claude` is synced from j3, and it has the header hook.
- **The `d vi` stop floods the log** with depthai USB read errors. Whether
  that gets a dome_vision issue is still undecided.

### Next

1. **Re-check `d b`'s `/telemetry/battery` once the UPS I2C is connected.**
   The other re-tests after the upgrade passed (2026-11-18, see TF05.1).
   - Decide whether `d vi`'s flood of depthai USB read errors on stop needs
     its own dome_vision issue.
2. **F05, TF05.2**: dome_control, dome_nav, dome_semantic and dome_telemetry
   are done, and dome_mission was skipped. Carry on with dome_vision,
   dome_viz and dome_voice. Remove each from `NOT_YET_CONVERTED` (TF05.6's
   strict xfails) as it is done. Progress is in TF05.
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
  so F05 leaves them alone. I13 also holds the slam_toolbox activation stall
  (4 of 31 before the upgrade, 0 of 4 after), which still has no chosen fix.

### Open issues

- I01: wheel/EKF odometry drifts a lot (`map → odom` reached about 1 m).
- I02: the EKF stalled for 10.65 s (2026-11-12). It recurred on 2026-11-17,
  stalling for 1.5 to 3.4 s three times with no Foxglove client. Cause
  unknown. E3 saw a 0.33 s `/odom` gap.
