# TF05 Consistent, correct launch files across the DOME stack, for Feature F05

**Date Created:** 2026-11-17

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.

Each step is numbered `TFNN.N`, matching this file's own `TFNN` (e.g. `TF03.0`,
`TF03.1`, ...), starting at `.0`.

For each task step, add a test when feasible. If not feasible, note why.

## TF05.0 — Inventory every DOME launch file

**Status**: done

**Description**: Write `stack/launch_inventory.md`. It gets one row per
launch file in the 12 registered packages, with these columns:

- path
- what it starts
- its arguments
- what it includes
- its last commit date
- whether dome2 or another launch file references it

The inventory covers **30 files**. dome2 has 7, dome_control 2,
dome_mission 1, dome_nav 12, dome_semantic 1, dome_telemetry 1, dome_vision 3,
dome_viz 1 and dome_voice 2. An earlier count of 33 was wrong.

Each row also gets a proposed verdict: **keep**, **merge into
`robot`/`remote`**, or **delete**.

**Test**: none, because this is a document. TF05.6 checks the inventory
against the launch folders.

**Result (2026-11-17):** `stack/launch_inventory.md`. Proposed: 6 keep (plus
voice, parked), 2 rename, 1 merge, 9 delete, 3 blocked, 6 sim files left to
F06, and 3 for the user to decide.

## TF05.1 — Run the experiments, then settle the decisions with the user

**Status**: done

**Description**: The user runs these on the robot, since launching can move
it. Record each result in the inventory.

- **E1:** `bl dome2 robot.launch.py --options "d vi"`. Does the vision
  subsystem start through dome2, given that its wrapper passes no config?
- **E2:** `d c`, `d vo`, `d f` and `d y`, one at a time. Do control, voice,
  foxglove and yellow each start cleanly on Kilted? Check their nodes and
  topics, and watch the logs for errors.
- **E3:** SLAM without Nav2: `slam_toolbox` with `dome_nav`'s
  `mapper_params_online_async.yaml`, plus `d b`. Record the load and the
  EKF rate. This is the baseline for a SLAM-only option.

**Results so far (2026-11-17):**

- **E1 `d vi`: pass.** `dome_vision` reached `active`, and image and
  detections ran at 10 Hz. An empty `config` falls back to
  `$DOME_VISION_CONFIG` (`node.py:165`).
- **E2a `d c`: pass.** `behavior_manager`, `telemetry` and `spin_survey` all
  came up. Stopping the launch printed `ExternalShutdownException`
  tracebacks. That is fixed stack-wide; see the chore in `chores.md`.
- **E2b `d vo`: fail. Not demonstrated.** `voice_input` crashes with no
  `openwakeword` module; it is not installed and not declared in
  `package.xml`. `speech_output` runs and stops cleanly. The voice board is
  not installed. The launch has no hardware check, and ALSA still lists
  `seeed2micvoicec` with the board out.
- **E2c `d f`: pass.** `foxglove_bridge` 3.4.1 listens on 8765. It accepts
  only the `foxglove.sdk.v1` subprotocol, so older clients can't connect.
- **E2d `d y`: pass.** The Yellow Pad drove the robot; tested by the user.
- **E3 SLAM without Nav2 (`d b` + raw `slam_toolbox` launch): pass.**

  | Measure | Value |
  |---|---|
  | Load | 1.3 (startup peak 2.35) |
  | EKF `/odom` | 29.8 Hz, max gap 0.33 s |
  | `/scan` | 9.7 Hz |
  | `/map` | about 0.17 Hz |
  | `map → odom` | published |

  A `bl` SLAM-only option on `robot_map.launch.py` would cover this setup.
- **E3 re-run: `slam_toolbox` didn't always activate.** On Kilted it's a
  lifecycle node. In one of two starts, the reply to the launch file's
  configure request timed out (`failed to send response to
  /slam_toolbox/change_state`). Activate was never sent, so the node stayed
  `inactive` with no `/map` until activated by hand. Any `bl` launch that
  includes SLAM must make sure it reaches `active`.
