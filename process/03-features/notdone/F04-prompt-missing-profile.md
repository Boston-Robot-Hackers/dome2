# F04 — Ask for subsystems when no options and no profile are given

**Priority**: Medium

**Date Created:** 2026-11-16

**Done:** no

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes

**Description**: Running `bl dome2 remote.launch.py` with no `--options` on a
machine where the profile env var (here `remote`) is unset currently crashes
with `ValueError: Profile 'remote': no env var 'remote' found`.

**Decision:** when both are missing, the launcher logs a friendly message —
the profile it looked for, the available subsystems, and an `export` hint —
then asks which subsystems to launch. The answer goes through the usual token
resolution.

- Applies to both `robot.launch.py` and `remote.launch.py` via the shared
  `launch_subsystems()`.
- `token_string()` keeps raising on a missing profile; the launcher checks
  first, so the pure layer's contract is unchanged.
- A set-but-empty profile var still means "launch nothing", as before.

## How to Demo

**Setup**: a shell where neither `remote` nor `DOME_REMOTE_PROFILE` is set.

**Steps**:
1. `bl dome2 remote.launch.py`
2. At the prompt, type `v`.

**Expected output**: a message naming profile `remote`, listing `viz`, and
suggesting `export remote="v"`; then dome_viz launches.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
