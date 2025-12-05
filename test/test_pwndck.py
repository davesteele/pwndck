


import pytest
from typing import NamedTuple

import pwndck.pwndck as pwndck


class ShaCase(NamedTuple):
    src: str
    sha: str

@pytest.mark.parametrize(
    "case",
    [
        ShaCase("foo", "0BEEC7B5EA3F0FDBC95D0DD47F3C5BC275DA8A33"),
        ShaCase("Foo", "201A6B3053CC1422D2C3670B62616221D2290929"),
    ],
)
def test_get_sha(case):
    assert pwndck.get_sha(case.src) == case.sha

