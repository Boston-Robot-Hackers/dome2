#!/usr/bin/env python3
# test_launch_conventions — static checks of stack/launch_conventions.md
# Author: Pito Salas and Claude Code
# Version: 3
# Created: 2026-11-17
# Updated: 2026-11-18
# Open Source Under MIT license
"""Check every DOME launch file against stack/launch_conventions.md.

Static only: files are parsed with `ast` and regexes, never launched. Every
registered package checked out next to dome2 is covered; a missing checkout is
reported as a skip.

Per launch file, one test collects every violation of: the allowed file names,
the header, the `@launch_this` entry function (name, docstring, literal
defaults, plain types, documented arguments), better_launch only, and the
two-level rule. Files the conventions list as known exceptions are skipped.

Files not yet converted are listed in NOT_YET_CONVERTED and run as strict
xfails: each F05 step removes the entries it fixes, and an entry that starts
passing fails until it is removed, so the list can only shrink.

Repo-wide tests check stale launch-file references in launch files, READMEs
and stack/ docs; that every LAUNCH_FILES target exists; that the subsystems
named in stack/README.md exist; and that the inventory matches the files.
"""

import ast
import fnmatch
import re
from pathlib import Path

import pytest
from conftest import load_launch_file

from dome2.stack_registry import load_registry

REPO_DIR = Path(__file__).parent.parent
SRC_DIR = REPO_DIR.parent
STACK_DIR = REPO_DIR / "stack"
NON_PACKAGE_DIRS = {"build", "install", "log"}
REGISTERED = [p.name for p in load_registry(STACK_DIR / "packages.yaml")]
CHECKED_OUT = [name for name in REGISTERED if (SRC_DIR / name).is_dir()]

ALLOWED_NAMES = {"robot.launch.py", "remote.launch.py"}
DOME2_ALLOWED_NAMES = ALLOWED_NAMES | {"drivers.launch.py"}
PLAIN_TYPES = {"str", "bool", "int", "float"}
FORBIDDEN_MODULES = {"launch", "launch_ros"}
PRESENT_VERDICTS = {"keep", "blocked", "f06"}
SELF_REFERENCING_DOCS = {"launch_inventory.md", "launch_conventions.md"}

# (repo, file glob), mirrored in launch_conventions.md's "Known exceptions".
KNOWN_EXCEPTIONS = [
    ("dome_nav", "robot_nav.launch.py"),
    ("dome_nav", "robot_explore.launch.py"),
    ("dome_mission", "mission_explore.launch.py"),
    ("dome_nav", "sim_*.launch.py"),
]

# repo/file or doc path; F05 steps remove entries as they fix them.
NOT_YET_CONVERTED = {
    "dome2/dome_control.launch.py",
    "dome2/dome_vision.launch.py",
    "dome2/dome_voice.launch.py",
    "dome2/foxglove.launch.py",
    "dome2/gendrv.launch.py",
    "dome2/remote.launch.py",
    "dome2/robot.launch.py",
    "dome_control/remote.launch.py",
    "dome_nav/just_explorer.launch.py",
    "dome_nav/nav2_experiment_navigation.launch.py",
    "dome_nav/nav_experiment.launch.py",
    "dome_vision/dome_vision_ros.launch.py",
    "dome_vision/remote.launch.py",
    "dome_vision/robot.launch.py",
    "dome_viz/view.launch.py",
    "dome_voice/remote.launch.py",
    "dome_voice/robot.launch.py",
    "inventory",
}

LAUNCH_NAME_RE = re.compile(r"\b(\w+\.launch\.py)\b")
PACKAGE_REF_RE = re.compile(r"(?:\bbl|ros2 launch)\s+(\w+)\s+(\w+\.launch\.py)")
PACKAGE_XML_NAME_RE = re.compile(r"<name>\s*([\w-]+)\s*</name>")


def package_dirs(root: Path) -> dict[str, Path]:
    """Map each ROS package name under root (depth 0-2) to its directory."""
    found = {}
    for pattern in ("package.xml", "*/package.xml", "*/*/package.xml"):
        for xml_path in root.glob(pattern):
            if NON_PACKAGE_DIRS & set(xml_path.relative_to(root).parts):
                continue
            match = PACKAGE_XML_NAME_RE.search(xml_path.read_text())
            if match:
                found[match.group(1)] = xml_path.parent
    return found


ALL_PACKAGES = package_dirs(SRC_DIR)
REPO_PACKAGES = {name: set(package_dirs(SRC_DIR / name)) for name in CHECKED_OUT}
DOME_PACKAGES = set().union(*REPO_PACKAGES.values())


