import pytest
import textwrap

import pwndck
from pwndck.pwndck import get_sha, get_hashes, procpw


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
        pwndck.pwndck.requests, "get", return_value=response_mock
    )

    return response_mock


@pytest.mark.parametrize(
    "pw, cnt",
    [
        ("foo", 5),
        ("bar", 0),
    ],
)
def test_procpw_patched(pw, cnt, requests_fixture):
    assert procpw(pw) == cnt


def test_procpw_exception(requests_fixture):
    requests_fixture.status_code = 100

    with pytest.raises(pwndck.pwndck.PwndException):
        procpw("foo")


@pytest.mark.webtest
def test_get_hashes():
    hash_list = get_hashes(foo_key)

    assert foo_hash in hash_list


@pytest.mark.webtest
def test_procpw():
    assert procpw("foo") > 5000
