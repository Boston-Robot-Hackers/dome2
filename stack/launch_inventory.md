# DOME Launch File Inventory

Every launch file in the registered DOME packages, as of **2026-11-17**. This
is F05's TF05.0. **The verdicts below were confirmed by the user in TF05.1
(2026-11-17).** The rules they apply are in
[`launch_conventions.md`](launch_conventions.md).

There are **30 files** in 9 packages. The 3 `*_msgs` packages have none.

## How to read this

- **Status** says whether the configuration has been *demonstrated*, and
  where the evidence is. E1–E3 are F05's own experiments (TF05.1).
- **Proposed** (now confirmed) uses these verdicts:
  - **keep**: stays as is, apart from header and argument clean-up.
  - **rename**: becomes the package's `robot.launch.py` or
    `remote.launch.py`.
  - **merge**: folded into another file, usually as an optional argument.
  - **delete**: removed. Git history keeps it.
  - **blocked**: left untouched until the named issue is fixed.
  - **decide**: needs the user's call in TF05.1.
  - **F06**: never tested; left alone here and built out by F06.
- All 30 use better_launch except one, flagged below.

## dome2 (7 files)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot.launch.py` | Top level: includes the chosen subsystems | `profile`, `options`, `is_interactive` | 2026-11-16 | **Pass**: E1, E2a, E2c, E2d, `d b` in many runs | **keep** |
| `remote.launch.py` | Top level: includes `dome_viz` | same | 2026-11-16 | **Pass**: F03, F04 on the VM | **keep** |
| `gendrv.launch.py` | `linorobot2_bringup` with dome2's URDF and EKF | none | 2026-11-05 | **Pass**: every run (`d`) | **rename** to `drivers.launch.py` (decided 2026-11-17; done 2026-11-19, TF05.4). dome2 owns the drivers. |
| `dome_control.launch.py` | Wrapper: picks `dome_control`'s robot or remote file from `$DOME_MODE` | none | 2026-08-05 | Pass via E2a | **delete**. `LAUNCH_FILES` points at `dome_control` directly. Removes the hidden `$DOME_MODE` switch. |
| `dome_vision.launch.py` | Wrapper for `dome_vision_ros`'s `robot.launch.py` | none | 2026-08-05 | Pass via E1 | **delete**. Point `LAUNCH_FILES` directly. |
| `dome_voice.launch.py` | Wrapper for `dome_voice`'s `robot.launch.py` | none | 2026-08-05 | Fail via E2b | **delete**. Point `LAUNCH_FILES` directly. |
| `foxglove.launch.py` | Wrapper for `foxglove_bridge_launch.xml`, port 8765 | none | 2026-08-05 | **Pass**: E2c | **delete**. 8765 is the bridge's default port, so `LAUNCH_FILES` can point at the XML directly. Its header comment is also wrong. |

## dome_control (2 files)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot.launch.py` | `behavior_manager`, `telemetry_node`, `spin_survey_node` | none | 2026-06-03 | **Pass**: E2a; clean stop confirmed | **keep**. Move `spin_survey`'s hardcoded params to arguments or a YAML file. |
| `remote.launch.py` | `behavior_manager` (if `behavior`) | `behavior=False` | 2026-05-11 | None recorded | **delete**. The registry says `dome_control` runs on the robot. Only the `$DOME_MODE` wrapper reaches it. |

## dome_mission (1 file)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `mission_explore.launch.py` | `mission_node`, plus `dome_nav`'s `sim_nav_full` or `robot_explore` | `sim_mode`, `map_name`, `world_name`, `urdf_name` | 2026-08-01 | Can't be shown now: needs Nav2 | **blocked** on `dome_nav` I13 and `dome_control` F19. It includes `dome_nav`, which breaks the two-level rule. Later: the combined launch moves to dome2, and `dome_mission`'s own `robot.launch.py` starts only `mission_node`. |

## dome_nav (12 files)

