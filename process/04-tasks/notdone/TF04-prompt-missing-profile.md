# TF04 List the subsystems and exit when no options and no profile are given, for Feature F04

**Date Created:** 2026-11-16

## TF04.0 — Pure message builder

**Status**: done

**Description**: Add `missing_profile_message(profile, subsystems)` to
`dome2/launch_options.py`. It returns the text naming the profile, listing
subsystems, and giving an `export <profile>="<first-letter>"` hint.

**Test**: unit tests in `test/test_launch_profiles.py`.

## TF04.1 — Exit from the launcher

**Status**: done

**Description**: In `dome2/subsystem_launcher.py`, when `options` is empty and
`profile` is not in the environment, log the message as an error and
`sys.exit(1)`. Otherwise call `token_string()` as before.

The first version prompted with `click.prompt` instead. On the VM the prompt
never appeared under better_launch's UI, so it was changed on 2026-11-17.

**Test**: `TestLaunchSubsystemsWithoutProfile` in
`test/test_launch_profiles.py`. It checks for exit code 1, that
`BetterLaunch` is never constructed (with and without `is_interactive`), and
that the subsystems are logged.

## TF04.2 — Tests

**Status**: done

**Description**: Write the `missing_profile_message` tests, run the suite and
ruff on changed files.

## TF04.3 — Manual check

**Status**: not done

**Description**: Run the F04 demo by hand (`bl dome2 remote.launch.py` with no
profile var set). Confirm the message is shown and the launcher exits without
starting anything.

First run, 2026-11-17 on the VM, with the old prompt: the message showed, then
the prompt hung. That led to the change in TF04.1.

**Test**: manual — launching can start nodes on the robot.
