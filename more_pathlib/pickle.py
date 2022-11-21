import pickle
from pathlib import Path
from typing import Any

from more_pathlib.common import before_dump_hook
from more_pathlib.validation import validate_file_path

_PICKLE_EXTENSIONS = frozenset((
    '.p',
    '.pkl',
    '.pickle',
))


def dump_pickle(
    obj: Any,  # noqa: WPS110
    path: Path,
    *,
    strict: bool,
    **kwargs: Any,
) -> None:
    before_dump_hook(
        path,
        strict=strict,
    )

    with open(path, 'wb') as out:
        pickle.dump(
            obj,
            out,
            **kwargs,
        )


def load_pickle(
    path: Path,
    **kwargs: Any,
) -> Any:
    validate_file_path(
        path,
        _PICKLE_EXTENSIONS,
    )

    with open(path, 'rb') as inp:
        return pickle.load(
            inp,
            **kwargs,
        )