Robot modes. dome_nav's own docs list these as the real-robot commands.

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot_map.launch.py` | `slam_toolbox` + Nav2 + `slam_manager_node` (Mode A) | `use_sim_time`, `map_name` | 2026-07-31 | SLAM part **passes** (TF36.7 runs). Its Nav2 half is broken (I13), and it starved the EKF in `mon09`. | **rename** to `robot.launch.py` with `--mode slam` (SLAM + `slam_manager`, no Nav2). E3 passed with this setup. It must make sure `slam_toolbox` reaches `active`. The Nav2 modes come back after I13. |
| `remote.launch.py` | One remote-capable unit per include: `slam` or `explorer` (dome_nav F36, added 2026-11-23). `robot.launch.py` likewise now takes `--unit slam/nav2/explorer` in place of `--mode`. | `unit`, `map_name`, `sim_time`, `max_explore_radius`, `blacklist_radius` | 2026-11-23 | Not yet run (F36 TF36.5, dome2 TF10.6) | **keep** |
| `robot_nav.launch.py` | AMCL + Nav2 on a saved map (Mode B) | `use_sim_time` | 2026-07-31 | Can't be shown now | **blocked** on I13. Later: `robot.launch.py --mode nav`. |
| `robot_explore.launch.py` | SLAM + Nav2 + `slam_manager` + `explorer_manager` (Mode E) | `use_sim_time`, `map_name`, `max_explore_radius`, `blacklist_radius` | 2026-07-30 | Can't be shown now | **blocked** on I13. Later: `robot.launch.py --mode explore`. |

Sim. **Never tested** (user, 2026-11-17). The sim is a global
configuration, so its top-level launch moves to dome2 in F06. F05 leaves
these files alone.

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `sim_nav_full.launch.py` | Whole sim: includes the four `sim_*` pieces below, plus `slam_manager` | `map_name`, `world_name`, `urdf_name`, 5 explore tunings | 2026-07-30 | Never tested | **F06** |
| `sim_robot.launch.py` | Gazebo, spawn, bridge, `robot_state_publisher`, laser TF | `world_name`, `urdf_name` | 2026-07-29 | Never tested | **F06** |
| `sim_slam.launch.py` | `slam_toolbox` (sim) | none | 2026-07-14 | Never tested | **F06** |
| `sim_nav2.launch.py` | Nav2 (sim) | none | 2026-07-14 | Never tested | **F06** |
| `sim_explore_node.launch.py` | `explorer_manager_node` with sim tunings | `map_name` + 11 tunings | 2026-07-30 | Never tested | **F06** |
| `sim_rviz.launch.py` | RViz with sim time | none | 2026-07-03 | Never tested | **F06** |

Experiments.

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `nav_experiment.launch.py` | SLAM + trimmed Nav2 + optional explorer, configs passed as paths | `slam_config`, `nav2_config`, `use_sim_time`, `map_name`, 2 tunings | 2026-07-30 | Experiment harness (C2 CPU work) | **delete**. Its one finding, the trimmed Nav2 node list, goes to I13's Nav2 rework. |
| `nav2_experiment_navigation.launch.py` | Trimmed copy of `nav2_bringup`'s `navigation_launch.py` | ROS launch args | 2026-07-16 | **Plain ROS launch file**, which breaks the better_launch rule. Cut idle load from 5.46 to 1.07. | **delete** with `nav_experiment`. Record the trimmed `lifecycle_nodes` list in I13 first. |
| `just_explorer.launch.py` | `explorer_manager_node` alone | `map_name`, `use_sim_time`, 12 tunings | 2026-07-30 | Debug tool for F31 (`simhowto.md`) | **delete** (decided 2026-11-17). F06 makes the explorer its own stage, selectable with `--options`, and moves its tunings into params YAML files chosen by one argument. |

## dome_pad (2 files)

Added 2026-11-22 (F09), after the inventory above was taken. dome_pad was
`yellow_pad`, whose `yellow_pad.launch.py` (plain ROS launch) is deleted.

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot.launch.py` | `joy_node`, `teleop_twist_joy` with `config/pad.yaml` | none | 2026-11-22 | Not run yet. Same nodes and config as `yellow_pad.launch.py`, which passed E2d (`d y`). | **keep**. `pad` in dome2's `robot.launch.py`. |
| `remote.launch.py` | rosbridge, `pad_buttons` | none | 2026-11-22 | Not run yet (F09 demo) | **keep**. `pad` in dome2's `remote.launch.py`. |

