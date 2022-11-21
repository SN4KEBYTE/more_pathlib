from pathlib import Path


def rmtree(  # noqa: WPS231
    path: Path,
    *,
    keep_root: bool = False,
    ignore_errors: bool = True,
) -> None:
    for child in path.iterdir():
        if child.is_file():
            child.unlink(missing_ok=ignore_errors)
        else:
            rmtree(
                child,
                keep_root=keep_root,
                ignore_errors=ignore_errors,
            )

    if not keep_root:
        try:
            path.rmdir()
        except FileNotFoundError as err:
            if not ignore_errors:
                raise err
