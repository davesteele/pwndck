# pwndck

Check the the HaveIBeenPwned password database to see if a particular password
has been compromised.

It uses the [haveibeenpwned API](https://haveibeenpwned.com/API/v3#PwnedPasswords)
for the check:
  * Use does not require an API key. Anyone can run it.
  * It is more secure than the [web page tool](https://haveibeenpwned.com/Passwords).
    your password is
    [not exposed](https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/)
    beyond your local machine.
  * This is a lightweight install. There are no large downloads.

It returns the number of times the password occurs in the database.

# Install
Install from [PyPi](https://pypi.org/project/pwndck/)

For Debian forky or newer, use

    sudo apt install pwndck

For other Debian derivatives, download the [deb file](https://deb.debian.org/debian/pool/main/p/pwndck/) and install with:

    sudo dpkg -i pwndck_*_all.deb
    sudo apt -f install

# Usage

    $ pwndck -h
    usage: pwndck [-q] [ [password]... | -i INPUT | --version | -h | -e ]
    
    Report # of password hits in HaveIBeenPwned
    
    positional arguments:
      passwords            The password(s) to check
    
    options:
      -h, --help           show this help message and exit
      -q, --quiet          Suppress output
      -i, --input INPUT    File containing passwords, one per line
                           ('-' for stdin)
      -e, --estimatedb     Estimate the current size of the HaveIBeenPwned
                           password database
      --version            show program's version number and exit
    
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

# Module

    $ python3
    Python 3.13.11 (main, Dec  8 2025, 11:43:54) [GCC 15.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pwndck
    >>> help(pwndck.processpw)
    Help on function process_pw in module pwndck.processpw:

    process_pw(pw: str) -> int
        Returns the number of entries for a password in the Have I Been Pwned
        database.

        Parameters:
            pw (str): The password to check.

        Returns:
            int: The number of entries in the database.

        Raises:
            PwndException: For web query errors.

    >>> pwndck.process_pw("password")
    52256179
    >>>
