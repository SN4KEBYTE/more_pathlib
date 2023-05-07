from pathlib import Path

from more_pathlib.validation import validate_directory


def rmtree(  # noqa: WPS231
    path: Path,
    *,
    keep_root: bool = False,
) -> None:
    validate_directory(path)

    for child in path.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rmtree(
                child,
                keep_root=False,
            )

    if not keep_root:
        path.rmdir()
