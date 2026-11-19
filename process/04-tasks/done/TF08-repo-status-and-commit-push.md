# TF08 Status and commit-push across every DOME repo, for Feature F08

**Date Created:** 2026-11-19

## TF08.0 — `status` operation in `stack_ops`

**Status**: done

**Description**: Add a `status` operation. Per package: `git fetch`, then `git status --porcelain` for the uncommitted count and `git rev-list --left-right --count @{u}...HEAD` for behind/ahead. A missing package fails and points to `make clone`, as `pull` does. A repo with no upstream branch is reported, not guessed at.

**Test**: unit tests with git mocked, like `test_stack_ops.py`: clean, dirty, ahead, behind, no upstream, fetch failure, missing package.

## TF08.1 — `commit-push` operation in `stack_ops`

**Status**: done, then removed (2026-11-19). The user dropped `commit-push-repos` before it was run. The operation, its 9 tests and its Makefile test were deleted with it.

## TF08.2 — Makefile targets and docs

**Status**: done

**Description**: Add `status-repos` (and, until it was dropped, `commit-push-repos`) to the Makefile, each with a `## description` so `make help` lists them. `commit-push-repos` checks `MSG` is set. Document both in `stack/README.md` next to `clone` and `pull`, and in `README.md`.

**Test**: a test that `make help` lists both targets, and that `make commit-push-repos` without `MSG` exits nonzero before running any git command (`make -n` style check, or calling `main` with no message).

## TF08.3 — Full test pass and a manual run

**Status**: done. Suite and ruff pass; `status-repos` checked on the Pi.

**Description**: Run dome2's whole suite and ruff on the changed files. Then the user runs `make status-repos` on the Pi and checks it against `git status` in two or three repos. `commit-push-repos` is first tried on a real change only when the user chooses to.

**Test**: the suite itself; the manual run is recorded here.

**Results (2026-11-19):**

- dome2: 127 passed, 9 skipped. ruff clean on the changed files (`stack_ops.py` and `test_stack_ops.py` were made executable for EXE001).
- `README.md` got a short "Stack commands" section; `stack/README.md` documents both targets.
- **`make status-repos` on the Pi:** all 12 repos reported. dome2 23 uncommitted and dome_control 2 uncommitted, matching `git status --porcelain`; dome2 0/0 against its upstream, matching `git rev-list`.
- **It showed a real `git add -A` hazard:** dome_mission's 2 "uncommitted" are untracked `__pycache__/` directories its `.gitignore` misses, and dome_control's 2 are the PDF deletions not made in this session. `commit-push-repos` would commit both.
- **Output format changed at the user's request:** one `CLEAN  <name>` or `DIRTY  <name>` line per repo, `FAIL   <name>: <why>` on a failure, no header or summary. DIRTY covers uncommitted, to push and to pull. dome2: 130 passed, 9 skipped.
- `MSG` is passed inside double quotes, so a message containing `"` breaks the shell command.
- **`commit-push-repos` removed** at the user's request. dome2: 120 passed, 9 skipped.
