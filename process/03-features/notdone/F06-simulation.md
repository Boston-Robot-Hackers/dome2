# Feature description for feature F06

Feature file name must be `FNN-<slug>.md` where `NN` matches the feature number.

# F06 — Build out the DOME simulation on the remote computer

**Priority**: Medium

**Date Created:** 2026-11-17

**Done:** no

**Tasks File Created:** yes

**Tests Written:** no

**Test Passing:** no

**Description**: Get a simulation of the DOME stack running on the remote
computer (the VM), started from one dome2 launch.

### Why

`dome_nav` has sim pieces from earlier work:

- five launch files (`sim_robot`, `sim_slam`, `sim_nav2`,
  `sim_explore_node`, `sim_nav_full`) plus `sim_rviz`
- two Gazebo worlds (`multi_room`, `simple_room`)
- sim URDF copies (`dome3_sim.urdf`, `minimal_sim.urdf`)
- sim SLAM and Nav2 params
- `02-doc/simhowto.md`

**They have never been tested end to end** (user, 2026-11-17). A working
sim lets stack changes be tried without the robot, on the computer with CPU
to spare.

### Where it lives

The sim spans several packages, so it is a *global* configuration (spec:
"Global vs package launch files").

- **Its top-level launch lives in dome2.**
- **`dome_nav` keeps its nav-specific pieces**: worlds, sim SLAM and Nav2
  params, the explorer.
- **The robot model comes from dome2**, the owner of the real URDF
  (`config/dome3.durdf` → `dome3.urdf`), not from `dome_nav`'s copies.

### Built in stages

Each stage is shown to work on the VM before the next one starts:

1. **Robot in a world**: Gazebo, the robot spawned, the bridge, and
   `/scan`, `/odom`, `/clock` and TF publishing.
2. **SLAM**: `/map` and `map → odom`, with `slam_toolbox` reaching `active`.
3. **Nav2**: a goal sent in sim moves the robot.
4. **Exploration**: an `exploration_start` intent grows the map. The
   explorer is its own stage, so `--options` can start it alone (this
   replaces `dome_nav`'s `just_explorer.launch.py`). Its tunings live in
   params YAML files in `dome_nav/config/`, chosen with one argument such as
   `--explore_params <file>`. Comparing two tunings means running with two
   files.
5. **Viewing**: dome_viz shows the sim map, using sim time.

### Out of scope

- Mission (`dome_mission`) in sim.
- Perception (camera, `dome_vision`) in sim.
- Voice.
- Tuning the sim to match the real robot's behaviour.

### Decisions to settle first (TF06.0)

- **Launch shape.** A dome2 `sim.launch.py` with the same `--options`
  interface, with stages as subsystems? Or a `sim` subsystem of
  `remote.launch.py`?
- **Sim URDF.** Generate it from dome2's `dome3.durdf`, adding the Gazebo
  plugins (diff drive, lidar)? Or adopt one of `dome_nav`'s copies for now?
- **What happens to `dome_nav`'s `sim_*.launch.py`.** Fold them into the
  dome2 launch, or keep them as package-level pieces it includes? F05's
  two-level rule decides.

## How to Demo

**Setup**: the VM, with the workspace pulled and built. Gazebo must be
installed (whether it is has not been checked). Set
`LIBGL_ALWAYS_SOFTWARE=1` (`simhowto.md`).

**Steps**:
1. Start the sim from dome2 with all stages, e.g.
   `bl dome2 sim.launch.py --options "w s n e v"`. The exact command is
   settled in TF06.0.
2. Check that `/scan`, `/odom`, `/clock` and `/map` are publishing.
3. Publish an `exploration_start` intent on `/intent`.
4. Open dome_viz in a browser.

**Expected output**: Gazebo shows the robot in `multi_room`. dome_viz shows
the map growing as the robot explores. Stopping the launch exits cleanly.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
