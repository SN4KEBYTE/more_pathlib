from pathlib import Path

import pytest

from more_pathlib.validation import (
    validate_directory,
    validate_file_path,
)
from tests.not_raises import not_raises

_TESTS_DIR = Path(__file__).parent
_DUMMY_FILE = _TESTS_DIR / 'dummy.py'


@pytest.fixture(
    scope='session',
    autouse=True,
)
def create_test_file() -> None:
    _DUMMY_FILE.touch(exist_ok=True)

    yield

    _DUMMY_FILE.unlink(missing_ok=True)


def test_validate_fp_non_existing_file() -> None:
    with pytest.raises(FileNotFoundError):
        validate_file_path(_TESTS_DIR / 'smth.py')


def test_validate_fp_is_directory() -> None:
    with pytest.raises(ValueError):
        validate_file_path(_TESTS_DIR)


def test_validate_fp_invalid_target_extension() -> None:
    with pytest.raises(ValueError):
        validate_file_path(
            _DUMMY_FILE,
            {
                '.py',
                'wrong',
            },
        )


def test_validate_fp_wrong_file_extension() -> None:
    with pytest.raises(ValueError):
        validate_file_path(
            _DUMMY_FILE,
            {
                '.pyi',
                '.pyc',
            },
        )


def test_validate_fp_valid_file() -> None:
    with not_raises(Exception):
        validate_file_path(
            _DUMMY_FILE,
            {'.py'},
        )


def test_validate_dir_non_existing() -> None:
    with pytest.raises(FileNotFoundError):
        validate_directory(_TESTS_DIR / 'dummy')


def test_validate_dir_is_file() -> None:
    with pytest.raises(ValueError):
        validate_directory(Path(__file__))


def test_validate_dir_normal_dir() -> None:
    with not_raises(Exception):
        validate_directory(_TESTS_DIR)
