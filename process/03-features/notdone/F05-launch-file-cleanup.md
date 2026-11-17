# Feature description for feature F05

Feature file name must be `FNN-<slug>.md` where `NN` matches the feature number.

# F05 — Consistent, correct launch files across the DOME stack

**Priority**: High

**Date Created:** 2026-11-17

**Done:** no

**Tasks File Created:** yes

**Tests Written:** no

**Test Passing:** no

**Description**: The DOME packages have collected many launch files from
earlier experiments. They don't follow one pattern, and it isn't clear which
of them still work.

This feature reviews every launch file in the registered DOME packages
(`stack/packages.yaml`) and makes them follow one convention.

### The convention

- **Two levels (decided 2026-11-17).**
  - **A DOME package's launch files start only its own nodes**, plus any
    outside (non-DOME) packages they need, such as `slam_toolbox`,
    `nav2_bringup` or `tf2_ros`. They never include another DOME package.
  - **Anything that combines DOME packages is global and lives in dome2.**
    The sim is global, so it is launched from dome2 (F06).
  - Today only `dome_mission`'s `mission_explore` breaks this rule, by
    including `dome_nav`. It is blocked on I13 anyway.
- **Package level.** Each package that runs nodes has a `robot.launch.py`,
  plus a `remote.launch.py` if it runs on the remote computer. Optional
  launch arguments select variants (mode, config, sim time), so there is no
  separate file per variant.
- **Top level.** dome2's `robot.launch.py` and `remote.launch.py` include the
  package-level files directly, chosen with the existing `--profile` /
  `--options` / `--is_interactive` interface. Since F04, they list the
  subsystems and stop when neither `--options` nor the profile env var is
  set.
- **Only demonstrated configurations.** A launch file or launch option stays
  only if it starts a configuration that has been shown to work. Everything
  else is deleted. Git history keeps it.
- **All DOME launch files use better_launch.** They may include external
  ROS launch files (e.g. `nav2_bringup`, `slam_toolbox`,
  `foxglove_bridge`) with `bl.include`. No DOME package ships a plain ROS
  `LaunchDescription` file. Today `dome_nav`'s
  `nav2_experiment_navigation.launch.py` is the only one.
- **Same header and docstring everywhere.** Each file has the style-guide
  header, usage examples, and a docstring for every argument.

### Scope

- **In scope:** the 12 registered DOME packages. The work edits launch files
  in their repos, so it means one commit per repo.
- **Out of scope:** third-party packages (`linorobot2`, `ldlidar_stl_ros2`,
  `better_launch`, `yellow_pad`, `foxglove_bridge`), and the legacy `dome`
  package, which isn't in the registry.

### What is known to work (2026-11-17)

- **Semantic-mapping run**, from `dome_semantic`'s notes (TF36.7, `mon09`):
  `dome2 --options "d b"`, plus `dome_nav robot_map.launch.py`, plus
  `dome_vision_ros.launch.py --config ... --depth true`, plus
  `dome_semantic semantic.launch.py`. That's four launches with the same
  `--map_name` given twice. `mon09` ran `slam_toolbox` without Nav2,
  because Nav2 starved the EKF.
- **Remote**: `dome2 remote.launch.py --options "v"` (F03).
- **Not yet shown on Kilted**: control, voice, foxglove and yellow. They
  are assumed to work, and TF05.1 tests them.
- **Blocked on `dome_nav` I13** (Nav2 params not migrated to Kilted):
  `robot_nav` (Mode B), `robot_explore` (Mode E) and `dome_mission`'s
  `mission_explore`. They are marked blocked, not deleted or rewritten.

### This feature's main target

**The semantic-mapping run from one top-level command**, with one shared
`--map_name`. This needs a SLAM-only nav option, which no launch file
offers today.

### Decisions this feature must settle (TF05.1)

- **Which configurations have been demonstrated.** Settled by the TF05.1
  experiments, or by a pass already on record. It can't be inferred from
  file names or dates.
- **dome_vision's launch file.** `robot.launch.py`, which dome2 uses,
  passes no config. `dome_vision_ros.launch.py` is the one the runs used.
  The proposal is to make the latter the new `robot.launch.py`, with a
  `$DOME_VISION_CONFIG` fallback and a working `--depth false`.
- **Whether nav joins `robot.launch.py`.** Today nav is launched on its own
  from `dome_nav` (Modes A, B and E), and mission from `dome_mission`. They
  could become subsystems with a mode argument instead.
- **Sim launch files: settled, out of scope.** `dome_nav`'s
  `sim_*.launch.py` were never tested. Building the sim out is F06. F05
  leaves those files alone.
- **The `--sim_time` pass-through gap.** `bl.include` currently forwards
  `remote.launch.py`'s own arguments to `view.launch.py`. Fix it here or
  leave it.

## How to Demo

**Setup**: The robot and the remote computer are both built from the
cleaned-up packages (`make pull`, then `colcon build`, then source the
install).

**Steps**:
1. Run `uv run pytest` in dome2. The launch-convention test passes for every
   registered package.
2. List each package's `launch/` folder. Only `robot.launch.py`,
   `remote.launch.py`, and any agreed exceptions remain.
3. On the robot, run `bl dome2 robot.launch.py --options "<each demonstrated
   combination>"` and confirm each subsystem comes up.
4. On the remote computer, run `bl dome2 remote.launch.py --options "v"` and
   open dome_viz.
5. Run one package-level file on its own, e.g.
   `bl dome_voice robot.launch.py`, and confirm it starts the same nodes the
   top-level launcher would.

**Expected output**: Every documented launch command starts its
configuration with no missing-file or missing-argument errors. No leftover
experiment launch files remain.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
