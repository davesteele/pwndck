import hashlib

import requests

from pwndck.version import __version__

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
