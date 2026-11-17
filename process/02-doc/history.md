# History — dome2

Archived entries from `current.md`'s Recent completions, oldest work moved
here to keep `current.md` focused on what's recent and relevant.

- 2026-11-17: F05 drafted (consistent launch files; first drafted as F04,
  renumbered after the remote's F04). Robot experiments E1–E3 run; results
  are in TF05.1. Convention rule added: all DOME launch files use
  better_launch. Stack-wide `ExternalShutdownException` shutdown fix made in
  7 repos (uncommitted). SLAM params and activation findings added to
  `dome_nav` I13.
- 2026-11-16: F04 built — launchers ask for subsystems instead of raising
  when neither `--options` nor the profile env var is set. Manual TF04.3
  pending. Also `chmod +x` on `dome2/launch_options.py` and
  `dome2/subsystem_launcher.py` (ruff EXE001).
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
