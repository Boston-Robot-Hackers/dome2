- [x] Fix `robot.launch.py`'s `options` param: `str | None` annotation broke
      `--options` (better_launch feeds annotations straight to
      `click.Option(type=...)`, which can't build an option from a union —
      crashed with `AttributeError: 'UnionType' object has no attribute
      '__name__'`). Changed to `options: str = ""`, treating empty string as
      "not provided". Regression test added:
      `test_launch_profiles.py::TestStartNavSignature`.
- [x] Added `battery` and `yellow` subsystems to `robot.launch.py`
      (`dome_telemetry/robot.launch.py` and `yellow_pad/yellow_pad.launch.py`)
      so battery telemetry and Yellow Pad joystick teleop can be toggled
      independently. Removed the telemetry include from `gendrv.launch.py`, so
      `drivers` no longer starts it. Added `exec_depend` on `dome_telemetry` and
      `yellow_pad` in `package.xml`.
- [x] URDF now generated from `config/dome3.durdf` (durdf source, copied from
      `~/durdf/examples/dome2.durdf`); `dome3.urdf` is regenerated, not hand-edited.
      Fixed the camera joint rpy (was `[-87.99, -8, -90]deg`, which rolled the
      image 8° and pointed ~2° up) to `[-95, 0, -90]deg` = 5° down (calibrated with horizon line), and set
      camera z to 0.075 (measured 2026-11-12: 13 cm forward, lens 14.5 cm above floor).
      Lidar joint now uses constants; moved to x -0.08, z 0.105 (measured
      2026-11-12: 8 cm behind centre, lens 17.5 cm above floor). Documented the origin
      (base_link = plate centre). Measured base geometry: plate top 7 cm above
      floor, wheels 7 cm diameter; wheel and caster now sit on the floor
      (previously sank into it). Moved the display-only
      laser post under the lidar.
- [x] 2026-11-16: Sync `.claude/` with the canonical `j3` kit and move the process folders under `process/`, matching the sibling packages. Added `.githooks/pre-commit` (header stamping), a `help`-only `Makefile`, and renumbered task steps to `TFNN.N` with `Date Created`.
- [x] `start_nav`'s `profile` default is the literal `""`, because `bl` parses the signature statically. Regression test: `TestLauncherSignature.test_defaults_are_literals` (covers `remote.launch.py` too).
- [ ] 2026-11-17: Stack-wide: node `main()`s print an `ExternalShutdownException` traceback when their launch is stopped (Kilted rclpy raises it from `spin` on SIGTERM/Ctrl-C), and skip `destroy_node`. Fixed in 11 mains across dome_control (4), dome_mission, dome_nav (2), dome_telemetry, dome_vision, dome_viz, dome_voice: catch it with `KeyboardInterrupt`, then `destroy_node` + `rclpy.try_shutdown()`. Regression test `test_main_shutdown.py` in each package (fails on the old code). dome_viz's test can't run on the Pi (no `aiohttp`); run it on the VM. Live check 2026-11-17: `speech_output` stops cleanly. Pending: one commit per repo.
