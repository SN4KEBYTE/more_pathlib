import contextlib
import random
import string
from pathlib import Path

import pytest

from more_pathlib.rm import rmtree

_MAX_FILENAME_LEN = 10
_DUMMY_DIR = Path(__file__).parent / 'dummy'

random.seed(1)


def _random_filename() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(_MAX_FILENAME_LEN))


def _create_random_tree(
    basedir: Path,
    n_files: int = 10,
    n_folders: int = 5,
    sigma_folders: int = 1,
    sigma_files: int = 1,
    max_depth: int = 3,
) -> None:
    if max_depth < 1:
        return

    basedir.mkdir(
        parents=False,
        exist_ok=True,
    )

    for _ in range(int(random.gauss(n_folders, sigma_folders))):
        path = basedir / _random_filename()
        path.mkdir(exist_ok=True)

        _create_random_tree(
            path,
            max_depth=max_depth - 1,
        )

    for _ in range(int(random.gauss(n_files, sigma_files))):
        path = basedir / _random_filename()
        path.touch(exist_ok=True)


@pytest.fixture(
    scope='function',
    autouse=True,
)
def cleanup() -> None:
    with contextlib.suppress(Exception):
        rmtree(
            _DUMMY_DIR,
            keep_root=False,
        )


def test_rmtree_non_existing_dir() -> None:
    with pytest.raises(FileNotFoundError):
        rmtree(_DUMMY_DIR)


def test_rmtree_file() -> None:
    with pytest.raises(ValueError):
        rmtree(Path(__file__))


@pytest.mark.parametrize(
    'keep_root',
    (
        True,
        False,
    ),
)
def test_rmtree_empty_dir(
    keep_root: bool,
) -> None:
    _DUMMY_DIR.mkdir()

    rmtree(
        _DUMMY_DIR,
        keep_root=keep_root,
    )

    assert _DUMMY_DIR.exists() == keep_root


@pytest.mark.parametrize(
    'keep_root',
    (
        True,
        False,
    ),
)
def test_rmtree_dir_with_files(
    keep_root: bool,
) -> None:
    _create_random_tree(_DUMMY_DIR)

    rmtree(
        _DUMMY_DIR,
        keep_root=keep_root,
    )

    assert not _DUMMY_DIR.exists() or not len(list(_DUMMY_DIR.iterdir()))
