# Current Status — dome2

## Last session

Date: 2026-08-04

Session on the Pi to plan a step-by-step bring-up/smoke test of the full
robot stack (drivers → control → dome_nav SLAM/Nav2/explorer →
dome_mission's `mission_node`). Drafted F02 + TF02 but deliberately did not
start implementation — see Blocked below. Robot is being rebooted at end of
session.

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

1. Land `dome_control`'s F19 (dome_mission `/intent` integration) —
   tracked in that package, not here.
2. Resume F02 (`03-features/notdone/F02-full-stack-smoke-test.md`) — T01
   (stage spec) and T02 (health-check logic) are pure and could start
   independently of F19 if useful; T03/T04 (actual orchestration through
   the control + mission stages) should wait for F19.

## Recent completions

- 2026-08-04: Drafted F02/TF02 — full-stack smoke test (4 stages: drivers,
  control, nav, mission), not started.
- 2026-07-08: Checkpoint — tests pass, literate docs updated, stale mode-gate docs removed
- Bootstrap scaffold created (LICENSE, spec.md, current.md, notes.md, process folders)
- Prior session: skip gated subsystem launches cleanly
- Prior session: codereview v3.1, /start command, CLAUDE.md, how_to_be wired
