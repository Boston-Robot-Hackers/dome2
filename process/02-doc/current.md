# Current Status — dome2

## Open

### Pick up here (2026-11-19)

**Checkpointed across three repos:** dome2, dome_vision and dome_viz (twice).
Details are in `history.md` and TF05.

- **TF05.2:** dome_vision is converted, and its `--depth` fix was verified
  on the robot. dome_viz's `view.launch.py` is now `remote.launch.py`. Its
  full suite and a launch still need the VM; the commands are in TF05.
  dome_voice is last.
- **The vision node aborts on a UI stop** (`std::terminate` in depthai).
  The fix is an open dome_vision chore, `release_device()` called from
  `main()`, and is not started. Its robot re-test may also close I06.
- **`nn_threads` is back to 2** after the user rewired the power. I02
  stays open until a full-stack run with drive shows no brownouts.

### Next

1. **F05, TF05.2**: dome_control, dome_nav, dome_semantic and dome_telemetry
   are done, dome_vision and dome_viz are done in code (2026-11-19), and
   dome_mission was skipped. Carry on with dome_voice. dome_viz still needs
   its full suite and a launch on the VM. Remove each from `NOT_YET_CONVERTED` (TF05.6's
   strict xfails) as it is done. Progress is in TF05.
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
