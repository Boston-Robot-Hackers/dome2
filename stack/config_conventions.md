# DOME Config File Conventions

The rules for where a DOME package's configuration lives, what it's called,
and how a node finds it. They were decided on 2026-11-19, and F07 brings the
packages into line.

See [`launch_conventions.md`](launch_conventions.md) for the companion rules
on launch files.

## Where it lives

- **A package's configuration is in its own `config/` directory**, committed
  to git. `setup.py` installs it to `share/<pkg>/config/`.
- **Runtime state goes in `~/.dome/`**, never in `config/`. That covers
  anything a program writes, plus machine-local data: maps, telemetry logs,
  history files.

## What it's called

- **`<subject>.yaml`**, named after the node or the thing it configures:
  `spin_survey.yaml`, `telemetry.yaml`, `semantic_map.yaml`,
  `class_profiles.yaml`, `ekf.yaml`.
- Lower case, words joined with `_`. No `-config`, `_config` or `_params`
  suffix, since the `config/` directory already says that.
- **Files for an outside package keep that package's style.** For example,
  `dome_nav`'s `nav2_params_*.yaml` follow Nav2.

## How a node finds it

**The launch file passes the installed copy.** No environment variable is
involved.

```python
bl.find("dome_semantic", "semantic_map.yaml")
```

- A ROS params file goes in through `param_files=`.
- An application YAML's path goes in as a node parameter, conventionally
  `config`.
- A launch argument may let you pick a different file for one run, e.g.
  `--config <path>`. Its default is the literal `""`, meaning "the installed
  file", per the launch conventions.
- **A node does not look up a config path from the environment**, and does
  not fall back to the defaults when the file it was given is missing. It
  raises.

**Why no environment variables:** they are a second, invisible way to choose
a file. They depend on the shell and on the source checkout's location, and
they made tests load the robot's config by accident (dome_voice I01).

## Editing without a rebuild

The installed copy is what runs. So that editing `config/` takes effect
without rebuilding, **build the workspace with `--symlink-install`**:

```
cd ~/ros2_ws && colcon build --symlink-install
```

The installed config files are then symlinks into the source tree.

- **Without it, the installed copy goes stale.** On 2026-11-19,
  `roboflow_oak.yaml`'s installed copy still said `nn_threads: 1`, an hour
  after the source said 2.
- Switching an existing package to `--symlink-install` needs that package's
  `build/` and `install/` directories removed first. colcon won't replace
  copied files with links.

## Two formats

| Format | Read by | Use it for |
|---|---|---|
| **ROS params file** (`<node>: ros__parameters:`) | ROS, via `param_files=` | a node's ROS parameters, especially ones changed live with `ros2 param set` |
| **Application YAML** | a pydantic model in the package | structured config: nested sections, lists, cross-field rules |

An application YAML follows these rules:

- **Defaults are written once**, in the pydantic model.
- **The file overrides only the keys it names.**
- **Unknown keys are an error** (`extra="forbid"`), so a misspelling can't
  be silently ignored.

dome_vision's `AppConfig` and dome_voice's `VoiceConfigFile` follow all
three. dome_semantic's `WorldTrackerConfig` and dome_control's
`SpinSurveyConfig` use pydantic but don't forbid unknown keys yet.

## Where tuned values go

Values tuned for this robot, its microphone, its camera or its room are
**deployment data**. They go in the YAML, not in code. The code's defaults
are generic and safe.
