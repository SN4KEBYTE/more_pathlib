import filecmp
from pathlib import Path
from typing import (
    ContextManager,
    Type,
)

import pytest

from more_pathlib.copy import copy_file
from tests.not_raises import not_raises

_TESTS_DIR = Path(__file__).parent
_DUMMY_FILE = _TESTS_DIR / 'dummy.py'


@pytest.fixture(
    autouse=True,
    scope='function',
)
def rm_dummy_file() -> None:
    yield

    _DUMMY_FILE.unlink(missing_ok=True)


def test_copy_file_src_does_not_exist() -> None:
    with pytest.raises(FileNotFoundError):
        copy_file(
            _DUMMY_FILE,
            _TESTS_DIR / 'not_raises.py',
        )


def test_copy_file_src_is_dir() -> None:
    with pytest.raises(ValueError):
        copy_file(
            _TESTS_DIR,
            _DUMMY_FILE,
        )


def test_copy_file_dest_is_dir() -> None:
    with pytest.raises(ValueError):
        copy_file(
            Path(__file__),
            _TESTS_DIR,
        )


def test_copy_file_normal_copy() -> None:
    copy_file(
        Path(__file__),
        _DUMMY_FILE,
    )

    assert filecmp.cmp(
        Path(__file__),
        _DUMMY_FILE,
    )


@pytest.mark.parametrize(
    'ctx_manager,exception,src,dest,overwrite',
    (
        (
            not_raises,
            Exception,
            Path(__file__),
            _DUMMY_FILE,
            False,
        ),
        (
            not_raises,
            Exception,
            Path(__file__),
            _DUMMY_FILE,
            True,
        ),
        (
            pytest.raises,
            ValueError,
            Path(__file__),
            _TESTS_DIR / 'not_raises.py',
            False,
        ),
        (
            not_raises,
            Exception,
            Path(__file__),
            _DUMMY_FILE,
            True,
        ),
    ),
)
def test_copy_file_different_overwrite(
    rm_dummy_file,
    ctx_manager: ContextManager,
    exception: Type[Exception],
    src: Path,
    dest: Path,
    overwrite: bool,
) -> None:
    with ctx_manager(exception):
        copy_file(
            src,
            dest,
            overwrite_dest=overwrite,
        )
