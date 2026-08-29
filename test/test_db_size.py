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


def test_sig_figs():
    assert sig_figs(12345, 2) == 12000


def test_fmt_num():
    assert fmt_num(12345, 2) == "12,000"


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