## dome_semantic (1 file)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `semantic.launch.py` | `semantic_map_node`, plus a static `map → odom` TF if asked | `map_name`, `publish_every_n`, `static_map_odom` | 2026-11-05 | **Pass**: TF36.7 runs, `mon09` | **rename** to `robot.launch.py`. No `remote.launch.py` (decided 2026-11-17). New `semantic` subsystem in dome2. |

## dome_telemetry (1 file)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot.launch.py` | `battery_telemetry_node` | none | 2026-10-22 | **Pass**: `d b` in many runs | **keep** |

## dome_vision (3 files, in `dome_vision_ros/launch/`)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot.launch.py` | `dome_vision_ros_node` (lifecycle → active), `depth` and `publish_raw` fixed | `config` | 2026-11-13 | **Pass**: E1 (an empty config then fell back to `$DOME_VISION_CONFIG`; since F07 it means the installed `roboflow_oak.yaml`) | **keep**, taking in `dome_vision_ros.launch.py`'s arguments |
| `dome_vision_ros.launch.py` | Same node | `config` (required), `depth`, `perf`, `enable_embeddings` | 2026-09-02 | **Pass**: every semantic run | **merge** into `robot.launch.py`. Also fix `--depth false` doing nothing (a dome_vision bug). |
| `remote.launch.py` | Nothing | none | 2026-05-11 | Empty | **delete** |

## dome_viz (1 file)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `view.launch.py` | `bridge_node` and its web page | `sim_time`, `host`, `port` | 2026-11-15 | **Pass**: F03 on the VM | **rename** to `remote.launch.py` (decided 2026-11-17). Argument forwarding, including `--sim_time`, is fixed in F05. |

## dome_voice (2 files)

| File | Starts | Args | Last change | Status | Proposed |
|---|---|---|---|---|---|
| `robot.launch.py` | `voice_input`, `speech_output` | 5 args with `os.environ.get(...)` defaults | 2026-05-14 | **Fail**: E2b. `openwakeword` is missing and the voice board is out. | **keep but park**. It is the only voice launch file. Fix the defaults to literals. Re-test when the board is back. |
| `remote.launch.py` | `llm_node` (Whisper, Claude) | none | 2026-11-20 | New in dome_voice F14 | **keep**. The LLM command path's VM side; `voice` in dome2's `remote.launch.py`. |

## Summary of proposals

- **keep**: 5. `dome2` `robot`, `remote`; `dome_control` `robot`;
  `dome_telemetry` `robot`; `dome_vision` `robot`. Plus `dome_voice` `robot`,
  parked.
- **rename**: 4. `dome2` `gendrv` → `drivers`; `dome_nav` `robot_map` →
  `robot` (`--mode slam`); `dome_semantic` `semantic` → `robot`; `dome_viz`
  `view` → `remote`.
- **merge**: 1. `dome_vision_ros.launch.py`.
- **delete**: 10. Four dome2 wrappers; `dome_control` and `dome_voice`
  `remote`; `dome_vision` `remote`; `nav_experiment`,
  `nav2_experiment_navigation` and `just_explorer`.
- **blocked**: 3. `robot_nav`, `robot_explore`, `mission_explore`.
- **F06**: 6. The `sim_*` files.
- **decide**: none left. The remaining confirmations are in TF05.1.

## Things outside the launch files that must change too

- **`dome_semantic/tools/power_load_test.sh`** launches
  `dome_vision_ros.launch.py` and `semantic.launch.py` by name. It moves to
  dome2 anyway (current.md, Next). Update it when the names change.
- **Run procedures in docs** name these files. Examples: `dome_semantic`'s
  `notes.md` and `dome_nav`'s `02-doc/current.md` and `simhowto.md`.
  TF05.3's reference test finds the rest.
- **The sim** is F06's job, including its docs (`dome_nav`'s
  `simhowto.md`).
