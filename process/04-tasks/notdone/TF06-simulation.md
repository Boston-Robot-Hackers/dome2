# TF06 Build out the DOME simulation on the remote computer, for Feature F06

**Date Created:** 2026-11-17

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.

Each step is numbered `TFNN.N`, matching this file's own `TFNN` (e.g. `TF03.0`,
`TF03.1`, ...), starting at `.0`.

For each task step, add a test when feasible. If not feasible, note why.

## TF06.0 — Survey the sim pieces, check the VM, settle the decisions

**Status**: not done

**Description**:

- Read `dome_nav`'s sim launch files, worlds, sim URDFs, sim params and
  `simhowto.md`. Write down what each piece does and what it depends on.
- On the VM, check what is installed: Gazebo version, the `ros_gz`
  packages, and better_launch's `gazebo` module.
- Settle F06's three decisions with the user: the launch shape, the sim
  URDF, and the fate of `dome_nav`'s `sim_*.launch.py`.

Record the results in this file.

**No code before this step is approved.**

**Test**: none, because this is a survey and decisions.

## TF06.1 — Stage 1: robot in a world

**Status**: not done

**Description**: Add the first stage of the dome2 sim launch: Gazebo with a
`dome_nav` world, the robot spawned, the bridge, and
`robot_state_publisher`. Run it on the VM.

**Test**:

- **Static:** a test that the launch's targets exist and that it follows
  F05's convention (better_launch only, literal defaults).
- **Manual on the VM:** `/scan`, `/odom` and `/clock` publish, and the TF
  tree reaches `base_footprint` and the lidar frame.

## TF06.2 — Sim URDF from dome2's model

**Status**: not done

**Description**: Make the sim use dome2's robot model, as decided in
TF06.0. Either generate a sim variant from `config/dome3.durdf` with the
Gazebo plugins added, or adopt a `dome_nav` copy as an interim step.

**Test**: a unit test that the sim URDF parses and has the same link and
frame names as `dome3.urdf`, plus the plugins the bridge needs.

## TF06.3 — Stage 2: SLAM in sim

**Status**: not done

**Description**: Add SLAM with `dome_nav`'s sim params. Make sure
`slam_toolbox` reaches `active`, since on Kilted it sometimes does not
(`dome_nav` I13).

**Test**: manual on the VM. `ros2 lifecycle get /slam_toolbox` is `active`,
`/map` publishes, and `map → odom` exists. It is not unit-testable because
it needs Gazebo and SLAM running.

## TF06.4 — Stage 3: Nav2 in sim

**Status**: not done

**Description**: Add Nav2 with `nav2_params_explore_sim.yaml`. I13 says
that file was already migrated to Kilted. Check that `/cmd_vel` has one type
in sim.

**Test**: manual on the VM. A goal sent with `ros2 action send_goal` moves
the robot, and `bt_navigator` stays up.

## TF06.5 — Stage 4: exploration in sim

**Status**: not done

**Description**: Add `slam_manager` and `explorer_manager` with the sim
tunings.

- Make the explorer its own stage, so `--options` can start it alone. This
  replaces `just_explorer.launch.py`.
- Move the tunings out of launch arguments into params YAML files in
  `dome_nav/config/`, picked with one argument (e.g. `--explore_params`).
  Start with the sim values that `simhowto.md` passes by hand.

**Test**:

- **Static:** a test that each explorer params file loads and names only
  parameters the node declares.
- **Manual on the VM:** an `exploration_start` intent on `/intent` makes
  the robot move and the map grow, and `/explore/status` reports progress.

## TF06.6 — Stage 5: dome_viz on the sim

**Status**: not done

**Description**: Show the sim in dome_viz with sim time. This needs the
`--sim_time` pass-through that `remote.launch.py` lacks today; fix it here
if F05 hasn't.

**Test**:

- **Static:** a test that `sim_time` reaches `view.launch.py`'s arguments.
- **Manual:** the page shows the sim map and robot.

## TF06.7 — Retire or fold `dome_nav`'s old sim launch files

**Status**: not done

**Description**: Apply TF06.0's decision to `sim_robot`, `sim_slam`,
`sim_nav2`, `sim_explore_node`, `sim_nav_full` and `sim_rviz`. Update
`dome_nav`'s `simhowto.md` and `stack/launch_inventory.md`. Changes in
`dome_nav` get their own commit there.

**Test**: F05's convention test (TF05.6). No launch file or doc may
reference a sim file that no longer exists.

## TF06.8 — Write the F06 test suite

**Status**: not done

**Description**: Collect and finish F06's automated tests in dome2:

- the sim launch's static checks (targets exist, convention)
- the URDF test
- the `sim_time` pass-through test

Run them with `/usr/bin/python3 -m pytest`.

**Test**: this task is the test suite.

## TF06.9 — End-to-end demo on the VM

**Status**: not done

**Description**: Run F06's demo by hand, from one command to exploration
shown in dome_viz. Record the commands and results in the feature file.

**Test**: manual only. It needs Gazebo and a browser.
