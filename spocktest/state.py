from dataclasses import dataclass
from typing import Optional, Final, List
from spocktest.model import SnippetsCollection


@dataclass
class __StateStore:
    """State container for the snippet parser.
    The classs is hidden away and should always be exposed
    as a Singleton by importing the `STATE` instance.
    """
    is_snippet: bool
    current_snippet_id: Optional[str]
    current_line: int
    snippets: SnippetsCollection
    placeholders_filled: int
    debug_container: List[str]
    debug: bool = False

    def reset(self):
        self.is_snippet = False
        self.current_snippet_id = None
        self.current_line = 0
        self.snippets = {}
        self.placeholders_filled = 0
        self.debug_container = []
        # do not reset self.debug!


STATE: Final = __StateStore(False, None, 0, {}, 0, [])