- **The SLAM params copy is stale.** `dome_nav`'s
  `mapper_params_online_async.yaml` carries three keys that Kilted's
  `slam_toolbox` 2.9.0 ignores, including `message_queue_size`. The fix is
  to start again from Kilted's upstream file and re-test each change. That
  is tracked in `dome_nav` I13, not here. F05's SLAM-only option uses
  whatever params file I13 produces.
- **A sparse map is expected with little driving.** SLAM adds a scan only
  every 0.5 m or 0.5 rad of motion (`minimum_travel_*`) and redraws the map
  every 10 s. Beyond about 3 m, the ~455-beam scan's rays are more than one
  5 cm cell apart.
- **Still to do:** a live clean-stop check of the dome_control nodes.

- **E5 (to run):** `bl dome2 robot.launch.py --is_interactive`. The F04
  prompt never appeared under better_launch's UI (`ui=True` owns the
  terminal), so `--is_interactive`'s `click.confirm` questions may hang the
  same way. If they do, drop `--is_interactive` or launch without the UI.

A file or option is kept only if it passes here or already has a pass on
record.

**Decisions settled with the user (2026-11-17):**

1. **`view.launch.py` → `remote.launch.py`** in dome_viz. Update dome2's
   `remote.launch.py` and dome_viz's Makefile.
2. **Argument forwarding is fixed in F05** (TF05.4). dome2's launchers pass
   chosen arguments (`--sim_time`, `--map_name`, later `--explore_params`)
   to the files they include. F06 uses the same mechanism.
3. **`gendrv.launch.py` → `drivers.launch.py`**, to match the subsystem name.
4. **dome_semantic gets no `remote.launch.py`.** Only `robot.launch.py`.
5. **New `slam` and `semantic` subsystems in dome2's `robot.launch.py`.**
   The semantic-mapping run becomes one command, e.g.
   `--options "d b s vi se" --map_name <name>`.
6. **`just_explorer.launch.py` is deleted.** F06 replaces it.

7. **The inventory's other proposals are confirmed**: the 10 deletions, the
   `dome_nav` and `dome_semantic` renames, the vision merge, voice parked,
   and the I13-blocked files left alone.

**E5 moves to TF05.7**, because it only affects `--is_interactive`. The
convention is written in `stack/launch_conventions.md`.

The inventory now holds the final verdicts. The convention in
`stack/launch_conventions.md` covers:

- file names
- argument style, including better_launch's limits: no `X | None`, and
  literal defaults only
- header and docstring
- how top-level files include package-level ones

**No edits to launch files before this step is approved.**

**Test**: none, because these are decisions. The convention becomes
TF05.6's test rules.

## TF05.2 — Make package-level launch files match the convention

**Status**: in progress

**Progress:**

- **dome_control: done** and passes TF05.6 (`9046e75`, not pushed).
  Header, usage and docstrings added. `spin_survey`'s params moved to
  `config/spin_survey.yaml` with the same values, plus
  `test_spin_survey_params.py`. The header-stamping hook was installed,
  since the repo had none. `remote.launch.py` is left for TF05.3.

**Description**: Work one package at a time: dome_control, dome_mission,
dome_nav, dome_semantic, dome_telemetry, dome_vision, dome_viz, dome_voice.

- Merge kept variants into `robot.launch.py` / `remote.launch.py` as
  optional arguments.
- Add the standard header, usage examples and docstrings.
- Rename entry functions consistently.

Each package gets its own commit in its own repo.

