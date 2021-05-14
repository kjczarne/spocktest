from typing import Final

SNIPPET_ID: Final = r'(?<=def )test_snippet_{{ID}}(?=\(.*\):)'
"""Default matching pattern for snippet test
cases. Matches functions like `test_snippet_<id>`,
where the `<id>` part is the actual function
ID placed in the documentation files."""

SNIPPET_INJECT: Final = r'# --Snippet--: {{ID}}'

SNIPPET_END: Final = r'# SNIPPET_END'
