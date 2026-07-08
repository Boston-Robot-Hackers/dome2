# F01 — Flexible Launch Profiles and Subsystem Selection

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Replace hardcoded all-subsystems launch with a profile + options system. User picks which subsystems to start via a named profile, a short token string, or an interactive prompt. All gating logic moves to `robot.launch.py`; subsystem launch files become unconditional.

## Subsystems

| token prefix | subsystem | launch file |
|---|---|---|
| `d` | drivers | `gendrv.launch.py` |
| `c` | control | `dome_control.launch.py` |
| `vi` | vision | `dome_vision.launch.py` |
| `vo` | voice | `dome_voice.launch.py` |
| `f` | foxglove | `foxglove.launch.py` |
| `n` | nav | `dome_nav.launch.py` (new) |

## CLI Interface

```bash
bl dome2 robot.launch.py                              # default profile ("robot")
bl dome2 robot.launch.py --profile remote             # named profile
bl dome2 robot.launch.py --options "d c vi"           # explicit token list
bl dome2 robot.launch.py --interactive True           # prompted per subsystem
bl dome2 robot.launch.py --profile dev-vision --interactive True  # prompted from profile defaults
DOME_PROFILE=remote bl dome2 robot.launch.py          # env var sets default profile
bl dome2 robot.launch.py --help                       # lists args and defaults
```

## Profiles

| profile | subsystems |
|---|---|
| `robot` | `d c vi vo f` |
| `robot-nav` | `d c vi vo f n` |
| `remote` | `c f` |
| `dev-control` | `c` |
| `dev-vision` | `c vi` |
| `headless` | `d c vi vo` |
| `nav` | `d c n` |

## Token Parsing

Tokens matched by prefix against subsystem names. Ambiguous or unknown tokens produce a warning and are skipped. Example: `"v"` warns (matches `vision` and `voice`); `"vi"` resolves cleanly.

## How to Demo

**Setup**: workspace built and sourced, `bl` available.

**Steps**:
1. `bl dome2 robot.launch.py --help` — verify all args shown with defaults
2. `bl dome2 robot.launch.py --options "c f"` — only control and foxglove start
3. `bl dome2 robot.launch.py --profile dev-control` — same result via profile
4. `bl dome2 robot.launch.py --options "v"` — warning logged, nothing launched for `v`
5. `DOME_PROFILE=remote bl dome2 robot.launch.py` — remote profile from env var
6. `bl dome2 robot.launch.py --profile robot --interactive True` — prompted for each

**Expected output**: Only specified subsystems appear in `ros2 node list`. Warning printed for ambiguous tokens. `--help` shows all options with correct defaults.
