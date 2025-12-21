#!/usr/bin/python3
#
# Copyright (c) 2025 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE
#

import argparse
import fileinput
import hashlib
import sys
import textwrap
import types
from importlib.metadata import PackageNotFoundError, version
from typing import Iterable, List

import requests

from pwndck import FlexiHelpFormatter

apiurl = "https://api.pwnedpasswords.com/range/{}"

try:
    __version__ = version("pwndck")
except PackageNotFoundError:
    __version__ = "?"


class PwndException(Exception):
    pass


def get_sha(data: str) -> str:
    hlib = hashlib.sha1()
    hlib.update(data.encode("utf-8"))
    hsh = hlib.hexdigest()

    return hsh.upper()


def get_hashes(key: str) -> str:
    """Return hash-adjacent results
    per https://haveibeenpwned.com/API/v3#PwnedPasswords"""

    url = apiurl.format(key)
    headers = {
        "User-Agent": f"PwndCk/{__version__}",
        "Add-Padding": "true",
    }
    r = requests.get(url, headers=headers)
    response = r.text

    if r.status_code != 200:
        raise PwndException(r.reason)

    return response


def process_pw(pw: str) -> int:
    """
    Returns the number of entries for a password in the Have I Been Pwned
    database.

    Parameters:
        pw (str): The password to check.

    Returns:
        int: The number of entries in the database.

    Raises:
        PwndException: For web query errors.
    """
    hsh = get_sha(pw)
    key = hsh[0:5]
    body = hsh[5:]

    for line in get_hashes(key).splitlines():
        if line.startswith(body):
            (body, count) = line.split(":")
            return int(count)

    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Report # of password hits in HaveIBeenPwned",
        epilog=textwrap.dedent(
            """
            Evaluate one or more passwords against the HaveIBeenPwned
            password database, and return the number of accounts for which
            they have been reported as compromised.

            The number of entries found in the database is returned. If
            multiple passwords are being checked, the password name is also
            returned.

            If the password is not specified on the command line, and there
            is no std input, the user will be prompted.

            The command returns with an error
            code if a password is found in the database.

            The process_pw() function is available for use in Python and can be
            accessed by importing it from its respective module.

            See https://haveibeenpwned.com/API/v3#PwnedPasswords
            """
        ),
        formatter_class=FlexiHelpFormatter,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="suppress output",
        default=False,
        action="store_true",
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-i",
        "--input",
        type=str,
        nargs="?",
        default=None,
        help="file containing passwords, one per line ('-' for stdin)",
    )

    group.add_argument(
        "passwords",
        help="The password(s) to check",
        nargs="*",
        default=None,
        type=str,
    )

    group.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()
    return args


def get_passwords(
    passwords_arg: List[str],
    input_file: str,
) -> Iterable[str]:
    if passwords_arg:
        return passwords_arg

    if input_file:
        return (
            f.strip()
            for f in fileinput.input(files=(input_file,), encoding="utf-8")
        )

    if sys.stdin.isatty():
        return [input("Enter password to check: ")]

    raise PwndException("No passwords")


def quiet_print(string, quiet) -> None:
    if not quiet:
        print(string)


def main() -> None:
    args = parse_args()

    try:
        passwords = get_passwords(args.passwords, args.input)

        fail = False
        verbose = isinstance(passwords, types.GeneratorType) or (
            isinstance(passwords, list) and len(passwords) > 1
        )
        for password in passwords:
            pwcount = process_pw(password)

            if verbose:
                quiet_print(f"{pwcount} {password}", args.quiet)
            else:
                quiet_print(pwcount, args.quiet)

            if pwcount > 0:
                fail = True

    except FileNotFoundError:
        quiet_print("ERROR - Input file not found", args.quiet)
        sys.exit(-2)
    except PermissionError:
        quiet_print(
            "ERROR - Insufficient permissions for input file", args.quiet
        )
        sys.exit(-2)
    except KeyboardInterrupt:
        quiet_print("", args.quiet)
        sys.exit(-2)
    except PwndException as e:
        quiet_print(str(e), args.quiet)
        sys.exit(-2)

    if fail:
        sys.exit(-1)


if __name__ == "__main__":
    main()
