# Current Status — dome2

## Open

### Pick up here (2026-11-19)

**Checkpointed:** dome2, dome_vision, dome_voice, dome_semantic,
dome_control and dome_nav. Details are in `history.md` and TF05.

- **TF05.3 is done and passed on the robot** (`d c`, `d vi`, `d vo`, `d f`).
  The dome2 wrappers are gone; `LAUNCH_FILES` names package files directly.
- **TF05.4 remains:** the `gendrv` → `drivers` rename, `--sim_time` and
  `--map_name` pass-through, and `remote.launch.py`.
- **F07 and dome_voice F02 are done.** `rosutils` is not committed yet
  (the user hasn't said whether to include it).
- **The vision node still aborts on a UI stop** (dome_vision chore, not started).

### Next

1. **F05:** TF05.3 is done and its robot test passed (2026-11-19). Finish TF05.4: the `gendrv` → `drivers` rename, argument forwarding and `remote.launch.py`.
2. **dome_vision's shutdown-abort chore**, then re-test a UI stop for the
   abort and I06's flood.
3. **I02: a full-stack run with drive** on 2 NN threads, watching
   `journalctl -kf | grep -i voltage`.
4. **dome_viz chore:** "Robot not connected" while the camera streams.
5. **F06, TF06.0** on the VM. Approved, but don't start until the user says so.
6. **Move the power load test here from `dome_semantic`.** Files:
   `tools/power_load_test.sh`, `tools/power_summary.awk`,
   `test/test_power_load_test.py`, `process/02-doc/power_testing.md`. See
   `dome_semantic`'s `current.md` for the references to update. It overlaps
   with F02.
7. Land `dome_control`'s F19 (dome_mission `/intent` integration). It is
   tracked in that package.
8. Resume F02 (`process/03-features/notdone/F02-full-stack-smoke-test.md`).
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

- **Voice can't run on the Pi: its runtime isn't installed.** The piper
  binary and model, `openwakeword`, `vosk` and the `hey_marvin` model are
  missing (TF05.2, dome_voice). An issue was offered but not opened.

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
