from typing import Final

ID_TEMPLATE_REGEX: Final = r'(\w+)'

SNIPPET_ID: Final = r'(?<=def )test_snippet_{{ID}}(?=\(.*\):)'
"""Default matching pattern for snippet test
cases. Matches functions like `test_snippet_<id>`,
where the `<id>` part is the actual function
ID placed in the documentation files."""

SNIPPET_INJECT: Final = r'# --Snippet--: {{ID}}'

SNIPPET_END: Final = r'# SNIPPET_END'

ALLOWED_DOC_EXTS: Final = ['.md', '.rst']

ALLOWED_CODE_EXTS: Final = ['.py']