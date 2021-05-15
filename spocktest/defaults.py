from typing import Final

ID_TEMPLATE_REGEX: Final = r'(\w+)'
"""Default regex meaning behind {{ID}}."""

SNIPPET_ID: Final = r'(?<=def )test_snippet_{{ID}}(?=\(.*\):)'
"""Default matching pattern for snippet test
cases. Matches functions like `test_snippet_<id>`,
where the `<id>` part is the actual function
ID placed in the documentation files."""

SNIPPET_INJECT: Final = r'# --Snippet--: {{ID}}'
"""Default regex pattern used to match the snippet placeholder."""

SNIPPET_END: Final = r'# SNIPPET_END'
"""Default regex pattern used to match the snippet cutoff tag."""

ALLOWED_DOC_EXTS: Final = ['.md', '.rst']
"""Default extensions for files with documentation."""

ALLOWED_CODE_EXTS: Final = ['.py']
"""Default extensions for files with code"""
