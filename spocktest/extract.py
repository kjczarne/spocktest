import inspect
import textwrap
import re
from spocktest.model import Snippet, SnippetLinesCollection, SnippetsCollection
from typing import Dict, Final, List, Optional
from collections import defaultdict
from copy import copy
from dataclasses import dataclass


def get_snippet_code_from_fixture(snippet_func: Snippet) -> str:
    """Extracts snippet function code, omits the definition line 
    and dedents the snippet code.
    """
    return textwrap.dedent(
        "\n".join(inspect.getsource(snippet_func).splitlines()[1:])
    )


def __snippet_id_found(snippet_id: str):
    """What should happen when snippet ID is found"""
    return [], snippet_id


def __snippet_finish_found(
    existing_snippet_list: List[str]
):
    """What should happen when snippet finish tag is found"""
    return existing_snippet_list


def __snippet_line_found(
    existing_snippet_list: List[str], 
    line: str
):
    """What should happen if a snippet line is found"""
    new_list = copy(existing_snippet_list)
    new_list.append(line)
    return new_list


@dataclass
class ExtractorState:
    """State container for the snippet parser."""
    # TODO: should be a Singleton
    is_snippet: bool
    current_snippet_id: Optional[str]
    current_line: int


STATE: Final = ExtractorState(False, None, 0)


def get_snippet_code(
    file_content: str,
    id:           str,
    finish:       str
) -> SnippetsCollection:
    """Extracts snippet code from an arbitrary file"""
    id_pattern = id.replace('{{ID}}', r'(\w+)')
    lines = file_content.splitlines()
    snippets: SnippetLinesCollection = defaultdict(lambda: [])
    
    for idx, line in enumerate(lines):
        STATE.current_line = idx
        
        m_id = re.search(id_pattern, line)
        if m_id:
            # if an ID is found
            snippet, snippet_id = __snippet_id_found(m_id.groups()[0])
            snippets[snippet_id] = snippet
            # TODO: move code from cases to the dunder functions
            # set current snippet ID state:
            STATE.current_snippet_id = snippet_id
            
            # set parser state to in-snippet
            STATE.is_snippet = True

        elif re.match(finish, line):
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
    return {
        k: textwrap.dedent("\n".join(v)) for k, v in snippets.items()
    }
