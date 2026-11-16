#!/usr/bin/env python3
# stack_registry — load and validate the DOME stack's package registry
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-16
# Updated: 2026-11-16
# Open Source Under MIT license
"""The registry (`stack/packages.yaml`) lists every DOME package.

Each entry has a `name`, a git `repo` URL, and `runs_on`, one of `robot`,
`remote` or `both`, recording where the package runs. Cross-package tools act
on every entry regardless of `runs_on`.

The file is validated once, at load time: a missing field, an unknown
`runs_on`, a duplicate name or an empty list raises `RegistryError` naming
the offending entry. After that the `StackPackage` values are trusted.
"""

from dataclasses import dataclass
from pathlib import Path

import yaml

RUNS_ON_VALUES = ("robot", "remote", "both")
REQUIRED_FIELDS = ("name", "repo", "runs_on")


class RegistryError(ValueError):
    """The registry file is malformed."""


@dataclass(frozen=True)
class StackPackage:
    name: str
    repo: str
    runs_on: str


def parse_package(entry: dict) -> StackPackage:
    missing = [field for field in REQUIRED_FIELDS if not entry.get(field)]
    if missing:
        raise RegistryError(f"Registry entry {entry!r} is missing {missing}")
    if entry["runs_on"] not in RUNS_ON_VALUES:
        raise RegistryError(
            f"Package '{entry['name']}': runs_on '{entry['runs_on']}' "
            f"is not one of {RUNS_ON_VALUES}"
        )
    return StackPackage(entry["name"], entry["repo"], entry["runs_on"])


def parse_registry(registry_doc: dict) -> list[StackPackage]:
    """Validate a parsed registry document and return its packages in order."""
    entries = registry_doc.get("packages") if registry_doc else None
    if not entries:
        raise RegistryError("Registry has no 'packages' entries")
    packages = [parse_package(entry) for entry in entries]
    names = [package.name for package in packages]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise RegistryError(f"Registry lists these packages twice: {duplicates}")
    return packages


def load_registry(registry_path: Path) -> list[StackPackage]:
    return parse_registry(yaml.safe_load(registry_path.read_text()))

