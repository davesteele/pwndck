% pwndck(1)
%
% Oct 2025

# NAME

pwndck -- check passwords against the HaveIBeenPwned leak database

## SYNOPSIS

**pwndck** [**-h**] [**-q**] [**-i** [INPUT] | **password**...]

## DESCRIPTION

The **pwndck** utility evaluates a password against the HaveIBeenPwned password
database, and returns the number of accounts for which it has been reported as
compromised.

The number of entries found in the database is returned. if
multiple passwords are being checked, the password name is also
returned.
 
If the password is not specified on the command line, the user will be prompted.
 
The command returns with an error code if a password is found in the database.
 
See https://haveibeenpwned.com/API/v3#PwnedPasswords

## General Options

**-h**, **-\-help**
:   Display a friendly help message.

**-q**, **-\-quiet**
:   Don't output text for successful runs, just return an error code.

**-i**, **-\-input**
:   File containing passwords, one per line ('-' for stdin)

## COPYRIGHT

Comitup is Copyright (C) 2025 David Steele &lt;steele@debian.org&gt;

