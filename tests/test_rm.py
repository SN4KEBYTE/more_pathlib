import random
import string
from pathlib import Path
from typing import (
    ContextManager,
    Type,
)

import pytest

from more_pathlib.rm import rmtree
from tests.not_raises import not_raises

_N = 10


def _random_string() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(_N))


def _create_random_tree(
    basedir: Path,
    n_files: int = 2,
    n_folders: int = 1,
    repeat: int = 1,
    sigma_folders: int = 1,
    sigma_files: int = 1,
) -> None:
    for _ in range(repeat):
        for entry in basedir.iterdir():
            for _ in range(int(random.gauss(n_folders, sigma_folders))):
                p = entry / _random_string()
                p.mkdir(exist_ok=True)

            for _ in range(int(random.gauss(n_files, sigma_files))):
                p = entry / _random_string()
                p.touch(exist_ok=True)


# @pytest.mark.parametrize(
#     'ctx_manager,exception,ignore_errors',
#     (
#         (
#             pytest.raises,
#             FileNotFoundError,
#             False,
#         ),
#         (
#             not_raises,
#             Exception,
#             True,
#         ),
#     ),
# )
# def test_rmtree_non_existing_dir(
#     ctx_manager: ContextManager,
#     exception: Type[Exception],
#     ignore_errors: bool,
# ) -> None:
#     with ctx_manager(exception):
#         rmtree(
#             Path(__file__).parent / 'dummy',
#             ignore_errors=ignore_errors,
#         )
