import re
import textwrap
from unittest.mock import MagicMock

import pytest

from pwndck.db_size import (
    estimate_db,
    fmt_num,
    get_line_count,
    get_pw_count,
    random_key,
    sig_figs,
)


def test_random_key_len():
    assert len(random_key()) == 5


def test_random_key_contents():
    key = random_key()
    assert re.search("^[0-9A-F]+$", key)


@pytest.mark.parametrize(
    "body, val",
    [
        ("73A05C0ED0176787A4F1574FF0075F7521E:5", 5),
        ("F27D4201DB9B28483BA83C48EBAFBB2AA17:5000", 5000),
    ],
)
def test_get_pw_count(body, val):
    assert get_pw_count(body) == val


def test_get_line_count():
    testdata = textwrap.dedent(
        """
        73A05C0ED0176787A4F1574FF0075F7521E:4
        F27D4201DB9B28483BA83C48EBAFBB2AA17:5
        DUMMY201DB9B28483BA83C48EBAFBB2AA17:0
        """
    ).strip()

    assert get_line_count(testdata) == 2


num_fmt_cases = [
    (12345, 1, 10000, "10,000"),
    (12345, 2, 12000, "12,000"),
    (12345, 3, 12300, "12,300"),
    (12345, 4, 12340, "12,340"),
    (12345, 5, 12345, "12,345"),
    (395, 5, 395, "395"),
    (395, 1, 400, "400"),
    (350, 1, 400, "400"),
    (349, 1, 300, "300"),
    (395, 0, 0, "0"),
]


@pytest.mark.parametrize("num, digits, result, resultstr", num_fmt_cases)
def test_sig_figs(num, digits, result, resultstr):
    assert sig_figs(num, digits) == result


@pytest.mark.parametrize("num, digits, result, resultstr", num_fmt_cases)
def test_fmt_num(num, digits, result, resultstr):
    assert fmt_num(num, digits) == resultstr


def test_estimate_deb(monkeypatch):
    testdata = textwrap.dedent(
        """
        73A05C0ED0176787A4F1574FF0075F7521E:4
        F27D4201DB9B28483BA83C48EBAFBB2AA17:5
        DUMMY201DB9B28483BA83C48EBAFBB2AA17:0
        """
    ).strip()

    mock_func = MagicMock(return_value=testdata)

    monkeypatch.setattr("pwndck.db_size.get_hashes", mock_func)

    assert estimate_db(10) == (2 * 2**20, 0)
    assert mock_func.call_count == 10