def repo_launch_files(repo: str) -> list[Path]:
    return sorted(
        path
        for path in (SRC_DIR / repo).glob("**/launch/*.launch.py")
        if not NON_PACKAGE_DIRS & set(path.parts)
    )


ALL_LAUNCH_FILES = [
    (repo, path) for repo in CHECKED_OUT for path in repo_launch_files(repo)
]


def is_known_exception(repo: str, file_name: str) -> bool:
    return any(
        repo == ex_repo and fnmatch.fnmatch(file_name, ex_glob)
        for ex_repo, ex_glob in KNOWN_EXCEPTIONS
    )


def pending(key: str, *values) -> pytest.param:
    marks = []
    if key in NOT_YET_CONVERTED:
        marks = pytest.mark.xfail(strict=True, reason="not yet converted (F05)")
    return pytest.param(*values, id=key, marks=marks)


def header_violations(path: Path, source: str) -> list[str]:
    header = []
    for line in source.splitlines()[1:]:
        if not line.startswith("#"):
            break
        header.append(line)
    problems = []
    if not header or not header[0].startswith(f"# {path.name} — "):
        problems.append("header must start with '# <file name> — <description>'")
    if not any(line.startswith("# Author:") for line in header):
        problems.append("header has no Author line")
    if "# Open Source Under MIT license" not in header:
        problems.append("header has no license line")
    if not any("bl " in line for line in header):
        problems.append("header has no 'bl ...' usage example")
    return problems


def is_launch_this(decorator: ast.expr) -> bool:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    return isinstance(target, ast.Name) and target.id == "launch_this"


def is_literal(node: ast.expr) -> bool:
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        node = node.operand
    return isinstance(node, ast.Constant)


def is_plain_type(annotation: ast.expr | None) -> bool:
    if isinstance(annotation, ast.Name):
        return annotation.id in PLAIN_TYPES
    return (
        isinstance(annotation, ast.Subscript)
        and isinstance(annotation.value, ast.Name)
        and annotation.value.id == "Literal"
    )


def entry_violations(path: Path, tree: ast.Module) -> list[str]:
    entries = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and any(map(is_launch_this, node.decorator_list))
    ]
    if len(entries) != 1:
        return [f"needs exactly one @launch_this function, found {len(entries)}"]
    entry = entries[0]
    problems = []
    expected_name = path.name.removesuffix(".launch.py") + "_launch"
    if entry.name != expected_name:
        problems.append(f"entry function is {entry.name}, expected {expected_name}")
    docstring = ast.get_docstring(entry) or ""
    if not docstring:
        problems.append("entry function has no docstring")
    args = entry.args.args
    defaults = [None] * (len(args) - len(entry.args.defaults)) + entry.args.defaults
    for arg, default in zip(args, defaults, strict=True):
        if default is None or not is_literal(default):
            problems.append(f"argument {arg.arg} needs a literal default")
        if not is_plain_type(arg.annotation):
            problems.append(f"argument {arg.arg} needs a plain type annotation")
        if arg.arg not in docstring:
            problems.append(f"argument {arg.arg} is not documented")
    return problems


def import_violations(tree: ast.Module) -> list[str]:
    problems = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or ""]
        else:
            modules = []
        for module in modules:
            if module.split(".")[0] in FORBIDDEN_MODULES:
                problems.append(f"imports {module}")
        if isinstance(node, ast.Name) and node.id == "LaunchDescription":
            problems.append("builds a LaunchDescription")
    return problems


def called_package(call: ast.Call) -> str | None:
    """Package named by a bl.node / bl.include call, if given as a literal."""
    if not (
        isinstance(call.func, ast.Attribute) and call.func.attr in {"node", "include"}
    ):
        return None
    candidates = call.args[:1] + [
        kw.value for kw in call.keywords if kw.arg == "package"
    ]
    for value in candidates:
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            return value.value
    return None


def two_level_violations(repo: str, tree: ast.Module) -> list[str]:
    if repo == "dome2":
        return []
    foreign = DOME_PACKAGES - REPO_PACKAGES[repo]
    return [
        f"starts or includes DOME package {package}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and (package := called_package(node)) in foreign
    ]


def launch_file_violations(repo: str, path: Path) -> list[str]:
    source = path.read_text()
    tree = ast.parse(source)
    allowed = DOME2_ALLOWED_NAMES if repo == "dome2" else ALLOWED_NAMES
    problems = [] if path.name in allowed else [f"file name {path.name} not allowed"]
    if not ast.get_docstring(tree):
        problems.append("no module docstring")
    problems += header_violations(path, source)
    problems += entry_violations(path, tree)
    problems += import_violations(tree)
    problems += two_level_violations(repo, tree)
    return problems


