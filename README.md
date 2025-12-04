# pwndck

Check the the HaveIBeenPwned password database to see if a particular password
has been compromised.

It uses the [haveibeenpwned API](https://haveibeenpwned.com/API/v3#PwnedPasswords)
for the check:
  * This use does not require an API key. Anyone can run it.
  * This is more secure than the [web page tool](https://haveibeenpwned.com/Passwords).
    your password is not exposed beyond your local machine.
  * It returns the number of times the password occurs in the database.

# Install
Install from [PyPi](https://pypi.org/project/pwndck/)

# Usage

    $ pwndck -h
    usage: pwndck [-h] [-q] [-i [INPUT] | passwords ...]
    
    Report # of password hits in HaveIBeenPwned
    
    positional arguments:
      passwords            The password(s) to check
    
    options:
      -h, --help           show this help message and exit
      -q, --quiet          Suppress output
      -i, --input [INPUT]  File containing passwords, one per line
                           ('-' for stdin)
    
    Evaluate one or more passwords against the HaveIBeenPwned
    password database, and return the number of accounts for which
    they have been reported as compromised.
     
    The number of entries found in the database is returned. if
    multiple passwords are being checked, the password name is also
    returned.
     
    If the password is not specified on the command line, the user
    will be prompted.
     
    The command returns with an error code if the password is found
    in the database.
     
    See https://haveibeenpwned.com/API/v3#PwnedPasswords
