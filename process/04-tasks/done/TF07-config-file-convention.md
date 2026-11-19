# TF07 Config files follow one convention; no config-path env vars (F07)

**Date Created:** 2026-11-19

Each package gets its own commit in its own repo.

## TF07.0 — dome_vision: launch passes the installed config; no env var

**Status**: done (2026-11-19)

**Description**:

- `robot.launch.py`: `config: str = ""`, and the body passes `config or bl.find("dome_vision_ros", "roboflow_oak.yaml")`.
- `node.py` `on_configure`: remove the `DOME_VISION_CONFIG` fallback. An empty `config` fails configure with a clear error.
- Update `test_node.py`'s env-var tests and `test_launch_args.py`.
- `dome_vision_ros.launch.py` already requires `--config`, and is deleted in F05's TF05.3.

**Test**:

- The launch passes the installed path when `--config` is empty, and the given path otherwise.
- An empty `config` fails configure, even with `DOME_VISION_CONFIG` set in the environment.

**Result:** `node.py` no longer reads `DOME_VISION_CONFIG`, and the unused `import os` is gone. The launch passes `config or bl.find(...)`. New `test_robot_launch_defaults_to_the_installed_config`. The empty-config test now sets the variable, to prove it is ignored. dome_vision_ros: 95 passed; dome_vision: 217.

## TF07.1 — dome_voice: path by parameter; rename to `voice.yaml`

**Status**: done (2026-11-19)

**Description**:

- `git mv config/voice_config.yaml config/voice.yaml`.
- `runtime.py`: delete `TUNE_CONFIG_ENV_VARS`. `load_voice_runtime_config(path)` uses `path`, or the defaults when it is `None`.
- `voice_input_node.py`: declare a `config` string parameter and load from it. An empty value is an error at startup, as in dome_vision. Only the ROS-free CLI (`python3 -m dome_voice.runtime`) runs on the defaults.
- `robot.launch.py`: pass `config` = `bl.find("dome_voice", "voice.yaml")` to `voice_input`.
- `test/conftest.py` is no longer needed; delete it. Update the config tests and I01's note.

**Test**:

- With a config variable set, the loader ignores it.
- The launch test checks that `voice_input` gets the installed `voice.yaml`.
- The baseline test reads `config/voice.yaml`.

**Result:**

- `voice_config.yaml` became `voice.yaml`. **`setup.py` hadn't installed `config/` at all**, so it now does.
- `TUNE_CONFIG_ENV_VARS` and `resolve_config_path` are gone.
- `VoiceInputNode.__init__` loads from its `config` parameter (`config_path()` raises if it is empty). `main()` creates the node before reading the config.
- `conftest.py` was deleted. New tests: the env vars are ignored, the parameter is required, and the launch passes the installed file.
- dome_voice: 71 passed, plus I01's 3, the same with the variables set or unset.

## TF07.2 — References

**Status**: done (2026-11-19)

**Description**: Update everything that names the variables or `voice_config.yaml`:

- dome_semantic's `tools/power_load_test.sh`, `notes.md`, `power_testing.md` and TF33
- the dome_vision and dome_voice READMEs and literate docs
- dome2's F05/TF05 and `launch_inventory.md`

**Test**: A grep for `DOME_VISION_CONFIG`, `DOME_VOICE_CONFIG`, `VOICE_TUNE_CONFIG` and `voice_config.yaml` finds only history and done files.

**Result:** updated the live references:

- dome_semantic's `power_load_test.sh`, which now uses the installed path from `ros2 pkg prefix`; its 7 tests pass. Also its notes, `power_testing.md` and TF33.
- dome_vision's literate 26.
- dome_voice's `voice.yaml` header, spec, `current.md`, notes and literate 00/01/03/05/X01.
- dome2's inventory note.

**Left as written, as records of past runs:** I01's original failure text, dome_vision's done chore, the evidence lines in TF05 and F05, and `history.md`.

## TF07.3 — The robot: `.bashrc` and `--symlink-install`

**Status**: done (2026-11-19)

**Description**:

- **The user removes** the `DOME_VOICE_CONFIG` and `DOME_VISION_CONFIG` exports from `~/.bashrc`.
- Rebuild with `--symlink-install`. For each package already built as copies, remove its `build/` and `install/` directories first. Start with `dome_vision_ros` and `dome_voice`; the whole workspace is better done in one go.
- Add the `--symlink-install` instruction to dome2's `notes.md` and its build commands.

**Test**: manual, on the robot. The installed `roboflow_oak.yaml` and `voice.yaml` are symlinks (`ls -l`).

**Progress:**

- Rebuilt `dome_vision_ros` and `dome_voice` with `--symlink-install`, after removing their `build/` and `install/`. Both installed configs resolve to the source files, and the installed `roboflow_oak.yaml` now has `nn_threads: 2` (it had gone stale at 1).
- The instruction was added to dome2's `notes.md`, `stack/README.md` and `CLAUDE.md`.
- **The exports weren't in `.bashrc`.** They were in `~/rosutils/ros2_dome_bashrc.bash` (lines 10–11), which `.bashrc` sources through `ros2_robot_bashrc.bash`. Both lines were removed, and `rosutils/SETUP.md` updated. `rosutils` is a shared repo and is uncommitted.
- **tmux still handed them to new panes**, from the server's stored environment. They were cleared with `tmux set-environment -g -u`. Both are recorded in dome2's `notes.md`.

## TF07.4 — Feature test suite and robot check

**Status**: done (2026-11-19)

**Description**: Run the dome_vision, dome_voice and dome2 suites. Then run F07's demo on the robot.

**Test**: The demo in F07.

**Result:**

- **Suites:** dome2 114 passed (9 skipped, 15 xfailed); dome_vision 217 and 95; dome_voice 71, plus I01's 3, the same with the variables set or unset; dome_semantic 160.
- **Robot demo: passed (user report, 2026-11-19).** In a fresh tmux window both variables were empty, and the vision and voice launches worked from the installed configs.
- **Not run separately:** demo step 3, editing a config and relaunching without a rebuild. Instead, `readlink -f` showed both installed configs resolve to the source files.
