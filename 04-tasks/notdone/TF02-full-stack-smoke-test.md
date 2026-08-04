# TF02 Full-Stack Smoke Test — Tasks for Feature F02

## T01 — Stage spec (pure data)
**Status**: not done
**Description**: A pure Python module defining the four smoke-test stages in
order — name, launch package/file (or `ros2 run` command), settle-time
seconds, and expected nodes/topics/actions for that stage. No ROS imports.
Test: a plain unit test asserting the stage list is well-formed (unique
names, non-empty expected sets, ascending order) — no ROS graph needed.

## T02 — Health-check logic (pure)
**Status**: not done
**Description**: Pure function(s) taking a stage's expected
nodes/topics/actions plus the actual observed sets (as plain lists/sets —
caller is responsible for querying the live ROS graph) and returning a
pass/fail verdict with the specific missing items. No ROS imports, no
subprocess calls. Test: unit tests with fixture input covering full match,
missing node, missing topic, missing action, and empty-actual-set.

## T03 — Orchestration tool
**Status**: not done
**Description**: The runtime seam: for each stage in order, launch it (via
`better_launch`'s `bl.include`, matching the existing launch files), wait the
settle time, query the live graph (`ros2 node list` / `topic list` /
`action list`, or the equivalent rclpy graph API), run it through T02's
checker, print a pass/fail report, and pause for operator confirm/abort
before the next stage (reuse the confirm-prompt pattern from
`robot.launch.py --is_interactive`). On fail, stop and leave prior stages
running. Hardware/runtime-only — no plain-suite test; manual test notes
required (command, setup, expected observation, actual result) once run on
the Pi.

## T04 — Wire in nav + mission stages
**Status**: not done
**Description**: Extend T03's stage list with stage 3 (dome_nav — operator
chooses `robot_map.launch.py` for a fresh map or `robot_explore.launch.py`
to reuse/extend one, passing `map_name` through) and stage 4 (dome_mission —
`ros2 run dome_mission mission_node`, checked as the sole `/intent`
subscriber and `ExploreArea` client). Hardware/runtime-only, same as T03 —
manual test notes required.

## T05 — Docs
**Status**: not done
**Description**: README section in dome2 describing the smoke-test tool and
how to run it; `01-literate/` entries for the new pure modules (T01/T02);
update dome2's `02-doc/current.md` once the feature closes.

## T06 — Test-writing task
**Status**: not done
**Description**: Dedicated pass to fill in unit test coverage for T01/T02
(edge cases: empty stage list, all-missing, partial-missing, exact match) and
to record T03/T04's manual test notes (command run, robot setup, expected
vs. actual observation per stage) after a real run on the Pi.
