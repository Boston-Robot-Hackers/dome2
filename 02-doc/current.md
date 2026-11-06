# Current Status — dome2

## Last session

Date: 2026-11-05

Checkpoint of a chore: `robot.launch.py` gained **`battery`** (battery
telemetry, from `dome_telemetry`) and **`yellow`** (Yellow Pad joystick
teleop) subsystems, so each can be turned on independently.
`gendrv.launch.py` no longer includes the telemetry launch, so `drivers`
alone doesn't start it. The base robot for power and semantic tests is now
`bl dome2 robot.launch.py --options "d b"`.

## In progress

Nothing in progress. F02 (see Next up) is drafted and accepted but not
started.

## Blocked / needs decision

**F02 is parked pending `dome_control`'s F19.** Investigating the smoke
test surfaced that `dome_control`'s `behavior_manager` and `dome_mission`'s
`mission_node` both subscribe to `/intent` with no coordination (dead
`intent.explore` CLI command, and `stop` doesn't cancel an active
`dome_mission` goal). Running F02's stage 2 (control) next to stage 4
(mission) would smoke-test through an unresolved integration gap, so
`dome_control`'s F19 (`03-features/notdone/F19-dome-mission-intent-
integration.md` in that package) needs to land first.

## Next up

0. **Move the power load test here from `dome_semantic`.** It covers the
   whole robot. Files: `tools/power_load_test.sh`, `tools/power_summary.awk`,
   `test/test_power_load_test.py`, `process/02-doc/power_testing.md`. See
   `dome_semantic`'s `current.md` for the full list of references to
   update. Probably a feature here. It overlaps with F02 (a staged run
   through the stack), so consider merging the two.
1. Land `dome_control`'s F19 (dome_mission `/intent` integration) —
   tracked in that package, not here.
2. Resume F02 (`03-features/notdone/F02-full-stack-smoke-test.md`) — T01
   (stage spec) and T02 (health-check logic) are pure and could start
   independently of F19 if useful; T03/T04 (actual orchestration through
   the control + mission stages) should wait for F19.

## Recent completions

- 2026-11-05: Chore: `battery` and `yellow` subsystems; telemetry taken
  out of `drivers`. `ruff format --check` flags 4 older files; they were
  left alone, since this repo's checkpoint asks before any ruff fix.
- 2026-08-05: Checkpoint — `.claude/` process rework, fixed nav-removal
  test regression, cleared ruff debt in Python source, `ruff.toml` added
  to record the one deliberate LOG015 exception.
- 2026-08-04: Drafted F02/TF02 — full-stack smoke test (4 stages: drivers,
  control, nav, mission), not started.

Older entries archived in `02-doc/history.md`.
