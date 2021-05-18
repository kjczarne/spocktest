from spocktest.state import STATE
from spocktest.model import SnippetsCollection
from spocktest.tools import load_file, write_file
from spocktest.defaults import ALLOWED_DOC_EXTS
from typing import List, Optional
import os
import re
import shutil


def __replace_file_contents(
    id:       str,
    snippet:  str,
    contents: str
) -> str:
    return re.sub(id, snippet, contents)


def __recursive_replace(
    file_path:             str,
    contents:              str,
    id_extraction_pattern: str,
    snippet:               str,
    snippet_id:            str,
) -> str:
    id_replacement_pattern = id_extraction_pattern.replace(
        '{{ID}}', snippet_id
    )
    # match whitespace and lock indentation offset on the tag indent
    m = re.search(f'([\\t ]+)?({id_replacement_pattern})', contents)
    if m:
        indent, match_pattern = m.groups()
        
        # first line is already indented correctly, the rest needs to be offset
        lines = snippet.splitlines()
        lines = [lines[0]] + [indent + i for i in lines[1:]] if indent else lines
        snippet_with_indent = "\n".join(lines)
        
        repl = __replace_file_contents(
            match_pattern, snippet_with_indent, contents
        )
        
        return __recursive_replace(
            file_path,
            repl,
            id_extraction_pattern,
            snippet,
            snippet_id
        )
    else:
        STATE.placeholders_filled += 1
        return contents


def __process_file(
    root:                  Optional[str],
    name:                  str,
    id_extraction_pattern: str,
    snippets:              SnippetsCollection,
    allowed_extensions:    List[str] = ALLOWED_DOC_EXTS
) -> None:    
    # get the full path to the file and read it:
    file_path = os.path.join(root, name) if root else name

    contents = load_file(file_path, allowed_extensions) 
    
    # if the file has an ignored extension, it won't be
    # loaded and we shall then return `None`
    if not contents:
        return

    # check if any of the known snippets matches
    # an ID used anywhere in the file:
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
        if STATE.debug:
            STATE.debug_container.append(new_contents)
        else:
            write_file(
                file_path,
                new_contents
            )


def inject(
    path:                  str,
    id_extraction_pattern: str,
    snippets:              SnippetsCollection,
    out_path:              Optional[str] = None,
    allowed_extensions:    List[str] = ALLOWED_DOC_EXTS
) -> None:
    """Walks through an input directory with
    documentation files and creates a copy
    of the documentation or does in-place
    substitution of specific snippet IDs
    with corresponding snippets."""

    if os.path.isfile(path):
        if out_path:
            shutil.copyfile(path, out_path)
            __process_file(
                None,
                out_path,
                id_extraction_pattern,
                snippets,
                allowed_extensions
            )
        else:
            __process_file(
                None,
                path,
                id_extraction_pattern,
                snippets,
                allowed_extensions
            )

    elif os.path.isdir(path):
        if out_path:
            # if a different output dir is provided from the
            # initial doc tree, we will copy the whole tree
            # to `out_path` and then process the copy:
            if os.path.exists(out_path):
                shutil.rmtree(out_path)
            shutil.copytree(path, out_path)
            for root, dirs, files in os.walk(out_path):
                for name in files:
                    __process_file(
                        root,
                        name,
                        id_extraction_pattern,
                        snippets,
                        allowed_extensions
                    )
        else:
            # if no extra output dir is provided, we replace
            # the same doctree
            for root, dirs, files in os.walk(path):
                for name in files:
                    __process_file(
                        root,
                        name,
                        id_extraction_pattern,
                        snippets,
                        allowed_extensions
                    )
    else:
        raise ValueError(
            "Path is neither a directory nor a file " + \
            "I have no idea how you managed to break it " + \
            "but mazel tov!"
        )
