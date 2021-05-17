import inspect
import textwrap
import re
import os
from spocktest.model import Snippet, SnippetLinesCollection, SnippetsCollection
from spocktest.state import STATE
from spocktest.tools import load_file
from spocktest.defaults import ALLOWED_CODE_EXTS, ID_TEMPLATE_REGEX
from typing import List, Tuple
from collections import defaultdict
from copy import copy
from loguru import logger


def _get_snippet_code_from_fixture(snippet_func: Snippet) -> str:
    """Extracts snippet function code, omits the definition line 
    and dedents the snippet code.
    """
    return textwrap.dedent(
        "\n".join(inspect.getsource(snippet_func).splitlines()[1:])
    )


def __snippet_id_found(snippet_id: str) -> Tuple[List[str], str]:
    """What should happen when snippet ID is found"""
    return [], snippet_id


def __snippet_finish_found(
    existing_snippet_list: List[str]
) -> List[str]:
    """What should happen when snippet finish tag is found"""
    return existing_snippet_list


def __snippet_line_found(
    existing_snippet_list: List[str], 
    line: str
) -> List[str]:
    """What should happen if a snippet line is found"""
    new_list = copy(existing_snippet_list)
    new_list.append(line)
    return new_list


def _get_snippet_code(
    file_content:      str,
    id_pattern:        str,
    finish:            str,
    id_regex_override: str = ID_TEMPLATE_REGEX
) -> SnippetsCollection:
    """Extracts snippet code from an arbitrary file"""
    id_pattern = id_pattern.replace('{{ID}}', id_regex_override)
    lines = file_content.splitlines()
    snippets: SnippetLinesCollection = defaultdict(lambda: [])
    
    for idx, line in enumerate(lines):
        STATE.current_line = idx
        
        m_id = re.search(id_pattern, line)
        if m_id:
            # if an ID is found
            snippet, snippet_id = __snippet_id_found(m_id.groups()[0])
            logger.info(f"Found snippet: {snippet_id}")
            
            snippets[snippet_id] = snippet
            # TODO: move code from cases to the dunder functions
            # set current snippet ID state:
            STATE.current_snippet_id = snippet_id
            
            # set parser state to in-snippet
            STATE.is_snippet = True

        elif re.search(finish, line):
            if STATE.current_snippet_id:
                snippet = __snippet_finish_found(
                    snippets[STATE.current_snippet_id]
                )
                # store snippets on finish:
                snippets[STATE.current_snippet_id] = snippet

                # set state back to initial:
                STATE.is_snippet = False
                STATE.current_snippet_id = None

        else:
            if STATE.current_snippet_id:
                snippet = __snippet_line_found(
                    snippets[STATE.current_snippet_id],
                    line
                )
                # extend snippet container every time a proper
                # snippet line is found:
                snippets[STATE.current_snippet_id] = snippet
    STATE.snippets.update({
        k: textwrap.dedent("\n".join(v)) for k, v in snippets.items()
    })
    return STATE.snippets


def extract(
    input_directory:   str,
    id_pattern:        str,
    finish:            str,
    allow_extensions:  List[str] = ALLOWED_CODE_EXTS,
    id_regex_override: str = ID_TEMPLATE_REGEX
) -> None:
    for root, dirs, files in os.walk(input_directory):
        for name in files:
            file_path = os.path.join(root, name) if root else name

            contents = load_file(file_path, allow_extensions)

            if not contents:
                continue
            
            # extractor loads snippets to the `STATE`
            # container
            _get_snippet_code(
                contents,
                id_pattern,
                finish,
                id_regex_override
            )
