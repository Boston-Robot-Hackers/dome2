# History — dome2

Archived entries from `current.md`'s Recent completions, oldest work moved
here to keep `current.md` focused on what's recent and relevant.

- 2026-11-19: F05 TF05.4 and F08.
  - **TF05.4:** `gendrv.launch.py` → `drivers.launch.py`; new `slam` (`sl`)
    and `semantic` (`se`) subsystems; `--sim_time` and `--map_name` reach the
    subsystems through better_launch's own argument passing, with two new
    convention tests. All three dome2 launchers now meet the convention, so
    `NOT_YET_CONVERTED` is empty. Not yet run on the robot.
  - **F08:** `make status-repos` prints `CLEAN`/`DIRTY` per registered repo.
    `commit-push-repos` was built and dropped at the user's request.
- 2026-11-19: F05 TF05.3 deletions, F07 config convention, dome_voice F02.
  - **TF05.3:** deleted the four dome2 wrappers (`LAUNCH_FILES` now names
    each package's file directly), `remote.launch.py` in dome_control,
    dome_voice and dome_vision, `dome_vision_ros.launch.py`, and dome_nav's
    three experiment files. The power test's `oak` stage now runs vision's
    `robot.launch.py`. **Robot test passed** for `d c`, `d vi`, `d vo` and `d f`.
  - **F07 (`stack/config_conventions.md`):** config is `<pkg>/config/<subject>.yaml`,
    passed by the launch file via `bl.find`. No config-path env vars:
    `DOME_VISION_CONFIG` and `DOME_VOICE_CONFIG` were removed from the nodes
    and from `rosutils`. The tmux server had kept the old values.
  - **dome_voice TF05.2 and F02:** `robot.launch.py` converted; the tuned
    table that the YAML had silently replaced is gone, and `voice.yaml` now
    holds every robot value under a strict pydantic model. The voice runtime
    isn't installed on the Pi, so only the config path was verified there.
  - **`--symlink-install`** is now the build command. dome2, dome_control,
    dome_nav, dome_voice and dome_vision_ros were rebuilt clean with it.
  - dome2's literate docs 00 to 04 were rewritten for the direct entries;
    X01 (foxglove wrapper) was deleted.
- 2026-11-19: F05 TF05.2, dome_viz.
  - **`view.launch.py` became `remote.launch.py`**, with entry function
    `remote_launch` (TF05.1 decision 1). Updated: dome_viz's Makefile, test,
    notes and literate X02; dome2's `remote.launch.py`, its profile test,
    TF06 and literate 04. It left `NOT_YET_CONVERTED`.
  - Verified on the Pi only: `test_launch.py` and `--help`. The rest of the
    suite needs `aiohttp`, which only the VM has.
- 2026-11-19: F05 TF05.2, dome_vision, plus robot tests.
  - **dome_vision's `robot.launch.py`** took in `dome_vision_ros.launch.py`'s
    arguments (`--config`, `--depth`, `--enable_embeddings`), dropped the
    dead `perf`, kept `publish_raw` fixed off, and left `NOT_YET_CONVERTED`.
  - **`--depth false` now works.** The node's `depth` parameter became an
    `auto`/`true`/`false` string. Verified on the robot: `/oak/depth` is
    gone with `false` and back by default.
  - **`d b` re-check done** (user report). **dome_vision I06** was opened
    for the depthai log flood on stop.
  - **A UI stop aborted the vision node** in depthai (`std::terminate`).
    The likely cause is that `on_deactivate` never runs on SIGTERM. Logged
    as an open dome_vision chore.
  - **After the user rewired the power, `nn_threads` went back to 2**, with
    EXT5V at 5.19 V (was 4.974 V) and no undervoltage. Recorded in dome_vision
    I02.
  - **dome_viz chore:** "Robot not connected" showed while the camera image
    was arriving, which contradicts `view_state`'s `any(...)` rule.
- 2026-11-18: F05 TF05.2, dome_telemetry, and dome_telemetry's move to j3.
  - **dome_telemetry's `robot.launch.py`** got the standard header, usage
    lines and docstrings, and left `NOT_YET_CONVERTED`.
  - **Wrong "launched with gendrv" claims were fixed** in its README,
    CLAUDE.md, spec and two literate docs. Since a017b05 the node has been
    dome2's `battery` subsystem.
  - **dome_telemetry now uses the j3 layout**: its docs are under `process/`,
    its `.claude` is synced from j3, and it has the header hook.
  - **j3 gained the feature `Date Created:` rule.** dome2's `process.md` was
    re-synced.
  - **dome_semantic's literate doc** `14-semantic_launch.md` became
    `14-robot_launch.md`.
  - The installed `robot_map.launch.py` is gone, cleared by the rebuild
    after the upgrade.
- 2026-11-18: Kilted apt upgrade and the shutdown fix's last check.
  - **The Pi and the VM were upgraded** (2026-11-17). The Pi now has Fast
    DDS 3.2.5 and foxglove_bridge 3.5.0. The pre-upgrade snapshot is
    `~/kilted-before-2026-11-17.txt` on the Pi.
  - **slam_toolbox activated in all 4 starts after the upgrade**, through
    `bl dome_nav robot.launch.py --mode slam`. Before the upgrade, 4 of 31
    had stalled. Four starts can't show a fix; details are in dome_nav I13.
  - **The errors seen in one run came from shutdown**, not startup:
    `slam_manager` tries a lifecycle transition while it is being shut down.
  - **dome_viz's `test_main_shutdown.py` passed on the VM.** That was the last
    check of the stack-wide clean-shutdown fix.
  - **Subsystem re-tests after the upgrade:**
    - `d c`, `d f` (bridge 3.5.0) and `d vi` passed.
    - `d b` starts, but its data waits on the UPS I2C being connected.
    - `d vi`'s stop floods the log with depthai USB read errors.
    - Details are in TF05.1.
- 2026-11-17: F05 TF05.1 settled.
  - **TF05.2:** dome_control is done and verified on the robot (`--options
    "d c"`; `param get` showed the YAML values). dome_mission was skipped
    (blocked). dome_nav's `robot_map.launch.py` became `robot.launch.py
    --mode slam` with no Nav2.
  - **dome_semantic was converted late the same day.** `semantic.launch.py`
    became `robot.launch.py` and ran on the robot with `--static_map_odom
    true`.
    - On that bench run, two cans at about 5 m became five targets. This is
      logged in dome_vision I04 (a recurrence) and the new dome_semantic I01.
  - **TF05.6** convention test written early, with strict xfails for
    unconverted files.
  - **Header-stamping hook** installed in dome_control and dome_nav.
  - **dome_control's unused `mapper_params*` copies** were deleted.
  - **`control.yaml` was looked into, then parked.** Only `simple_cli`'s
    `config set` rewrites it. The options were: seed it from the repo copy
    if missing, or keep defaults in share with overrides in `~/.dome`
    (dome_nav's `write_config` works this way). `launch_templates` should
    move out either way.
  - **slam_toolbox stall:** the evidence went to dome_nav I13. Starting it
    with `bl.node(lifecycle_target=ACTIVE)` was ruled out, because
    better_launch's transition `call()` has no timeout and would hang.
- 2026-11-17: F05 TF05.0 done: `stack/launch_inventory.md`. Two-level launch
  rule decided and added to the spec. Sim declared untested; F06 (sim on the
  VM) drafted.
- 2026-11-17: F04 closed. With no `--options` and no profile env var, the
  launchers log the subsystems and call `BetterLaunch().shutdown()` (exit
  status 0). Two earlier versions failed on the VM under better_launch's UI:
  `click.prompt` never appeared, and `sys.exit(1)` ended only the UI's worker
  thread. Verified clean on the VM.
- 2026-11-17: F05 drafted (consistent launch files; first drafted as F04,
  renumbered after the remote's F04). Robot experiments E1–E3 run; results
  are in TF05.1. Convention rule added: all DOME launch files use
  better_launch. Stack-wide `ExternalShutdownException` shutdown fix committed
  and pushed in 7 repos. SLAM params and activation findings added to
  `dome_nav` I13.
- 2026-11-16: F04 built — launchers ask for subsystems instead of raising
  when neither `--options` nor the profile env var is set. Manual TF04.3
  pending. Also `chmod +x` on `dome2/launch_options.py` and
  `dome2/subsystem_launcher.py` (ruff EXE001).
- 2026-11-16: F03 closed — dome2 is the stack hub: `stack/packages.yaml`
  (12 packages), `make clone` / `make pull`, `remote.launch.py` (viz),
  shared launcher modules, `stack/README.md`. Verified on robot and VM.
- 2026-11-16: `.claude/` synced with the `j3` kit; process folders moved
  under `process/`; task steps renumbered `TFNN.N`; header-stamping
  pre-commit hook and Makefile added.
- 2026-11-05: Chore: `battery` and `yellow` subsystems in
  `robot.launch.py`; telemetry taken out of `drivers`. Base robot for power
  and semantic tests is `bl dome2 robot.launch.py --options "d b"`.
  `ruff format --check` flags 4 older files, left alone.
- 2026-08-05: Checkpoint — `.claude/` process rework, fixed nav-removal
  test regression, cleared ruff debt, `ruff.toml` added for the one
  deliberate LOG015 exception.
- 2026-08-04: Drafted F02/TF02 — full-stack smoke test (4 stages: drivers,
  control, nav, mission), not started.
- 2026-07-08: Checkpoint — tests pass, literate docs updated, stale
  mode-gate docs removed.
- Bootstrap scaffold created (LICENSE, spec.md, current.md, notes.md,
  process folders).
- Prior session: skip gated subsystem launches cleanly.
- Prior session: codereview v3.1, /start command, CLAUDE.md, how_to_be
  wired.
