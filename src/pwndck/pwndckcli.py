#!/usr/bin/python3
#
# Copyright (c) 2025 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE
#

import argparse
import fileinput
import gettext
import sys
import textwrap
import types
from collections.abc import Iterable
from pathlib import Path

from pwndck.db_size import estimate_db, fmt_num
from pwndck.flexi_formatter import FlexiHelpFormatter
from pwndck.processpw import PwndException, process_pw
from pwndck.version import __version__

locale_dir = Path(__file__).resolve().parent.parent.parent / "locales"

lang = gettext.translation("pwndck", localedir=locale_dir, fallback=True)
_ = lang.gettext


def parse_args():

    PWNDURL = "https://haveibeenpwned.com/API/v3#PwnedPasswords"

    parser = argparse.ArgumentParser(
        description=_("Report # of password hits in HaveIBeenPwned"),
        epilog=textwrap.dedent(
            _(
                """
                Evaluate one or more passwords against the HaveIBeenPwned
                password database, and return the number of accounts for which
                they have been reported as compromised.

                The number of entries found in the database is returned. If
                multiple passwords are being checked, the password name is also
                returned.

                If the password is not specified on the command line, the user
                will be prompted.

                The command returns with an error code if a password is found
                in the database.

                The process_pw() function is available for use in Python and
                can be accessed by importing it from the pwndck module.

                See {}
                """
            ).format(PWNDURL)
        ),
        formatter_class=FlexiHelpFormatter,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help=_("suppress output"),
        default=False,
        action="store_true",
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-i",
        "--input",
        type=str,
        action="store",
        default=None,
        help=_("file containing passwords, one per line ('-' for stdin)"),
    )

    group.add_argument(
        "passwords",
        help=_("The password(s) to check"),
        nargs="*",
        default=None,
        metavar="password",
        type=str,
    )

    group.add_argument(
        "-e",
        "--estimatedb",
        action="store_true",
        help=_(
            "estimate the current size of the HaveIBeenPwnd password database"
        ),
    )

    group.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()
    return args


def get_passwords(
    passwords_arg: list[str],
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
        return [input(_("Enter password to check: "))]

    raise PwndException(_("No passwords"))


def quiet_print(string: str, quiet: bool = False) -> None:
    if not quiet:
        print(string)


def use_verbose(passwords: Iterable[str]) -> bool:
    verbose = isinstance(passwords, types.GeneratorType) or (
        isinstance(passwords, list) and len(passwords) > 1
    )
    return verbose


def main(args: argparse.Namespace) -> int:

    return_val = 0

    if args.estimatedb:
        mean, _stddev = estimate_db()
        estimate = fmt_num(mean, 3)
        quiet_print(
            _(
                "There are currently approximately {} entries in the HaveIBeenPwned password database"
            ).format(estimate)
        )

    else:
        passwords = get_passwords(args.passwords, args.input)

        verbose = use_verbose(passwords)

        for password in passwords:
            pwcount = process_pw(password)

            if verbose:
                quiet_print(f"{pwcount:<8}  {password:}", args.quiet)
            else:
                quiet_print(pwcount, args.quiet)

            if pwcount > 0:
                return_val = -1

    return return_val


def main_wrap():
    errmsg = {
        FileNotFoundError: _("ERROR - Input file not found"),
        PermissionError: _("ERROR - Insufficient permissions for input file"),
        KeyboardInterrupt: "",
    }

    args = parse_args()

    try:
        error_code: int = main(args)
    except PwndException as e:
        quiet_print(str(e), args.quiet)
        error_code = -2
    except tuple(errmsg.keys()) as e:
        quiet_print(errmsg[type(e)], args.quiet)
        error_code = -2

    sys.exit(error_code)


if __name__ == "__main__":
    main_wrap()
