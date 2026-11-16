#!/usr/bin/env python3
# launch_options — pure token and profile resolution shared by dome2's launchers
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-16
# Updated: 2026-11-16
# Open Source Under MIT license
"""Turns a launcher's `--profile` / `--options` into a list of subsystems.

`--options` is a space-separated string of subsystem-name prefixes ("d c vi").
Each token must match exactly one subsystem; an unknown or ambiguous token is
logged as a warning and skipped. With no `--options`, the profile names an
environment variable whose value is the token string; a missing variable
raises. No ROS imports, so both `robot.launch.py` and `remote.launch.py` share
it and it tests without a ROS runtime.
"""

import logging
from collections.abc import Mapping


def resolve_tokens(options_str: str, subsystems: list[str]) -> list[str]:
    resolved = []
    for token in options_str.split():
        matches = [s for s in subsystems if s.startswith(token.lower())]
        if len(matches) == 1:
            resolved.append(matches[0])
        elif not matches:
            logging.warning(f"Launch option '{token}' matches no subsystem, skipping")
        else:
            logging.warning(
                f"Launch option '{token}' is ambiguous: matches {matches}, skipping"
            )
    return resolved


def missing_profile_message(profile: str, subsystems: list[str]) -> str:
    """Explain that neither `--options` nor the profile env var was given."""
    return (
        f"No --options given and no env var '{profile}' is set.\n"
        f"Available subsystems: {', '.join(subsystems)}.\n"
        f'To skip this question next time: export {profile}="{subsystems[0][0]}"'
    )


def token_string(profile: str, options: str, environ: Mapping[str, str]) -> str:
    """Return `options` if given, else the value of the env var named `profile`."""
    if options:
        return options
    token_str = environ.get(profile)
    if token_str is None:
        raise ValueError(f"Profile '{profile}': no env var '{profile}' found")
    return token_str
