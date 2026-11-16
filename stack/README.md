# The DOME Software Stack

This folder holds what is true of the DOME stack as a whole, robot and remote. Each package's own docs cover that package only.

**Agents asked about the whole stack, or for an architectural critique, start here.**

## Two computers

- **The robot**: a Raspberry Pi 5 running ROS 2 Kilted (`/opt/ros/kilted`). It runs the drivers, control, navigation, mission, perception, voice and telemetry. It has little CPU to spare.
- **The remote computer**: an Ubuntu VM in VMware on the Mac mini, on the same Wi-Fi DDS network (bridged networking). For now it runs only `dome_viz`. Work that doesn't have to be on the robot should move here over time.

dome2 is checked out on both. **Both computers keep every DOME package checked out**, whichever computer it runs on.

## The registry

[`packages.yaml`](packages.yaml) is the single list of DOME packages: name, repo, and `runs_on` (`robot`, `remote` or `both`). Cross-package tools act on every entry; `runs_on` records where a package runs, not where it is checked out.

When a package is added or moves between computers:

- Update `packages.yaml`.
- Update the table in `process/02-doc/spec.md`.
- Update the package list below.

`test/test_stack_registry.py` fails if any of these three disagree.

## Packages

Each package keeps its spec and session handoff in its own repo. Older packages use `02-doc/`; packages on the newer process kit use `process/02-doc/`.

| Package | Runs on | Spec and `current.md` |
|---|---|---|
| `dome2` | both | `process/02-doc/` |
| `dome_control` | robot | `02-doc/` |
| `dome_mission` | robot | `02-doc/` |
| `dome_nav` | robot | `02-doc/` |
| `dome_nav_msgs` | robot | none (interfaces only: `ExploreArea` action) |
| `dome_semantic` | both | `process/02-doc/` |
| `dome_semantic_msgs` | both | none (interfaces only: `SemanticTarget`, `SemanticTargetArray`) |
| `dome_telemetry` | robot | `02-doc/` |
| `dome_telemetry_msgs` | both | none (interfaces only: `BatteryStats`, `OakStats`) |
| `dome_vision` | robot | `process/02-doc/` |
| `dome_viz` | remote | `process/02-doc/` |
| `dome_voice` | robot | `02-doc/` |

All of them sit side by side in the workspace `src/` directory (`~/ros2_ws/src/<package>`).

## Launching

- **Robot**: `bl dome2 robot.launch.py --options "d c vi"`. Subsystems: drivers, control, vision, voice, foxglove, battery, yellow. Nav is launched separately from `dome_nav`.
- **Remote**: `bl dome2 remote.launch.py --options "v"`. Subsystems: viz.

Both take `--profile <env var>` (defaults `$DOME_PROFILE` / `$DOME_REMOTE_PROFILE`) and `--is_interactive`.

## Cross-package operations

Run from the dome2 checkout:

- `make clone` clones every registered package that isn't checked out yet, next to dome2 (`../<name>`). Packages already there are left alone.
- `make pull` runs `git pull --ff-only` in every registered package. A missing package is reported as a failure that points to `make clone`.

Both keep going past a failure, list every failure at the end, and exit nonzero if there was any.

## Setting up the remote computer

1. Clone dome2 into the workspace: `git clone git@github.com:Boston-Robot-Hackers/dome2.git ~/ros2_ws/src/dome2`.
2. Run `make clone` in `~/ros2_ws/src/dome2`. It clones the other 11 packages next to dome2.
3. From `~/ros2_ws`, run `colcon build`, then `source install/setup.bash`.
4. Run `bl dome2 remote.launch.py --options "v"`.

## Other stack-wide docs

- [`dome_developer_onboarding.md`](dome_developer_onboarding.md): topics, services, messages, intent flow, and how to add CLI and voice commands. **It predates `dome_nav`, `dome_mission`, `dome_semantic` and `dome_viz`**, so check claims about those against their specs.

## Architectural critique: what to cover

Read the registry and each package's spec first, then look at the code. Cover:

- **Ownership:** does each topic, service and action have one clear owner? Known gap: `/intent` has two uncoordinated subscribers (`dome_control`'s F19).
- **Dependencies:** do they point one way? Pure logic should stay free of ROS, and `*_msgs` packages should be the only shared types.
- **Robot vs. remote:** what runs on the Pi that could move to the remote computer, given the Pi's CPU budget?
- **Duplication:** logic or config repeated across packages.
- **Failure and startup:** what happens when a subsystem is absent or late (hardware missing, DDS link lost)?
- **Drift:** where package docs and code disagree, starting with the onboarding guide.
