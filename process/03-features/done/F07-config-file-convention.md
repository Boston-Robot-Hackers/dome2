# F07 — Config files follow one convention; no config-path env vars

**Priority**: Medium

**Date Created:** 2026-11-19

**Done:** yes

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes

## Description

`stack/config_conventions.md` (written 2026-11-19) sets the rules:

- config is in `<pkg>/config/<subject>.yaml`
- the launch file passes the installed copy, found with `bl.find`
- no node looks up a config path from the environment
- the workspace is built with `--symlink-install`

This feature brings the two packages that break it into line, **dome_vision and dome_voice**. **The user decided to remove the config-path environment variables** as unneeded complexity.

### What changes

- **dome_vision:**
  - `DOME_VISION_CONFIG` goes.
  - `robot.launch.py`'s `--config` defaults to the installed `roboflow_oak.yaml`.
  - The node raises if `config` is empty.
- **dome_voice:**
  - `DOME_VOICE_CONFIG`, `CONTROL_VOICE_TUNE_CONFIG` and `VOICE_TUNE_CONFIG` go.
  - `voice_input` gets a `config` ROS parameter from `robot.launch.py`, the installed file.
  - The ROS-free runtime takes a path, or uses its defaults.
  - `voice_config.yaml` becomes `voice.yaml`, per the naming rule.
- **The robot's `.bashrc`** drops the two exports. The user does this.
- **The workspace is rebuilt with `--symlink-install`**, so editing `config/` takes effect without a rebuild.
- **References are updated**: dome_semantic's `power_load_test.sh`, notes, `power_testing.md` and TF33, plus the READMEs and literate docs.

### Out of scope

- **Renaming `roboflow_oak.yaml`.** The name describes the model and camera, not the node, but it is referenced widely. Decide separately.
- **Other environment variables.** `DOME_PIPER_BIN`, `DOME_PIPER_MODEL_PATH`, `SPEECH_*` and `PIPER_LENGTH_SCALE` set `speech_output`'s settings, not a config path. `DOME_SPIN_SURVEY_MAP` names a data file, and `DOME_CAMERA` selects a camera. Each is its own decision.
- **Adding `extra="forbid"`** to dome_semantic's and dome_control's pydantic models.
- **dome_control's `~/.dome/config/control.yaml`.** It is parked by the user (dome2 `current.md`).

## How to Demo

**Setup**: robot, with the two exports removed from `.bashrc` and a new shell.

**Steps**:

1. `echo $DOME_VISION_CONFIG $DOME_VOICE_CONFIG`. Both are empty.
2. `bl dome_vision_ros robot.launch.py`. The vision node reaches `active`, and its log names the installed `roboflow_oak.yaml`.
3. Edit a value in `dome_vision_ros/config/roboflow_oak.yaml` and relaunch, without rebuilding. The node uses the new value.
4. `bl dome_voice robot.launch.py`. `voice_input` logs the installed `voice.yaml` as its source. It still stops on the missing `openwakeword`; that is separate.

**Expected output**: as above, with no config-path variable anywhere in the source (`grep` finds none).
