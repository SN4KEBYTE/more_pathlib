from pathlib import Path

from more_pathlib.validation import validate_file_path

_DEFAULT_CHUNK_SIZE = 4096


def copy_file(
    src: Path,
    dest: Path,
    *,
    overwrite_dest: bool = False,
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
) -> None:
    if chunk_size <= 0:
        raise ValueError('chunk size must be greater than zero')

    validate_file_path(src)

    try:
        validate_file_path(dest)
    except FileNotFoundError:
        pass  # noqa: WPS420
    else:
        if not overwrite_dest:
            raise ValueError('dest exists, but overwrite_dest was set to False')

    with open(src, 'rb') as src_f, open(dest, 'wb') as dest_f:  # noqa: WPS316
        chunk = src_f.read(chunk_size)

        while chunk:
            dest_f.write(chunk)
            chunk = src_f.read(chunk_size)
