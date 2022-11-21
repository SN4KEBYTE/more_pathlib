from pathlib import Path

from more_pathlib.validation import validate_directory


def before_dump_hook(
    path: Path,
    *,
    strict: bool,
) -> None:
    if strict:
        validate_directory(path.parent)
    else:
        path.parent.mkdir(
            exist_ok=True,
            parents=True,
        )
