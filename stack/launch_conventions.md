# DOME Launch File Conventions

The rules every DOME launch file follows. They were decided in F05
(2026-11-17). `test/test_launch_conventions.py` (TF05.6) checks the ones a
test can check.

See [`launch_inventory.md`](launch_inventory.md) for every launch file and
its status.

## Two levels

- **A DOME package's launch files start only its own nodes.** They may also
  start or include outside (non-DOME) packages they need, such as
  `slam_toolbox`, `nav2_bringup` or `tf2_ros`.
- **They never include another DOME package.**
- **Anything that combines DOME packages is global and lives in dome2.**
  That covers dome2's `robot.launch.py`, `remote.launch.py`, and the sim
  (F06).

## File names

- **Package level:** `robot.launch.py` if the package runs on the robot,
  `remote.launch.py` if it runs on the remote computer. Nothing else.
- **dome2:** `robot.launch.py` and `remote.launch.py` (top level), plus
  `drivers.launch.py`, because dome2 owns the driver bringup.
- **Variants are arguments, not files.** A mode, config or sim-time choice
  is a launch argument (e.g. `dome_nav`'s `--mode slam`), never a second
  file.

### Known exceptions

`test/test_launch_conventions.py` skips these. Its `KNOWN_EXCEPTIONS` list
mirrors this section.

These are blocked on `dome_nav` I13 and left untouched until it is fixed:

- `dome_nav`: `robot_nav.launch.py`, `robot_explore.launch.py`
- `dome_mission`: `mission_explore.launch.py`, which also breaks the
  two-level rule

The `dome_nav` `sim_*.launch.py` files are untested and belong to F06.

## Only demonstrated configurations

A launch file or launch option stays only if the configuration it starts
has been shown to work, with the evidence recorded (in the inventory or a
feature file). Anything else is deleted; git history keeps it.

## better_launch only

- Every DOME launch file uses better_launch (`@launch_this`).
- No DOME launch file imports `launch` or `launch_ros`, or builds a
  `LaunchDescription`.
- Outside packages' own ROS launch files may still be included with
  `bl.include`.

## Arguments

better_launch reads launch arguments by parsing the source, and hands each
annotation to `click`. So:

- **Literal defaults only.** `profile: str = ""`, never a name such as
  `DEFAULT_PROFILE` or a call such as `os.environ.get(...)`. Read the
  environment in the body instead.
- **Plain types only.** `str`, `bool`, `int`, `float`, or a `Literal[...]`.
  No unions such as `str | None`.
- **Every argument is documented** in the entry function's docstring.

## Top-level launchers (dome2)

- Each launcher declares an ordered `LAUNCH_FILES` table that maps a
  subsystem name to a package and launch file. It points **directly** at
  the package-level file, with no wrapper files in between.
- **Subsystems are chosen** with `--options` (token prefixes), `--profile`
  (an env var holding a token string), or `--is_interactive`.
- **With neither `--options` nor the profile env var**, the launcher lists
  the subsystems and stops (F04).
- **Arguments are forwarded** (`--sim_time`, `--map_name`): the launcher
  passes them on to the files that declare them. TF05.4 builds this.

## Entry function

- The `@launch_this` entry function is named after its file:
  `robot_launch` in `robot.launch.py`, `remote_launch` in `remote.launch.py`,
  `drivers_launch` in `drivers.launch.py`.

## Header and docstring

Every launch file has:

- the style-guide file header (module name and description, `Author`,
  `Version`, `Created`, `Updated`, license); the pre-commit hook stamps
  `Version`, `Created` and `Updated`
- usage examples in the header comment
- a docstring on the entry function

## Runtime behaviour

- **Lifecycle nodes must reach `active`.** Use
  `lifecycle_target=LifecycleStage.ACTIVE`. For an outside launch that
  activates its own node, such as `slam_toolbox`, check and activate it if
  needed; on Kilted it sometimes stays `inactive`.
- **Missing hardware.** A subsystem whose hardware is missing should say so
  and skip, not crash half-way (spec). The voice subsystem doesn't do this
  yet.
- **Clean stop.** Every node `main()` treats `ExternalShutdownException` like
  `KeyboardInterrupt`, then calls `destroy_node()` and
  `rclpy.try_shutdown()`, so stopping a launch prints no traceback.
