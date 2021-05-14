from spocktest.model import SnippetsCollection
from loguru import logger
from typing import Generator, List, Optional, Union
import os
import re


def __replace_file_contents(
    id:       str,
    snippet:  str,
    contents: str
):
    return re.sub(id, snippet, contents)


def __write_file(
    file_path:   str,
    replacement: str
):
    with open(file_path, 'w') as f:
        f.write(replacement)


def __recursive_replace(
    file_path:             str,
    contents:              str,
    id_extraction_pattern: str,
    snippet:               str,
    snippet_id:            str,
):
    id_replacement_pattern = id_extraction_pattern.replace(
        '{{ID}}', snippet_id
    )
    m = re.search(
        id_replacement_pattern,
        contents
    )
    if m:
        repl = __replace_file_contents(
            id_replacement_pattern, snippet, contents
        )
        return __recursive_replace(
            file_path,
            repl,
            id_extraction_pattern,
            snippet,
            snippet_id
        )
    else:
        return contents


def __process_file(
    root:                  Optional[str],
    name:                  str,
    id_extraction_pattern: str,
    snippets:              SnippetsCollection,
    ignore_extensions:     List[str] = [],
    debug:                 bool = False
):
    # first check if the file extension is ok:
    is_disallowed_ext = \
        any(map(lambda ext: name.endswith(ext), ignore_extensions))
    
    if is_disallowed_ext:
        return
    
    # get the full path to the file and read it:
    file_path = os.path.join(root, name) if root else name
    logger.debug(f"Reading file {file_path}")

    with open(file_path, 'r') as f:
        contents = f.read()
    
    # check if any of the known snippets matches
    # an ID used anywhere in the file:
    logger.debug(f"Writing file {file_path}")
    new_contents = contents
    for snippet_id, snippet in snippets.items():
        new_contents = __recursive_replace(
            file_path,
            new_contents,
            id_extraction_pattern,
            snippet,
            snippet_id
        )
    else:
        if debug:
            return new_contents
        else:
            __write_file(
                file_path,
                new_contents
            )
        # id_replacement_pattern = id_extraction_pattern.replace(
        #     '{{ID}}', snippet_id
        # )
        # m = re.search(
        #     id_replacement_pattern,
        #     contents
        # )
        # if m:
        #     if debug:
        #         repl = __replace_file_contents(
        #             id_replacement_pattern, snippet, contents
        #         )
        #         return repl
        #     else:
        #         repl = __replace_file_contents(
        #             id_replacement_pattern, snippet, contents
        #         )
        #         __write_file(
        #             file_path,
        #             repl
        #         )


def inject(
    path:                  str,
    id_extraction_pattern: str,
    snippets:              SnippetsCollection,
    ignore_extensions:     List[str] = [],
    debug:                 bool = False
):
    """Walks through an input directory with
    documentation files and creates a copy
    of the documentation or does in-place
    substitution of specific snippet IDs
    with corresponding snippets."""
    if os.path.isfile(path):
        return __process_file(
            None,
            path,
            id_extraction_pattern,
            snippets,
            ignore_extensions,
            debug
        )

    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                return __process_file(
                    root,
                    name,
                    id_extraction_pattern,
                    snippets,
                    ignore_extensions,
                    debug
                )
    else:
        raise ValueError(
            "Path is neither a directory nor a file " + \
            "I have no idea how you managed to break it " + \
            "but mazel tov!"
        )
