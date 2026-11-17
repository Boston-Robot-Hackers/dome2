# F04 — List the subsystems and exit when no options and no profile are given

**Priority**: Medium

**Date Created:** 2026-11-16

**Done:** yes

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes

**Description**: Running `bl dome2 remote.launch.py` with no `--options` on a
machine where the profile env var (here `remote`) is unset currently crashes
with `ValueError: Profile 'remote': no env var 'remote' found`.

**Decision:** when both are missing, the launcher logs a friendly error,
then **shuts down without launching anything**. The error names the
profile it looked for, lists the available subsystems, and suggests either
`--options "<letter>"` or `export <profile>="<letter>"`.

- **It doesn't ask.** The first version prompted for tokens with
  `click.prompt`. On the VM the prompt never appeared: better_launch's UI
  (`ui=True`) owns the terminal and printed `WARNING: your terminal doesn't
  support cursor position requests (CPR)`, then hung. **Decided 2026-11-17:
  print the options and exit.**
- **Not `sys.exit(1)`.** That was tried next. Under the UI, the launch
  function runs in a worker thread, so the exit ended only that thread. The
  UI stayed up and asked "Shutdown nodes and quit?". The launcher now calls
  `shutdown()` on the `BetterLaunch` instance, which makes the UI quit by
  itself. **The exit status is 0, not 1.**
- It stops with `--is_interactive` too, for the same reason.
- Applies to both `robot.launch.py` and `remote.launch.py` via the shared
  `launch_subsystems()`.
- `token_string()` keeps raising on a missing profile. The launcher checks
  first, so the pure layer's contract is unchanged.
- A set-but-empty profile var still means "launch nothing", as before.

## How to Demo

**Setup**: a shell where neither `remote` nor `DOME_REMOTE_PROFILE` is set.

**Steps**:
1. `bl dome2 remote.launch.py`

**Expected output**: an error naming profile `remote`, listing `viz`, and
suggesting `--options "v"` or `export remote="v"`. The launcher then
returns to the shell by itself, with no nodes started and no quit question.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
