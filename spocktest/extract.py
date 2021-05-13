import inspect
import textwrap
from spocktest.model import Snippet

def get_snippet_code(snippet_func: Snippet) -> str:
    """
    Extracts snippet function code, omits the definition line and dedents the snippet code.
    """
    return textwrap.dedent("\n".join(inspect.getsource(snippet_func).splitlines()[1:]))