@pytest.mark.parametrize("package", REGISTERED)
def test_registered_package_checked_out(package):
    if package not in CHECKED_OUT:
        pytest.skip(
            f"{package} is not checked out next to dome2; its checks are skipped"
        )


@pytest.mark.parametrize(
    "repo, path",
    [pending(f"{repo}/{path.name}", repo, path) for repo, path in ALL_LAUNCH_FILES],
)
def test_launch_file_follows_convention(repo, path):
    if is_known_exception(repo, path.name):
        pytest.skip("known exception in launch_conventions.md")
    assert launch_file_violations(repo, path) == []


def test_known_exceptions_are_listed_in_conventions_doc():
    conventions = (STACK_DIR / "launch_conventions.md").read_text()
    for _, file_glob in KNOWN_EXCEPTIONS:
        assert f"`{file_glob}`" in conventions, file_glob


def referencing_docs() -> list[Path]:
    """Launch files, READMEs and stack/ docs that name launch files to run.

    The inventory and the conventions doc are left out: they name deleted and
    planned files on purpose.
    """
    docs = [
        path
        for repo, path in ALL_LAUNCH_FILES
        if not is_known_exception(repo, path.name)
    ]
    docs += [SRC_DIR / repo / "README.md" for repo in CHECKED_OUT]
    docs += [p for p in STACK_DIR.glob("*.md") if p.name not in SELF_REFERENCING_DOCS]
    return [doc for doc in docs if doc.is_file()]


def package_has_launch_file(package: str, file_name: str) -> bool:
    package_dir = ALL_PACKAGES.get(package)
    if package_dir is None:
        installed = list(Path("/opt/ros").glob(f"*/share/{package}"))
        if not installed:
            pytest.skip(f"package {package} not found in src or /opt/ros")
        package_dir = installed[0]
    return any(package_dir.glob(f"**/launch/{file_name}"))


EXISTING_NAMES = {
    path.name
    for path in SRC_DIR.glob("*/**/launch/*.launch.py")
    if not NON_PACKAGE_DIRS & set(path.relative_to(SRC_DIR).parts)
}


def stale_references(doc: Path) -> list[str]:
    text = doc.read_text()
    stale = [
        name for name in set(LAUNCH_NAME_RE.findall(text)) if name not in EXISTING_NAMES
    ]
    for package, file_name in PACKAGE_REF_RE.findall(text):
        if package in DOME_PACKAGES and not package_has_launch_file(package, file_name):
            stale.append(f"{package} {file_name}")
    return sorted(stale)


@pytest.mark.parametrize(
    "doc",
    [pending(str(doc.relative_to(SRC_DIR)), doc) for doc in referencing_docs()],
)
def test_no_stale_launch_file_references(doc):
    assert stale_references(doc) == []


@pytest.mark.parametrize("launcher", ["robot.launch.py", "remote.launch.py"])
def test_launch_files_targets_exist(launcher):
    for package, file_name in load_launch_file(launcher).LAUNCH_FILES.values():
        assert package_has_launch_file(package, file_name), f"{package} {file_name}"


@pytest.mark.parametrize(
    "label, launcher", [("Robot", "robot.launch.py"), ("Remote", "remote.launch.py")]
)
def test_readme_subsystems_exist(label, launcher):
    readme = (STACK_DIR / "README.md").read_text()
    match = re.search(rf"- \*\*{label}\*\*:.*Subsystems: ([\w, ]+)\.", readme)
    assert match, f"no '{label}' subsystem list in stack/README.md"
    named = {name.strip() for name in match.group(1).split(",")}
    assert named <= set(load_launch_file(launcher).LAUNCH_FILES)


def inventory_present_files() -> dict[str, set[str]]:
    """Per repo, the inventory's files whose verdict says they exist."""
    present: dict[str, set[str]] = {}
    repo = None
    for line in (STACK_DIR / "launch_inventory.md").read_text().splitlines():
        if heading := re.match(r"## (\w+) \(\d+ files?", line):
            repo = heading.group(1)
            present[repo] = set()
        elif repo and (
            row := re.match(r"\| `([\w.]+\.launch\.py)` \|.*\| \*\*(\w+)", line)
        ):
            if row.group(2).lower() in PRESENT_VERDICTS:
                present[repo].add(row.group(1))
    return present


@pytest.mark.parametrize("key", [pending("inventory", "inventory")])
def test_inventory_matches_launch_files(key):
    present = inventory_present_files()
    for repo in CHECKED_OUT:
        actual = {path.name for path in repo_launch_files(repo)}
        assert present.get(repo, set()) == actual, repo
