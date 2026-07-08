# TF01 — Flexible Launch Profiles and Subsystem Selection

## T01 — Add dome_nav.launch.py wrapper
**Status**: done
**Description**: Create `launch/dome_nav.launch.py` in dome2 that unconditionally includes `dome_nav/robot.launch.py`. Follow same pattern as existing subsystem wrappers.
**Test**: File exists and `bl.include` target resolves without error (import check).

## T02 — Strip env var gating from subsystem launch files
**Status**: done
**Description**: Remove `DOME_MODE` and `DOME_CAMERA` env var reads and early-return guards from `dome_control.launch.py`, `dome_vision.launch.py`, `dome_voice.launch.py`, `gendrv.launch.py`. Each file becomes an unconditional include of its subsystem launch file.
**Test**: Each stripped file imports and executes without referencing `os.environ` for mode/camera (grep check).

## T03 — Implement token parser
**Status**: done
**Description**: Write `resolve_tokens(options_str) -> list[str]` in `robot.launch.py`. Splits string on whitespace, matches each token as prefix of subsystem name. Warns via `logging.warning` and skips on zero or multiple matches. Returns list of resolved subsystem names.
**Test**: Unit tests covering: exact match, prefix match, ambiguous token (warning + skip), unknown token (warning + skip), empty string returns empty list.

## T04 — Implement profile table and launch arg wiring
**Status**: done
**Description**: Add `PROFILES` dict and `SUBSYSTEMS` list to `robot.launch.py`. Add `_default_profile = os.environ.get("DOME_PROFILE", "robot")`. Update `@launch_this(ui=True)` function signature with `profile: str = _default_profile` and `options: str = None` and `interactive: bool = False`. Resolve active token list: `options` wins over profile lookup.
**Test**: Manual `--help` shows all three args with correct defaults.

## T05 — Implement conditional includes
**Status**: done
**Description**: Replace unconditional `bl.include` calls in `robot.launch.py` with conditional includes driven by resolved subsystem list from T03/T04. Map subsystem names to their launch files.
**Test**: `--options "c f"` starts only control and foxglove nodes (verified via `ros2 node list` — manual test, note hardware dependency).

## T06 — Implement interactive mode
**Status**: done
**Description**: When `interactive=True`, after resolving cfg from profile/options, loop over all subsystems and call `click.confirm(f"Launch {name}?", default=<resolved bool>)` to let user override each.
**Test**: Not unit-testable (interactive stdin). Manual test: `--interactive True` prompts for each subsystem and respects y/n input.

## T07 — Write unit tests
**Status**: done
**Description**: Write `test/test_launch_profiles.py` covering: `resolve_tokens` (T03 cases), profile lookup returns correct subsystem set, unknown profile raises or warns, env var default respected. Run with plain `pytest`.
**Test**: `pytest test/test_launch_profiles.py` passes with no skips.

## T08 — Update feature file
**Status**: done
**Description**: Set `Tasks File Created: yes` in F01. After all tasks done, set `Done: yes`, `Tests Written: yes`, `Test Passing: yes` and move files to done folders.
**Test**: N/A — process bookkeeping.
