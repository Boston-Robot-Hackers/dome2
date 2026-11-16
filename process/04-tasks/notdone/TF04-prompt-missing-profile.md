# TF04 Ask for subsystems when no options and no profile are given, for Feature F04

**Date Created:** 2026-11-16

## TF04.0 — Pure message builder

**Status**: done

**Description**: Add `missing_profile_message(profile, subsystems)` to
`dome2/launch_options.py`. It returns the text naming the profile, listing
subsystems, and giving an `export <profile>="<first-letter>"` hint.

**Test**: unit tests in `test/test_launch_profiles.py`.

## TF04.1 — Prompt in the launcher

**Status**: done

**Description**: In `dome2/subsystem_launcher.py`, when `options` is empty and
`profile` is not in the environment, log the message and read the token string
with `click.prompt`; otherwise call `token_string()` as before.

**Test**: not unit-testable without a TTY and the better_launch runtime;
covered by the manual demo in F04.

## TF04.2 — Tests

**Status**: done

**Description**: Write the `missing_profile_message` tests, run the suite and
ruff on changed files.

## TF04.3 — Manual check

**Status**: not done

**Description**: Run the F04 demo by hand (`bl dome2 remote.launch.py` with no
profile var set) and confirm the prompt and launch.

**Test**: manual — launching can start nodes on the robot.
