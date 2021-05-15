from typing import List, Optional
from loguru import logger
from spocktest.state import STATE


def is_in_allowed_extensions(
    name:              str,
    allow_extensions:  List[str]
) -> bool:
    return any(
        map(
            lambda ext: name.endswith(ext),
            allow_extensions
        )
    )


def write_file(
    file_path:   str,
    replacement: str
) -> None:
    if STATE.debug:
        logger.debug(f"Writing file {file_path}")
    with open(file_path, 'w') as f:
        f.write(replacement)


def load_file(
    file_path:         str,
    allow_extensions:  List[str]
) -> Optional[str]:
    # first check if the file extension is ok:
    is_allowed_ext = \
        is_in_allowed_extensions(file_path, allow_extensions)

    if not is_allowed_ext:
        return
    
    if STATE.debug:
        logger.debug(f"Reading file {file_path}")

    with open(file_path, 'r') as f:
        contents = f.read()

    return contents
