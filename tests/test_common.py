import shutil
from pathlib import Path

import pytest

from more_pathlib.common import before_dump_hook

_DUMMY_FILE = Path(__file__).parent / 'a' / 'b.py'


@pytest.fixture(autouse=True)
def _cleanup() -> None:
    yield

    shutil.rmtree(
        _DUMMY_FILE.parent,
        ignore_errors=True,
    )


def test_before_dump_strict_no_parent() -> None:
    with pytest.raises(FileNotFoundError):
        before_dump_hook(
            _DUMMY_FILE,
            strict=True,
        )


def test_before_dump_strict_parent_is_file() -> None:
    with pytest.raises(ValueError):
        before_dump_hook(
            Path(__file__) / 'file.py',
            strict=True,
        )


def test_before_dump_non_strict() -> None:
    before_dump_hook(
        _DUMMY_FILE,
        strict=False,
    )

    assert _DUMMY_FILE.parent.exists()
