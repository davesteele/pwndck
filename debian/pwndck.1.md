---
date: February 2026
section: 1
title: PWNDCK
---

# NAME

pwndck - Check passwords against the HaveIBeenPwned leak database

# DESCRIPTION

usage: pwndck \[-h\] \[-q\] \[\[-i \[INPUT\]\] \| \[passwords
\...\] \| \[\--version\]\]

Report \# of password hits in HaveIBeenPwned

## positional arguments:

passwords

:   The password(s) to check

## options:

**-h**, **\--help**

:   show this help message and exit

**-q**, **\--quiet**

:   suppress output

**-i**, **\--input** \[INPUT\]

:   file containing passwords, one per line (\'-\' for stdin)

**\--version**

:   show program\'s version number and exit

Evaluate one or more passwords against the HaveIBeenPwned password
database, and return the number of accounts for which they have been
reported as compromised.

The number of entries found in the database is returned. If multiple
passwords are being checked, the password name is also returned.

If the password is not specified on the command line, and there is no
std input, the user will be prompted.

The command returns with an error code if a password is found in the
database.

The process\_pw() function is available for use in Python. It can be
accessed by importing it from the pwndck module.

See https://haveibeenpwned.com/API/v3#PwnedPasswords
