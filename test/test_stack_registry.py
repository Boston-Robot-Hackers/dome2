#!/usr/bin/env python3
# test_stack_registry.py — tests for the stack registry and its doc tables
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-16
# Updated: 2026-11-24
# Open Source Under MIT license

from pathlib import Path

import pytest

from dome2.stack_registry import (
    RegistryError,
    load_registry,
    parse_registry,
)

REPO_DIR = Path(__file__).parent.parent
REGISTRY_PATH = REPO_DIR / "stack" / "packages.yaml"


def entry(name="dome_x", repo="git@example:dome_x.git", runs_on="robot"):
    return {"name": name, "repo": repo, "runs_on": runs_on}


@pytest.fixture(scope="module")
def real_packages():
    return load_registry(REGISTRY_PATH)


class TestRealRegistry:
    def test_loads_all_packages(self, real_packages):
        assert len(real_packages) == 14
        assert real_packages[0].name == "dome2"

    def test_runs_on_values(self, real_packages):
        runs_on = {p.name: p.runs_on for p in real_packages}
        assert runs_on["dome2"] == "both"
        assert runs_on["dome_viz"] == "remote"
        assert runs_on["dome_nav"] == "robot"

    def test_spec_table_lists_every_package(self, real_packages):
        spec_text = (REPO_DIR / "process" / "02-doc" / "spec.md").read_text()
        for package in real_packages:
            assert f"| {package.name} | {package.runs_on} |" in spec_text

    def test_stack_readme_mentions_every_package(self, real_packages):
        readme_text = (REPO_DIR / "stack" / "README.md").read_text()
        for package in real_packages:
            assert f"`{package.name}`" in readme_text, package.name


class TestParseRegistry:
    def test_valid_entries_keep_order(self):
        packages = parse_registry({"packages": [entry("b"), entry("a")]})
        assert [p.name for p in packages] == ["b", "a"]

    @pytest.mark.parametrize("registry_doc", [None, {}, {"packages": []}])
    def test_empty_registry_raises(self, registry_doc):
        with pytest.raises(RegistryError):
            parse_registry(registry_doc)

    @pytest.mark.parametrize("field", ["name", "repo", "runs_on"])
    def test_missing_field_raises(self, field):
        broken = entry()
        del broken[field]
        with pytest.raises(RegistryError, match=field):
            parse_registry({"packages": [broken]})

    def test_bad_runs_on_names_the_package(self):
        with pytest.raises(RegistryError, match="dome_x"):
            parse_registry({"packages": [entry(runs_on="laptop")]})

    def test_duplicate_name_raises(self):
        with pytest.raises(RegistryError, match="dome_x"):
            parse_registry({"packages": [entry(), entry()]})

