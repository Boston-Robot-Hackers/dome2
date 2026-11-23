# Current Status — dome2

## Open

### Pick up here (2026-11-23)

**F10 per-entry launch args: code, tests and docs done; robot + VM run left.**
Driven from dome_nav's F36 (launch units) session.

- `LAUNCH_FILES` entries may carry fixed args:
  `("dome_nav", "robot.launch.py", {"unit": "nav2"})`. Pure
  `launch_options.entry_parts`; `launch_subsystems` passes them to
  `bl.include`. A better_launch spike (TF10.0) confirmed double includes and
  that per-include args beat forwarded ones.
- **Placement rule** written into `stack/launch_conventions.md`: each
  launcher offers every sub-launch that *can* run on its side; "either" units
  are in both; double starts are the operator's call.
- New subsystems: robot `nav2`, `explorer` (and `slam` now with
  `unit=slam`); remote `slam`, `explorer`. `remote.launch.py` now forwards
  `map_name`. Explore = `d sl n e`, or `d sl n` + remote `e`.
- Tests: 150 passed, 9 skipped (`/usr/bin/python3 -m pytest`; no `uv` on the
  Pi). Convention test checks per-entry args against their targets.
- **Do next (TF10.6):** robot `--options "d sl n" --map_name <name>`, VM
  `remote.launch.py --options "e" --map_name <name>`; check each node runs
  once, on the intended machine.

### Before that (2026-11-22, late): the session moves to the Pi

Work so far was on the Mac. **Everything is committed and pushed** (dome2,
dome_pad, dome_voice, esp32-c6-demo). On the Pi:

1. **Update the workspace:** `cd ~/ros2_ws/src/dome2 && make pull`, then
   `cd ~/ros2_ws && colcon build --packages-select dome2 dome_pad dome_voice`
   and `source install/setup.bash`. The Pi was seen running an older dome2
   (a `/gendrv` node) on 2026-11-22.
2. **Next task: dome_voice F15's TF15.2**, testing faster speech on the
   robot. Steps are in dome_voice's `process/02-doc/current.md`.
3. **Launch for the pad:** Pi `bl dome2 robot.launch.py --options "d c vo p"`
   (`c` is needed for the Status key; `p` for the pad at all); VM
   `bl dome2 remote.launch.py --options "vo p"` with `ANTHROPIC_API_KEY`.
4. **Watch the EKF:** "Failed to meet update rate" errors (30 Hz; updates
   took 40-300 ms) were seen with `d c vo p`. Not yet diagnosed: check
   `top` idle vs. while the robot speaks. Candidates: `voice_input`'s
   always-on wake word and STT, and Piper synthesis.

### Earlier on 2026-11-22

**F09 is done: the Yellow Pad as `dome_pad`.** New repo
`Boston-Robot-Hackers/dome_pad` (was `yellow_pad`), registered here; `pad`
subsystem on both launchers; button A asks dome_voice's LLM for a robot
joke. The user confirmed driving, the ROS tab and button A on the robot
and VM. Results are in TF09 (`process/04-tasks/done/`).

- **Run the Pi with `p`**: `bl dome2 robot.launch.py --options "d vo p"`.
  Without it there's no `joy_node`, so the pad neither drives nor sends
  button presses.
- **`yellow_pad` is archived** on GitHub (its README points to dome_pad),
  and its submodule is removed from `esp32-c6-demo` (2026-11-22).
- **The Mac's test run here** has 23 failures that come from stale checkouts
  next to dome2 (dome_control, dome_voice, dome_telemetry behind origin;
  dome_viz not cloned). Identical before and after F09. Run the suite on
  the VM after `make pull`.

### Before that (2026-11-19)

**Checkpointed dome2.** Details are in `history.md`, TF05 and F08.

- **TF05.4 is done but not run on the robot.** The commands are at the end
  of TF05.4: `d`, `d b sl`, `d b sl vi se` (with `--map_name tf054`), and
  `d sl` without a map name, which must fail.
- **F08 is done:** `make status-repos`. It shows dome_control and
  dome_mission DIRTY from things not made in this session: dome_control's
  two deleted PDFs and dome_mission's untracked `__pycache__/`.
- **`rosutils` is still uncommitted** (the user hasn't said whether to
  include it).
- **The vision node still aborts on a UI stop** (dome_vision chore, not started).

### Next

0. **F10:** TF10.6 robot + VM run (commands above).
1. **F05:** robot-test TF05.4 (commands in TF05). Then TF05.5 (stack docs) and TF05.7 (verify on robot and VM, including `--is_interactive`).
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
- `package.xml` exec-depends on `dome_telemetry`, which isn't on the
  remote computer. `rosdep install` there will complain;
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
