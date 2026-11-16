# TF03 dome2 as the Stack Hub — Tasks for Feature F03

**Date Created:** 2026-11-16

## TF03.0 — Amend the spec

**Status**: done

**Description**: Replace `process/02-doc/spec.md`'s Scope with the four roles: launch orchestration, stack registry, cross-package operations, and stack-wide knowledge. dome2 runs on both robot and remote. Refresh the stale subsystem table so it lists every registered package with its role. Drop the outdated claim that `dome_vision` owns the semantic map.

**Test**: none, since this is a doc change. TF03.1's test checks that the registry and the spec's table agree.

## TF03.1 — Stack registry

**Status**: done

**Description**: `stack/packages.yaml` lists the 12 packages, each with `name`, `repo` (git URL) and `runs_on` (`robot` | `remote` | `both`). A pure loader in `dome2/stack_registry.py` validates the file once at load time: required fields present, `runs_on` in the allowed set, names unique. A bad entry raises with the package name.

**Test**: unit tests against the real file and against small malformed fixtures (missing field, bad `runs_on`, duplicate name, unknown role). Also a test that every registered package appears in the spec's subsystem table.

## TF03.2 — `make pull`

**Status**: done

**Description**: `dome2/stack_ops.py` with a `pull` command. It takes the workspace `src/` that dome2 sits in and checks that every registered package is present (missing ones are reported with a `git clone` line). It then runs `git pull --ff-only` in each one and prints a per-package result and a summary. Exit status is nonzero if anything failed. The pure parts (missing-package results, summarizing) are kept apart from the `subprocess` calls. The Makefile gets `pull: ## git pull every DOME package in the registry`. **Changed 2026-11-16:** it first pulled only the packages for a `$DOME_ROLE` host role; now it pulls all of them on either computer, and the role code is gone.

**Test**: unit tests for the pure planning and summary logic, with git calls mocked: unset or unknown role, missing package, one failing pull among several. A manual run on the robot is recorded in TF03.6.

## TF03.3 — Shared token parsing

**Status**: done

**Description**: Move `resolve_tokens` from `robot.launch.py` into `dome2/launch_options.py`, taking the subsystem list as an argument. `robot.launch.py` imports it, and its behavior is unchanged.

**Test**: the existing `test/test_launch_profiles.py` cases point at the new module and still pass.

## TF03.4 — `remote.launch.py`

**Status**: done

**Description**: `launch/remote.launch.py` mirrors `robot.launch.py`: `SUBSYSTEMS = ["viz"]`, `LAUNCH_FILES = {"viz": ("dome_viz", "view.launch.py")}`, the same `--profile` / `--options` / `--is_interactive` arguments, and a profile env var defaulting to `$DOME_REMOTE_PROFILE` or else `remote`. Like `start_nav`, it takes a literal `""` default because `bl` parses signatures statically.

**Test**: unit tests in the style of `test_launch_profiles.py` (better_launch stubbed): `v` resolves to `viz`, an unknown token warns, a missing profile env var raises, and the defaults are literals. Actually launching dome_viz is runtime-only and recorded manually in TF03.6.

## TF03.5 — `stack/` knowledge home

**Status**: done

**Description**: Create `stack/README.md` as the agent entry point. It covers what the stack is, the robot vs. remote split, a pointer to `packages.yaml`, and, for each package, where its spec and `current.md` live. It also lists the questions an architectural critique should cover. Move `process/02-doc/dome_developer_onboarding.md` into `stack/` with `git mv` and fix references to it. Add one line to CLAUDE.md: stack-wide or architecture questions start at `stack/README.md`. Add remote-computer setup (clone, pull, build) to `stack/README.md`.

**Test**: a unit test that every package in `packages.yaml` is mentioned in `stack/README.md`, so the index can't silently fall behind the registry.

## TF03.7 — `make clone`

**Status**: done

**Description**: Add a `clone` command to `dome2/stack_ops.py`. For each registered package it checks `--src/<name>`: if that path exists it is reported as already present and not touched; otherwise it runs `git clone <repo> <src>/<name>`. Each result is printed, failures don't stop the rest, and the exit status is nonzero if any clone failed.
- `PullResult` becomes a general `PackageResult` shared by both commands, and the summary line names the operation.
- `make pull`'s missing-package message now says to run `make clone`.
- The Makefile gets `clone: ## git clone every registered DOME package that is missing`.
- `stack/README.md`'s remote setup becomes: clone dome2, `make clone`, `colcon build`.

**Test**: unit tests with git mocked: missing packages are cloned to the peer path from their registry repo, present ones are skipped with no git call, and one failed clone doesn't stop the others and sets exit status 1. A manual check on the robot (all 12 already present, so nothing to clone) is recorded in TF03.6, and the real clone run on the VM goes there too.

## TF03.6 — Test-writing and manual verification

**Status**: done

**Description**: Fill any unit-test gaps left by TF03.1–TF03.5 and TF03.7 (edge cases: empty registry, `both` packages selected under each role). Record manual test notes (command, setup, expected, actual) for:
- `make pull` on the robot.
- `make pull` on the VM.
- `bl dome2 remote.launch.py --options "v"` on the VM.

**Progress (2026-11-16):** unit gaps filled (empty registry, literal-default regression for both launchers); 42 tests pass after the role code was removed. Done on the robot: `colcon build`, `bl dome2 robot.launch.py --help` and `remote.launch.py --help` show the three options; **Manual run, robot, 2026-11-16:** `export DOME_ROLE=robot` added to `~/.bashrc`; `make pull` in `~/ros2_ws/src/dome2`. Expected: the 11 robot-role packages pulled, dome_viz skipped. Actual: "Pulling 11 packages for role 'robot'", all 11 ok (already up to date), exit 0. **Re-run after the all-packages change, 2026-11-16:** `make pull` with no `DOME_ROLE`: "Pulling 12 packages", all 12 ok, exit 0; dome_viz fast-forwarded to `origin/main`. **`make clone`, robot, 2026-11-16:** all 12 already present, nothing cloned, exit 0. A one-entry registry pointed at a scratch `src/` cloned `dome_nav_msgs` for real, and a second run reported it already present. 51 tests pass. **Remote launch, VM, 2026-11-16:** after clearing a stale `build/dome_telemetry_msgs` (its cache still pointed at the old `src/dome_vision/dome_telemetry_msgs` location), `colcon build` succeeded. `bl dome2 remote.launch.py --options "v"` included `view.launch.py`, started `dome_viz_bridge`, and logged `http://192.168.4.83:8080/`. Expected and actual match. **`make clone` and `make pull`, VM, 2026-11-16:** both run by the user on the VM and reported working (output not pasted).

**Test**: this is the test task. The manual runs need the robot and the VM, so they are kept out of the plain test run.
