from typing import Any, Callable, Literal, Tuple, Type, List, NewType, Union, Optional, Dict

Context = Union[Tuple, Any, None]
"""Context passed around from setup to test"""

ExpOutput = Union[Tuple, Any]
"""Expected Output may be a Tuple or a primitive.
This is what the `expected` function should return."""

ActualOutput = Union[Tuple, Any, None]
"""Actual output may also be None, if only print statements
were used and no return statement was used."""

PrintCallback = Optional[Callable]
"""Optional function to populate the simulated standard
output stream."""

Snippet = Callable[[PrintCallback], ActualOutput]
"""The snippet that should be returned from the closure.
This will be injected verbatim into documentation."""

SupportedAssertions = Literal[
    'assertEqual',
    'assertNotEqual'
]
"""Supported unittest assertion functions."""

SnippetLinesCollection = Dict[str, List[str]]
"""Intermediate Snippet Collection used by the parser"""

SnippetsCollection = Dict[str, str]
"""Snippet Collection returned by the parser"""
