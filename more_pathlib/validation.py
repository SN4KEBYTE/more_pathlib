import re
from pathlib import Path
from typing import (
    Collection,
    Optional,
)

_EXTENSION_RE = re.compile(r'^\.[a-zA-Z0-9_]+$')


def _check_provided_extensions(
    extensions: Collection[str],
) -> None:
    bad_extensions = [ext for ext in extensions if not _EXTENSION_RE.match(ext)]

    if bad_extensions:
        raise ValueError(f'found invalid target extensions: {",".join(bad_extensions)}')


def validate_file_path(
    path: Path,
    extensions: Optional[Collection[str]] = None,
) -> None:
    if not path.exists():
        raise FileNotFoundError(f'file {path.resolve()} does not exist')

    if not path.is_file():
        raise ValueError(f'file {path.resolve()} is not a file')

    if extensions is not None:
        _check_provided_extensions(extensions)

        if path.suffix not in extensions:
            raise ValueError(f'found {path.suffix} extension, expected one of {",".join(extensions)}')


def validate_directory(
    path: Path,
) -> None:
    if not path.exists():
        raise FileNotFoundError(f'directory {path.resolve()} does not exist')

    if not path.is_dir():
        raise ValueError(f'directory {path.resolve()} is not a directory')
