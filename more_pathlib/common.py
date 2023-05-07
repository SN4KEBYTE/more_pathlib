from pathlib import Path

from more_pathlib.validation import validate_directory


def before_dump_hook(
    path: Path,
    *,
    validate_parent_dir: bool,
) -> None:
    if validate_parent_dir:
        validate_directory(path.parent)
    else:
        path.parent.mkdir(
            exist_ok=True,
            parents=True,
        )
