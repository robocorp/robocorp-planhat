import re
import sys
import tempfile
import textwrap
from contextlib import contextmanager
from itertools import chain
from pathlib import Path
from typing import Iterator, List, Optional

from invoke import task

ROOT = Path(__file__).parent
REPOSITORY_URL = "https://github.com/robocorp/robocorp-planhat/tree/master/"
PACKAGE_NAME = "robocorp-planhat"
IMPORT_NAME = "planhat"
TAG_PREFIX = PACKAGE_NAME.replace(".", "-")
DIST = ROOT / "dist"


def get_tag(tag_prefix: str) -> str:
    """
    Args:
        tag_prefix: The tag prefix to match (i.e.: "robocorp-tasks")
    """
    import subprocess

    # i.e.: Gets the last tagged version
    cmd = f"git describe --tags --abbrev=0 --match {tag_prefix}-[0-9]*".split()
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = popen.communicate()

    # Something as: b'robocorp-tasks-0.0.1'
    return stdout.decode("utf-8").strip()


def get_all_tags(tag_prefix: str) -> List[str]:
    import subprocess

    cmd = "git tag".split()
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = popen.communicate()

    found = stdout.decode("utf-8").strip()
    return [x for x in found.splitlines() if x.startswith(tag_prefix)]


def to_identifier(value: str) -> str:
    value = re.sub(r"[^\w\s_]", "", value.lower())
    value = re.sub(r"[_\s]+", "_", value).strip("_")
    return value


def run(ctx, *cmd, **options):
    import os

    options.setdefault("pty", sys.platform != "win32")
    options.setdefault("echo", True)

    os.chdir(ROOT)
    args = " ".join(str(c) for c in cmd)
    return ctx.run(args, **options)


def poetry(ctx, *cmd):
    return run(ctx, "poetry", *cmd)


@task
def install(ctx):
    """Install dependencies"""
    poetry(ctx, "install")


@task
def lint(ctx, strict: bool = False):
    """Run static analysis and formatting checks"""
    poetry(ctx, f"run ruff src tests")
    poetry(ctx, f"run black --check src tests")
    poetry(ctx, f"run isort --check src tests")
    if strict:
        poetry(ctx, f"run pylint --rcfile {ROOT / '.pylintrc'} src")


@task
def typecheck(ctx):
    """Type check code"""
    poetry(
        ctx,
        "run mypy",
        "--follow-imports=silent",
        "--show-column-numbers",
        "--namespace-packages",
        "--explicit-package-bases",
        f"-p {IMPORT_NAME}",
    )


@task
def pretty(ctx):
    """Auto-format code and sort imports"""
    poetry(ctx, f"run black src tests")
    poetry(ctx, f"run isort src tests")


@task
def test(ctx):
    """Run unittests"""
    poetry(ctx, f"run pytest -rfE -vv")


@task
def doctest(ctx):
    """Statically verify documentation examples."""
    pattern = re.compile(r"^\s*```python([\s\S]*?)\s*```", re.MULTILINE)
    files = [
        (ROOT / "src").rglob("*.py"),
        (ROOT / "docs" / "guides").rglob("*.md"),
    ]

    output = ""
    for path in chain(*files):
        dirname = to_identifier(path.parent.name)
        filename = to_identifier(path.name)

        content = path.read_text()
        matches = re.findall(pattern, content)
        if not matches:
            continue

        print(f"Found examples in: {path}")
        output += f"\n# {path.name}\n"
        for index, match in enumerate(matches):
            code = textwrap.indent(textwrap.dedent(match), "    ")
            output += f"\ndef codeblock_{dirname}_{filename}_{index}() -> None:"
            output += code
            output += "\n"

    if not output:
        print("No example blocks found")
        return

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        print(f"Validating project: {ROOT.name}")
        for lineno, line in enumerate(output.splitlines(), 1):
            print(f"{lineno:3}: {line}")

        tmp.write(output)
        tmp.close()  # Fix for Windows
        poetry(ctx, f"run mypy --strict {tmp.name}")


@task(lint, typecheck, test)
def check_all(ctx):
    """Run all checks"""
    pass


@task
def build(ctx):
    """Build distributable .tar.gz and .wheel files"""
    poetry(ctx, "build")


@task
def publish(ctx):
    """Publish to PyPI"""
    poetry(ctx, "publish")


@task
def docs(ctx):
    """Build API documentation"""
    output_path = ROOT / "docs" / "api"
    output_path.mkdir(exist_ok=True)
    for path in output_path.iterdir():
        path.unlink()

    poetry(
        ctx,
        "run lazydocs",
        "--validate",
        "--no-watermark",
        "--remove-package-prefix",
        f"--src-base-url {REPOSITORY_URL}",
        "--overview-file README.md",
        f"--output-path {output_path}",
        IMPORT_NAME,
    )


@task
def make_release(ctx):
    """Create a release tag"""
    import importlib

    import semver

    result = run(ctx, "git rev-parse --abbrev-ref HEAD", hide=True)
    branch = result.stdout.strip()
    if branch != "main":
        sys.stderr.write(f"Not on main branch: {branch}\n")
        sys.exit(1)

    current_version = importlib.import_module(IMPORT_NAME).__version__

    previous_tag = get_tag(TAG_PREFIX)
    previous_version = previous_tag.split("-")[-1]

    if not previous_version:
        print(f"No previous release for {PACKAGE_NAME}")
    elif semver.compare(current_version, previous_version) <= 0:
        sys.stderr.write(
            f"Current version older/same than previous: {current_version} <= {previous_version}\n"
        )
        sys.exit(1)

    current_tag = f"{TAG_PREFIX}-{current_version}"
    run(
        ctx,
        "git tag",
        "-a",
        current_tag,
        "-m",
        f'"Release {current_version} for {PACKAGE_NAME}"',
        echo=True,
    )

    print(f"Trigger the release with: git push origin {current_tag}")


@task
def check_tag_version(ctx):
    """
    Checks if the current tag matches the latest version (exits with 1 if it
    does not match and with 0 if it does match).
    """
    import importlib

    mod = importlib.import_module(IMPORT_NAME)

    tag = get_tag(TAG_PREFIX)
    version = tag[tag.rfind("-") + 1 :]

    if mod.__version__ == version:
        sys.stderr.write(f"Version matches ({version}) (exit(0))\n")
        sys.exit(0)
    else:
        sys.stderr.write(
            f"Version does not match ({TAG_PREFIX}: {mod.__version__} != repo tag: {version}).\nTags:{get_all_tags(TAG_PREFIX)}\n(exit(1))\n"
        )
        sys.exit(1)


@task
def set_version(ctx, version):
    """Sets a new version for the project in all the needed files"""
    import re
    from pathlib import Path

    version_patterns = (
        re.compile(r"(version\s*=\s*)\"\d+\.\d+\.\d+"),
        re.compile(r"(__version__\s*=\s*)\"\d+\.\d+\.\d+"),
        re.compile(r"(\"version\"\s*:\s*)\"\d+\.\d+\.\d+"),
    )

    def update_version(version, filepath):
        with open(filepath, "r") as stream:
            before = stream.read()

        after = before
        for pattern in version_patterns:
            after = re.sub(pattern, r'\1"%s' % (version,), after)

        if before != after:
            print("Changed: ", filepath)
            with open(filepath, "w") as stream:
                stream.write(after)

    # Update version in current project pyproject.toml
    update_version(version, "pyproject.toml")

    # Update version in current project __init__.py
    package_path = IMPORT_NAME.split(".")
    init_file = Path(ROOT, "src", *package_path, "__init__.py")
    update_version(version, init_file)
