#!/usr/bin/python3
#
# Copyright (c) 2022 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE
#

"""
devtest.py

This creates a  virtual environment, and runs a number of test environments
against the comitup code.

The venv is persistent, and the tests run in parallel, so this is much quicker
than tox or nox.
"""

import shlex
import subprocess
import sys
import textwrap
import venv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

envpath: Path = Path(__file__).resolve().parent / ".devenv"
pythonpath: str = str(envpath / "bin" / "python")


pkgs: list[str] = [
    "pytest",
    "ruff",
]

targets: str = "pwndck test devtest.py"


def mkcmd(cmd: str) -> list[str]:
    return [str(pythonpath), "-m"] + shlex.split(cmd)


def run(cmd: str) -> subprocess.CompletedProcess:
    cp = subprocess.run(
        mkcmd(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    return cp


print("# Tests starting")

if not envpath.exists():
    print("# Creating virtual environment")

    virtenv = venv.EnvBuilder(
        system_site_packages=True, symlinks=True, with_pip=True
    )
    virtenv.create(str(envpath))

    print("# Installing packages")

    for pkg in pkgs:
        cp = run("pip install " + pkg)
        print("Running", " ".join(cp.args))
        print(cp.stdout.decode())


tests: list[str] = [
    f"ruff format --check {targets}",
    f"ruff check --select I {targets}",
    f"ruff check {targets}",
    "pytest -m always_run",
]

executor = ThreadPoolExecutor(max_workers=5)

fail = False
for result in executor.map(lambda x: run(x), tests):
    judgement = "PASS" if not result.returncode else "FAIL"
    print(
        textwrap.dedent(
            f"""\
            #####################################
            # Running {" ".join(result.args)}
            {textwrap.indent(result.stdout.decode(), "            ")}
            ################{judgement}#################
            """
        )
    )
    if result.returncode:
        fail = True

if fail:
    print("# ERROR(S) ENCOUNTERED")
    sys.exit(1)

print("# Tests complete")
