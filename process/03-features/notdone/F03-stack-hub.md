# F03 — dome2 as the Stack Hub

**Priority**: High

**Date Created:** 2026-11-16

**Done:** no

**Tasks File Created:** yes

**Tests Written:** no

**Test Passing:** no

**Description**: dome2 becomes the hub for the whole DOME software stack, not just the robot's launcher. It lives on both the robot and the remote computer.

## Scope

- **Stack registry:** one file listing every DOME package, with its repo and where it runs (`robot`, `remote` or `both`).
- **Cross-package operations:** `make clone`, which clones every registered package that isn't checked out yet, and `make pull`, which runs `git pull` on all of them.
- **Stack-wide knowledge:** a `stack/` folder for docs about the whole stack, robot and remote. Its `README.md` is where agents start for an architectural critique.
- **Remote launcher:** `remote.launch.py`, with the same `--profile` / `--options` / `--is_interactive` interface as `robot.launch.py`. Its only subsystem at first is `viz` (`bl dome_viz view.launch.py`).

## Decisions

- **The registry covers `dome2`, the `dome_*` packages and the `*_msgs` packages** (12 in all). The old `campusrover/dome` repo and the non-DOME dependencies (`yellow_pad`, `better_launch`, `linorobot2`) are left out.
- **`make pull` pulls every registered package on either computer** (changed 2026-11-16; it first selected by a `$DOME_ROLE` host role). Both computers keep the whole stack checked out, and `runs_on` only records where a package runs.
- **`make clone` fills in missing packages** (added 2026-11-16). After cloning dome2, `make clone` clones every other registered package as a peer directory (`../<name>`) from its registry `repo`. A package that is already there is left alone, whatever its state. A failed clone is reported, the rest still run, and the exit status is nonzero.
- **`make pull` still treats a missing package as an error** and points to `make clone`. It never clones by itself, so a pull can't silently add repos.
- **Pulls are `git pull --ff-only`.** Each package that fails (dirty tree, diverged branch, network error) is reported. The rest still run, the summary lists the failures, and the exit status is nonzero.
- **Token parsing is shared.** `resolve_tokens` moves out of `robot.launch.py` into a pure `dome2/launch_options.py` that both launchers import, so the two can't drift apart.
- **The `remote` profile reads `$DOME_REMOTE_PROFILE`** (default `remote`), mirroring `$DOME_PROFILE` on the robot side.
- **Stack-wide docs move to `stack/`.** `process/02-doc/dome_developer_onboarding.md` covers the whole stack, so it moves there. `process/` stays for dome2's own features, tasks and issues.

## Out of scope

- Other cross-package operations (status, build, test). Each gets its own feature when wanted.
- Moving robot functionality to the remote computer. This feature only provides the place to put it.
- The power load test move from `dome_semantic` (its own item in `current.md`).

## How to Demo

**Setup**: dome2 is built on both the robot and the remote VM, with every registered package checked out on each.

**Steps**:
0. On the VM, clone dome2 into `~/ros2_ws/src` and run `make clone` there.
1. On the robot, run `make pull` in `dome2`.
2. On the VM, run `make pull` in `dome2`.
3. On the VM, run `bl dome2 remote.launch.py --options "v"`.
4. Open `stack/README.md` and check it points to every package's spec and to the critique checklist.

**Expected output**:
- `make clone` on the VM clones the 11 missing packages; a second run reports all 12 already present.
- Each `make pull` lists all 12 packages with their pull results, and ends with a summary.
- The VM starts dome_viz's bridge and logs the page URLs.
- `stack/README.md` lists all 12 packages. Writing an actual critique is not part of this feature.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