**Test**: TF05.6's static convention test. Also, for each package, `bl
<pkg> <file> --help` must parse without error. That check is manual and
only on the robot, because it needs the built workspace.

## TF05.3 — Delete files that didn't make the cut

**Status**: not done

**Description**: Remove every launch file whose final verdict is **delete**
or **merged**. Also remove stale references to them:

- READMEs
- package specs and `current.md`
- dome2's `robot.launch.py` comment block
- `stack/README.md`

Before any `git rm`, list exactly what will be deleted in each repo and get
the user's approval.

**Test**: TF05.6 fails if a deleted file is still referenced from any
launch file, README or `stack/` doc.

## TF05.4 — Point dome2's top-level launchers at package-level files

**Status**: not done

**Description**:

- Replace the dome2 wrapper files (`dome_control.launch.py`,
  `dome_vision.launch.py`, `dome_voice.launch.py`, `foxglove.launch.py`)
  with direct entries in `LAUNCH_FILES`.
- Keep `gendrv.launch.py` (or rename it to the convention), since dome2 owns
  the driver bringup.
- Add nav/mission subsystems if TF05.1 decided to.
- Fix the `--sim_time` pass-through if TF05.1 decided to.
- Update `remote.launch.py` with any remote subsystems that were agreed.
  The sim is not one of them: it is F06.

**Test**: Extend `test/` to check that every `LAUNCH_FILES` entry in
`robot.launch.py` and `remote.launch.py` names a launch file that exists in
that package's source tree, for both DOME and non-DOME targets.

## TF05.5 — Update stack docs

**Status**: not done

**Description**: Bring `stack/README.md`'s "Launching" section and
`process/02-doc/spec.md`'s orchestration scope in line with the final
convention and subsystem list. Point both to `stack/launch_conventions.md`.

**Test**: The existing `test_stack_registry.py` keeps passing. TF05.6 checks
that every subsystem named in the docs exists in `LAUNCH_FILES`.

## TF05.6 — Write the launch-convention test suite

**Status**: in progress. Written ahead of TF05.2's other repos (2026-11-17),
so each repo is checked as it is converted.

**Progress:**

- **`test/test_launch_conventions.py` is written.** It covers every check
  below. With `/usr/bin/python3 -m pytest` the result is 49 passed, 9
  skipped (known exceptions) and 22 xfailed.
- **Unconverted files are strict xfails**, listed in `NOT_YET_CONVERTED`.
  Each F05 step removes the entries it fixes. A listed entry that starts
  passing fails the run, so the list can only shrink. The task is done when
  the list is empty.
- **The inventory test compares** each repo's files with the inventory rows
  whose verdict is keep, blocked or F06. So TF05.3 must also rewrite the
  renamed rows under their new names as **keep**.
- **The stale-reference check leaves out** `launch_inventory.md` and
  `launch_conventions.md`, which name deleted and planned files on purpose.
- **`colcon test` runs 0 tests in dome2.** This was already true before
  this file, and it still needs fixing.

**Description**: Add `test/test_launch_conventions.py` to dome2. It is
static, parses files with `ast`, and never launches anything. For every
registered package checked out next to dome2, it checks:

- Only allowed file names are in `launch/`. Agreed exceptions are listed in
  `stack/launch_conventions.md`.
- Each file has the standard header and a `@launch_this` entry function
  with literal defaults.
- No file imports `launch` / `launch_ros` or builds a
  `LaunchDescription`. Every launch file is better_launch only.
- A package-level launch file never includes another registered DOME
  package. Outside packages are allowed. Only dome2 may combine DOME
  packages. Files blocked on I13 are listed as known exceptions.
- No launch file, README or `stack/` doc references a launch file that no
  longer exists.
- Every top-level `LAUNCH_FILES` target exists.
- Every subsystem named in `stack/README.md` exists in `LAUNCH_FILES`.
- The inventory's **keep** rows match the files that actually exist.

If a registered package isn't checked out, its checks are skipped and the
reason is reported.

**Test**: This task is the test suite. Run it with `uv run pytest` and
`colcon test`.

## TF05.7 — Verify on the robot and the remote computer

**Status**: not done

**Description**: Run the F05 demo by hand:

- Every demonstrated `--options` combination on the robot.
- `remote.launch.py` on the VM.
- One package-level file run on its own.
- **E4:** the semantic-mapping run from one top-level command, compared
  with the four-terminal procedure in `dome_semantic`'s notes.
- **E5:** `bl dome2 robot.launch.py --is_interactive`. Do the yes/no
  questions appear under better_launch's UI, or hang like F04's prompt? If
  they hang, drop `--is_interactive` or launch without the UI.

Record the results in the feature file.

**Test**: manual only. Per CLAUDE.md, launching can move the robot, so
runtime launch tests stay out of the automated suite.
