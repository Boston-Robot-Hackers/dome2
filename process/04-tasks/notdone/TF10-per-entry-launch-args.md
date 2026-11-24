# TF10 Per-entry launch arguments, for Feature F10

**Date Created:** 2026-11-23

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.

Each step is numbered `TFNN.N`, matching this file's own `TFNN` (e.g. `TF03.0`,
`TF03.1`, ...), starting at `.0`.

For each task step, add a test when feasible. If not feasible, note why.

## TF10.0 — Spike: can better_launch do this?

**Status**: done (2026-11-23)

**Result: both work.** Read in `better_launch/launcher.py` (`include`) and
`wrapper.py` (`launch_this`), then confirmed by running a throwaway top/child
pair with `--unit fromcli --map_name` defaulted to `m1`:

| Include | Child received |
|---|---|
| `include(child, unit="slam")` | `unit='slam'`, `map_name='m1'` |
| `include(child, unit="nav2")` | `unit='nav2'`, `map_name='m1'` |
| `include(child)` | `unit='fromcli'`, `map_name='m1'` |

- **Same file twice: works.** Each include re-`exec`s the file with fresh
  globals and calls its entry function again.
- **Per-include args win.** `include` applies the launcher's `launch_args`
  first, then `**kwargs` on top. The child gets only names it declares.
- **Two consequences for TF10.2:**
  - Per-include values are passed **as-is, not converted by click**, so the
    value's Python type must already match the target's annotation.
  - A per-entry name that the launcher *also* declares silently overrides the
    forwarded value for that entry. Forbid the overlap rather than rely on it.

**Description**: Settle the two unknowns before any design is fixed. Use a
throwaway pair of better_launch files in the scratchpad, not the real ones.

- Include the **same file twice** in one launch with different arguments
  (`unit=a`, `unit=b`). Do both run?
- Give an include a **per-include argument** that has the same name as one the
  top-level launcher declares. Which value does the included file see?

Record both answers in this file. If either fails, stop and redesign with the
user before TF10.1.

**Test**: none — this is an experiment. Its result decides whether TF10.1 can
use `bl.include(..., **args)` as planned.

## TF10.1 — Optional per-entry arguments in `launch_subsystems`

**Status**: done (2026-11-23)

**Result:** `launch_options.py` gained a `LaunchEntry` type and a pure
`entry_parts(entry)` that splits an entry into package, file and per-entry
args (`{}` for two elements; other lengths raise). `launch_subsystems` uses it
and calls `bl.include(pkg, file, **entry_args)`. Tests:
`TestEntryParts` and `TestLaunchSubsystemsIncludes` in
`test_launch_profiles.py`. dome2 suite: 137 passed, 9 skipped (with
`/usr/bin/python3 -m pytest`; `uv` isn't installed on the Pi).

**Description**: Accept `(package, file)` and `(package, file, args)` entries
in `LAUNCH_FILES`. Pass `args` to `bl.include`. The type hint widens
accordingly.

**Test**: a unit test with a fake `BetterLaunch` that records `include` calls.
Check that a 3-element entry passes its args, a 2-element entry passes none,
and selection still follows `--options`.

## TF10.2 — Convention tests for per-entry arguments

**Status**: done (2026-11-23)

**Result:** `test_launch_conventions.py` reads entries through
`entry_parts` everywhere. New pure `entry_arg_violations` (plus
`value_fits`) checks the four rules below; `test_per_entry_args_fit_their_target`
runs it over both launchers, and a parametrized test feeds it one bad case
per rule. Suite: 145 passed, 9 skipped. The real launchers carry no per-entry
args until TF10.4, so that test passes trivially for now.

**Description**: Extend `test/test_launch_conventions.py`.

- Accept both entry shapes everywhere `LAUNCH_FILES` is read.
- **Each per-entry argument is declared by its target**, with a type that
  accepts the given value.
- **Per-entry arguments are left out of the forwarded-argument check**
  (`test_forwarded_args_reach_a_target_with_the_same_type`). They are fixed
  per entry, not forwarded.
- A per-entry argument may not be `profile`, `options` or `is_interactive`.
- **A per-entry argument may not share a name with an argument the launcher
  declares** (`sim_time`, `map_name`), since it would silently override the
  forwarded value (TF10.0).
- **The per-entry value's Python type matches the target's annotation** —
  include values are not converted by click (TF10.0).

**Test**: this task is tests. Add a failing-case fixture for each new rule.

## TF10.3 — Write the rule into `stack/launch_conventions.md`

**Status**: done (2026-11-23) — *Per-entry arguments* bullet under
*Top-level launchers*, and a new *Placement: robot or remote* section.

**Description**: Add to the *Top-level launchers* section:

- the placement rule (offer every sub-launch that *can* run on each side;
  "either" sub-launches appear in both; operator chooses),
- per-entry arguments and when to use them,
- double starts being the operator's responsibility.

**Test**: none (document). TF10.2 enforces the checkable parts.

## TF10.4 — Add dome_nav's units to both launchers

**Status**: done (2026-11-23)

**Result:** robot: `slam`, `nav2`, `explorer` → `dome_nav robot.launch.py`
with `{"unit": ...}`, after `drivers`. Remote: `slam`, `explorer` →
`dome_nav remote.launch.py`; `remote.launch.py` now also declares and
forwards `map_name`. Prefixes stay unambiguous (`sl`/`se`, `n`, `e`). Header
usage shows explore all-on-robot and explorer-on-remote. New tests:
`test_dome_nav_units_share_one_file`, `test_dome_nav_units_use_its_remote_file`,
`test_nav2_is_robot_only`. `bl dome2 robot.launch.py --help` and
`remote.launch.py --help` parse after a rebuild.

**Description**:

- `robot.launch.py`: `slam`, `nav2`, `explorer` → `dome_nav robot.launch.py`
  with `{"unit": ...}`. `nav2` is robot-only for now.
- `remote.launch.py`: `slam`, `explorer` → `dome_nav remote.launch.py`.
- Check token prefixes stay unambiguous (`sl`/`se` already exist).
- Update the header usage examples, including an explore option set.

**Test**: TF10.2's checks cover the entries; the existing launcher-file
existence test covers the targets.

## TF10.5 — Test-writing pass

**Status**: done (2026-11-23) — dome2 suite 150 passed, 9 skipped.

**Description**: Make sure every new behavior from TF10.1–TF10.4 has a test,
and the full dome2 suite passes with `uv run pytest`.

**Test**: the suite itself.

## TF10.6 — Verify on the robot and the VM

**Status**: done (2026-11-23)

**Result:** robot `bl dome2 robot.launch.py --options "d sl n" --map_name
n2301`, VM `bl dome2 remote.launch.py --options "e" --map_name n2301`.
`ros2 node list --no-daemon --spin-time 10` from the robot showed
`slam_toolbox`, `slam_manager` and the Nav2 servers (incl. `bt_navigator`)
on the robot and `explore_manager` from the VM, each once;
`slam_toolbox` reached `active`. The VM's explorer sent `navigate_to_pose`
goals and Nav2 answered each. (Exploration itself then failed on a phantom
start obstacle — dome_nav I14/I17, not a placement problem.)

**Gotcha:** `ros2 node list --no-daemon` uses a short default
`--spin-time`, too short to discover the other machine over wifi. Use
`--spin-time 10`, or the daemon.

**Description**: Run the F10 demo by hand: `slam` + `nav2` on the robot,
`explorer` on the VM, and confirm each node starts once on the intended
machine. Record the commands and what `ros2 node list` showed.

**Test**: manual only — launching can move the robot.
