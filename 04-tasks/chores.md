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
