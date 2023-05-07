import json
from pathlib import Path
from typing import Any

from more_pathlib.common import before_dump_hook
from more_pathlib.validation import validate_file_path

_JSON_EXTENSIONS = frozenset(('.json',))


def dump_json(
    obj: Any,  # noqa: WPS110
    path: Path,
    *,
    validate_parent_dir: bool = False,
    encoding: str = 'utf-8',
    **kwargs: Any,
) -> None:
    before_dump_hook(
        path,
        validate_parent_dir=validate_parent_dir,
    )

    with open(path, 'w', encoding=encoding) as out:
        json.dump(
            obj,
            out,
            **kwargs,
        )


def load_json(
    path: Path,
    *,
    encoding: str = 'utf-8',
    **kwargs: Any,
) -> Any:
    validate_file_path(
        path,
        _JSON_EXTENSIONS,
    )

    with open(path, 'r', encoding=encoding) as inp:
        return json.load(
            inp,
            **kwargs,
        )
