import sys
from unittest.mock import patch

import pytest

import pwndck
from pwndck.processpw import PwndException
from pwndck.pwndckcli import get_passwords, use_verbose


def test_get_passwords_arg():
    assert get_passwords(["foo", "bar"], "baz") == ["foo", "bar"]


def test_get_passwords_input_file(monkeypatch):
    monkeypatch.setattr("fileinput.input", lambda files, encoding: ["buzz"])
    assert [x for x in get_passwords([], "baz")] == ["buzz"]


def test_get_passwords_prompt(monkeypatch):
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt: "buzz")

    assert get_passwords([], "") == ["buzz"]


def test_get_passwrds_nope(monkeypatch):
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)

    with pytest.raises(PwndException):
        get_passwords([], "")


@pytest.mark.parametrize(
    "passwords, result",
    [
        ((x for x in []), True),
        ((x for x in ["one"]), True),
        (["one"], False),
        (["one", "two"], True),
    ],
)
def test_use_verbose(passwords, result):
    assert use_verbose(passwords) == result


@pytest.mark.parametrize(
    "egception, substring",
    [
        (FileNotFoundError, "found"),
        (PermissionError, "permission"),
        (KeyboardInterrupt, ""),
    ],
)
def test_main_wrap_exceptions(monkeypatch, capsys, egception, substring):
    monkeypatch.setattr(sys, "exit", lambda x: -2)

    with patch("pwndck.pwndckcli.main", side_effect=egception()):
        pwndck.pwndckcli.main_wrap()

        captured = capsys.readouterr()

        assert substring in captured.out
