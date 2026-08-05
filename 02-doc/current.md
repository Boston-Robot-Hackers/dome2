# Current Status — dome2

## Last session

Date: 2026-08-05

Checkpoint session: reworked `.claude/` process docs (removed
`codereview.md` and `how_to_be.md`, updated `bootstrap.md`, `literate.md`,
`process.md`, `settings.json`, `CLAUDE.md`). Along the way found and fixed
a regression from the earlier nav-subsystem removal (93f2c97) — two tests
in `test/test_launch_profiles.py` still asserted on a `"nav"` token that
no longer resolves. Also cleared pre-existing `ruff check`/`ruff format`
debt in the Python source (`launch/`, `test/`, `setup.py`): missing exec
bits, import ordering, implicit-`Optional`, a self-calling lambda. Added
`ruff.toml` to ignore `LOG015` — the fix (module-level `logging.getLogger`
instead of the root logger) breaks `caplog`-based log assertions in this
environment, so it's a deliberate exception, not unnoticed debt. Also
updated `.claude/commands/checkpoint.md` to require asking the user before
applying any ruff fix, and to state whether it aligns with
`.claude/style_guide.md`.

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

- 2026-08-05: Checkpoint — `.claude/` process rework, fixed nav-removal
  test regression, cleared ruff debt in Python source, `ruff.toml` added
  to record the one deliberate LOG015 exception.
- 2026-08-04: Drafted F02/TF02 — full-stack smoke test (4 stages: drivers,
  control, nav, mission), not started.

Older entries archived in `02-doc/history.md`.
