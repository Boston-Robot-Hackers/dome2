# F08 — Status and commit-push across every DOME repo

**Priority**: Medium

**Date Created:** 2026-11-19

**Done:** yes

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes

**Description**: Two new Makefile targets that act on every package in `stack/packages.yaml`, next to the existing `clone` and `pull`. Work now spans many repos at once (this session's checkpoint touched eight), and checking and committing them one by one is slow and easy to get wrong.

## Scope

- **`make status-repos`** prints `CLEAN  <name>` or `DIRTY  <name>` for every package in `stack/packages.yaml`, after a `git fetch`. DIRTY means uncommitted files, commits to push or commits to pull. A repo it can't check prints `FAIL   <name>: <why>`, and the exit status is then nonzero.
- It is a new `status` operation in `dome2.stack_ops`, next to `clone` and `pull`.

## Decisions (2026-11-19)

- **`status-repos` fetches first**, so "to pull" is current.
- **Output is one line per repo**, no header or summary (the user's format).
- **`commit-push-repos` was built, then removed at the user's request** before it was ever run. Committing stays with `/checkpoint` or by hand. Its `git add -A` would also have committed files a repo's `.gitignore` misses, as the first `status-repos` run showed (dome_mission's `__pycache__/`, dome_control's PDF deletions).

## How to Demo

**Setup**: some DOME repos with uncommitted changes, some clean.

**Steps**:
1. `make status-repos`

**Expected output**: one `CLEAN` or `DIRTY` line per registered repo, matching `git status` in each.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
