# History — dome2

Archived entries from `current.md`'s Recent completions, oldest work moved
here to keep `current.md` focused on what's recent and relevant.

- 2026-11-16: F03 closed — dome2 is the stack hub: `stack/packages.yaml`
  (12 packages), `make clone` / `make pull`, `remote.launch.py` (viz),
  shared launcher modules, `stack/README.md`. Verified on robot and VM.
- 2026-11-16: `.claude/` synced with the `j3` kit; process folders moved
  under `process/`; task steps renumbered `TFNN.N`; header-stamping
  pre-commit hook and Makefile added.
- 2026-11-05: Chore: `battery` and `yellow` subsystems in
  `robot.launch.py`; telemetry taken out of `drivers`. Base robot for power
  and semantic tests is `bl dome2 robot.launch.py --options "d b"`.
  `ruff format --check` flags 4 older files, left alone.
- 2026-08-05: Checkpoint — `.claude/` process rework, fixed nav-removal
  test regression, cleared ruff debt, `ruff.toml` added for the one
  deliberate LOG015 exception.
- 2026-08-04: Drafted F02/TF02 — full-stack smoke test (4 stages: drivers,
  control, nav, mission), not started.
- 2026-07-08: Checkpoint — tests pass, literate docs updated, stale
  mode-gate docs removed.
- Bootstrap scaffold created (LICENSE, spec.md, current.md, notes.md,
  process folders).
- Prior session: skip gated subsystem launches cleanly.
- Prior session: codereview v3.1, /start command, CLAUDE.md, how_to_be
  wired.
