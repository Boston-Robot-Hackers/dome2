# F10 — Per-entry launch arguments, so one package file can serve several subsystems

**Priority**: High

**Date Created:** 2026-11-23

**Done:** no

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes (dome2 150 passed, 9 skipped; TF10.6 robot/VM run pending)

**Description**: dome2's top-level launchers can't select part of a package's
launch file. `LAUNCH_FILES` maps a subsystem to a `(package, file)` with no
arguments, so one package file can only be one subsystem.

dome_nav needs more than that. Its nodes are grouped into **units** (`slam`,
`nav2`, `explorer`, later `localization`) that are placed separately: some on
the robot, some on the remote computer (dome_nav F36). Each unit must be its
own selectable subsystem, while dome_nav keeps one `robot.launch.py` and one
`remote.launch.py`, as the convention requires.

### The placement rule (decided 2026-11-23)

- **`robot.launch.py` offers, as `--options` subsystems, every sub-launch that
  *can* run on the robot.**
- **`remote.launch.py` offers every sub-launch that *can* run remotely.**
- A sub-launch that can run on either machine appears in **both**. The operator
  chooses where it runs by which side's `--options` selects it.
- Robot-only sub-launches (e.g. the safety stop) appear only in
  `robot.launch.py`.
- **Double starts are the operator's responsibility.** Selecting the same unit
  on both sides starts it twice. No guard is built.

### The mechanism

- A `LAUNCH_FILES` entry gets an **optional third element**: a dict of fixed
  arguments for that subsystem.

  ```python
  "slam":     ("dome_nav", "robot.launch.py", {"unit": "slam"}),
  "nav2":     ("dome_nav", "robot.launch.py", {"unit": "nav2"}),
  "explorer": ("dome_nav", "robot.launch.py", {"unit": "explorer"}),
  ```

- `launch_subsystems` passes them through: `bl.include(pkg, file, **args)`.
- Two-element entries keep working unchanged.
- **Modes become option sets.** dome_nav's explore mode is
  `--options "... sl nav2 explorer"`, which can be saved as a profile.

### Scope

- **In scope:** `subsystem_launcher.py`, both launchers' `LAUNCH_FILES`, the
  convention text in `stack/launch_conventions.md`, and
  `test/test_launch_conventions.py`.
- **Out of scope:** dome_nav's own unit split (dome_nav F36), and splitting
  Nav2 so its planner/controller can run remotely (deferred; the `nav2` unit is
  robot-only for now).

### Unverified — settled by TF10.0

- better_launch may not allow **including the same file twice** in one launch.
- A per-entry argument may not take precedence over the same-named argument
  forwarded from the top-level launcher.

## How to Demo

**Setup**: robot and VM built from the updated dome2 and dome_nav (dome_nav F36
done for at least `slam` and `explorer`).

**Steps**:
1. `uv run pytest` in dome2 — convention tests pass, including the new
   per-entry argument checks.
2. On the robot: `bl dome2 robot.launch.py --options "d sl nav2"
   --map_name <name>`.
3. On the VM: `bl dome2 remote.launch.py --options "explorer"
   --map_name <name>`.
4. `ros2 node list` shows `slam_toolbox` and Nav2 on the robot and
   `explore_manager` on the VM, each started once.

**Expected output**: one dome_nav package file serves three subsystems, split
across two machines by `--options` alone.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
