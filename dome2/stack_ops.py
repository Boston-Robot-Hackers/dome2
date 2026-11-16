#!/usr/bin/env python3
# stack_ops — operations across every DOME package in the stack registry
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-16
# Updated: 2026-11-16
# Open Source Under MIT license
"""Command-line tool for operations that span the DOME stack.

Run from the dome2 checkout, normally through the Makefile:

    python3 -m dome2.stack_ops clone --registry stack/packages.yaml --src ..
    python3 -m dome2.stack_ops pull --registry stack/packages.yaml --src ..

Both act on every registered package, whatever its `runs_on`, as a peer of
dome2 under `--src` (the workspace `src/` directory).

- `clone` runs `git clone <repo> <src>/<name>` for each package whose path
  doesn't exist yet. An existing path is left alone, whatever is in it.
- `pull` runs `git pull --ff-only` in each package. A missing package is a
  failure that points to `clone`; `pull` never clones by itself.

One failure does not stop the others. The summary lists every failure and
the exit status is 1 if there was any.
"""

import argparse
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from dome2.stack_registry import StackPackage, load_registry


@dataclass(frozen=True)
class PackageResult:
    name: str
    is_ok: bool
    detail: str


def run_git(name: str, git_args: list[str]) -> PackageResult:
    completed = subprocess.run(
        ["git", *git_args], capture_output=True, text=True, check=False
    )
    is_ok = completed.returncode == 0
    lines = (completed.stdout + completed.stderr).strip().splitlines()
    # On success git's first line says what happened ("Updating a..b",
    # "Already up to date.", "Cloning into ..."); on failure the error is last.
    detail = (lines[0] if is_ok else lines[-1]) if lines else ""
    return PackageResult(name, is_ok, detail)


def pull_package(package: StackPackage, src_dir: Path) -> PackageResult:
    package_dir = src_dir / package.name
    if not package_dir.is_dir():
        return PackageResult(package.name, False, "not checked out; run: make clone")
    return run_git(package.name, ["-C", str(package_dir), "pull", "--ff-only"])


def clone_package(package: StackPackage, src_dir: Path) -> PackageResult:
    package_dir = src_dir / package.name
    if package_dir.exists():
        return PackageResult(package.name, True, "already present")
    return run_git(package.name, ["clone", package.repo, str(package_dir)])


OPERATIONS: dict[str, Callable[[StackPackage, Path], PackageResult]] = {
    "clone": clone_package,
    "pull": pull_package,
}


def summary_lines(results: list[PackageResult], operation: str) -> list[str]:
    """One line per package, then a total line naming any failures."""
    lines = [
        f"{'ok  ' if result.is_ok else 'FAIL'} {result.name}: {result.detail}"
        for result in results
    ]
    failed = [result.name for result in results if not result.is_ok]
    if failed:
        lines.append(
            f"{operation}: {len(failed)} of {len(results)} failed: {', '.join(failed)}"
        )
    else:
        lines.append(f"{operation}: all {len(results)} packages ok")
    return lines


def run_operation(operation: str, registry_path: Path, src_dir: Path) -> int:
    packages = load_registry(registry_path)
    print(f"{operation}: {len(packages)} packages in {src_dir}")
    package_op = OPERATIONS[operation]
    results = [package_op(package, src_dir) for package in packages]
    print("\n".join(summary_lines(results, operation)))
    return 0 if all(result.is_ok for result in results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stack_ops", description=__doc__)
    parser.add_argument("operation", choices=list(OPERATIONS))
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--src", type=Path, required=True, help="workspace src/ dir")
    args = parser.parse_args(argv)
    return run_operation(args.operation, args.registry, args.src.resolve())


if __name__ == "__main__":
    sys.exit(main())
