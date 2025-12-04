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
from importlib.metadata import version
from typing import List

import requests

from pwndck import FlexiHelpFormatter

apiurl = "https://api.pwnedpasswords.com/range/{}"

__version__ = version("pwndck")


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


def procpw(pw: str) -> int:
    """Return # of times found in HIBP"""
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

            If the password is not specified on the command line, the
            user will be prompted.

            The command returns with an error
            code if the password is found in the database.

            See https://haveibeenpwned.com/API/v3#PwnedPasswords
            """
        ),
        formatter_class=FlexiHelpFormatter,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="Suppress output",
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
        help="File containing passwords, one per line ('-' for stdin)",
    )

    group.add_argument(
        "passwords",
        help="The password(s) to check",
        nargs="*",
        default=None,
        type=str,
    )

    group.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()
    return args


def get_passwords(
    passwords_arg: List[str],
    input_file: str,
) -> List[str]:
    if passwords_arg:
        return passwords_arg

    if input_file:
        return [
            f.strip()
            for f in fileinput.input(files=(input_file,), encoding="utf-8")
        ]

    return [input("Enter password to check: ")]


def main() -> None:
    args = parse_args()

    try:
        passwords = get_passwords(args.passwords, args.input)
    except FileNotFoundError:
        if not args.quiet:
            print("ERROR - Input file not found")
        sys.exit(-2)
    except PermissionError:
        if not args.quiet:
            print("ERROR - Insufficient permissions for input file")
        sys.exit(-2)

    fail = False
    verbose = len(passwords) > 1
    for password in passwords:
        pwcount = procpw(password)

        if not args.quiet:
            if verbose:
                print(f"{pwcount} {password}")
            else:
                print(pwcount)

        if pwcount > 0:
            fail = True

    if fail:
        sys.exit(-1)


if __name__ == "__main__":
    main()
