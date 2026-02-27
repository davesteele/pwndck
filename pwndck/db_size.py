import secrets
import statistics
from math import floor, log10

from pwndck.processpw import get_hashes


def random_key() -> str:
    return secrets.token_hex(3)[:5].upper()


def get_pw_count(db_line: str) -> int:
    str_cnt = db_line.split(":")[1]
    cnt = int(str_cnt)
    return cnt


def get_line_count(hash_response: str) -> int:
    return len([x for x in hash_response.splitlines() if get_pw_count(x) > 0])


def estimate_db(samples: int = 10):
    keys = (random_key() for _ in range(samples))

    hashes = (get_hashes(x) for x in keys)

    lengths = [get_line_count(x) for x in hashes]

    scale = int(2**20)

    mean = scale * statistics.mean(lengths)
    stdev = scale * statistics.stdev(lengths)

    return mean, stdev


def sig_figs(x: float, precision: int) -> float:
    x = float(x)
    precision = int(precision)

    return round(x, -int(floor(log10(abs(x)))) + (precision - 1))


def fmt_num(num: float, precision: int) -> str:
    return f"{int(sig_figs(num, precision)):,}"
