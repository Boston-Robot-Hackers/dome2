- [x] Fix `robot.launch.py`'s `options` param: `str | None` annotation broke
      `--options` (better_launch feeds annotations straight to
      `click.Option(type=...)`, which can't build an option from a union —
      crashed with `AttributeError: 'UnionType' object has no attribute
      '__name__'`). Changed to `options: str = ""`, treating empty string as
      "not provided". Regression test added:
      `test_launch_profiles.py::TestStartNavSignature`.
