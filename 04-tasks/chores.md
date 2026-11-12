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
