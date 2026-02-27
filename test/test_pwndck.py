import textwrap

import pytest

import pwndck
import pwndck.processpw
from pwndck.processpw import PwndException, get_hashes, get_sha, process_pw
from pwndck.pwndck import get_passwords

foo_sha = "0BEEC7B5EA3F0FDBC95D0DD47F3C5BC275DA8A33"
foo_key = "0BEEC"
foo_hash = "7B5EA3F0FDBC95D0DD47F3C5BC275DA8A33"


def test_null():
    pass


def test_pwndck_null():
    get_sha("foo")


def test_get_sha():
    assert get_sha("foo") == foo_sha


@pytest.fixture
def requests_fixture(mocker):
    response_mock = mocker.Mock()

    response_mock.status_code = 200
    response_mock.text = textwrap.dedent(
        f"""
        {foo_hash}:5

        """
    )

    mocker.patch.object(
        pwndck.processpw.requests, "get", return_value=response_mock
    )

    return response_mock


@pytest.mark.parametrize(
    "pw, cnt",
    [
        ("foo", 5),
        ("bar", 0),
    ],
)
def test_process_pw_patched(pw, cnt, requests_fixture):
    assert process_pw(pw) == cnt


def test_process_pw_exception(requests_fixture):
    requests_fixture.status_code = 100

    with pytest.raises(PwndException):
        process_pw("foo")


@pytest.mark.webtest
def test_get_hashes():
    hash_list = get_hashes(foo_key)

    assert foo_hash in hash_list


@pytest.mark.webtest
def test_process_pw():
    assert process_pw("foo") > 5000


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
