#!/usr/bin/python3
#
# Copyright (c) 2025 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE
#

import argparse
import hashlib
import sys
import textwrap

from importlib.metadata import version

import requests

apiurl = "https://api.pwnedpasswords.com/range/{}"


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
        "User-Agent": f"PwndCk/{version("pwndck")}",
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
            Evaluate a password against the HaveIBeenPwned password
            database, and return the number of accounts for which it
            has been reported as compromised.

            If the password is not specified on the command line, the
            user will be prompted.

            The command returns with an error
            code if the password is found in the database.

            See https://haveibeenpwned.com/API/v3#PwnedPasswords
            """
        ),
    )

    parser.add_argument(
        "password",
        help="The password to check",
        nargs="?",
        default=None,
        type=str,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="Suppress output",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()
    return args


def main() -> None:

    args = parse_args()

    password = args.password

    if password is None:
        password = input("Enter password to check: ")

    pwcount = procpw(password)

    if not args.quiet:
        print(pwcount)

    if pwcount > 0:
        sys.exit(-1)


if __name__ == "__main__":

    main()
