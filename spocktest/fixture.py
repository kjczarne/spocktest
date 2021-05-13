import unittest
from typing import Any, Callable, Tuple, Type, List, NewType, Union, Optional
from spocktest.model import Context, ExpOutput, Snippet, SupportedAssertions


def replacement_print():
    stream_replacement_list = []
    def closure(*args):
        stream_replacement_list.extend(args)
    return stream_replacement_list, closure


class _Test(unittest.TestCase):
    """Fixture type that accepts the snippet
    along with setup and teardown code and
    a function returning expected values."""
    def __init__(
        self, 
        methodName:        str,
        set_up:            Optional[Callable[[], Context]],
        snippet_closure:   Callable[[Context], Snippet],
        expected:          Callable[[], ExpOutput],
        tear_down:         Optional[Callable[[Context], None]],
        assertionFuncName: Optional[SupportedAssertions]
    ) -> None:
        self.set_up = set_up
        self.snippet_closure = snippet_closure
        self.expected = expected
        self.tear_down = tear_down
        # rename the test method after the test snippet:
        self.__setattr__(methodName, self.test)
        super().__init__(methodName=methodName)

    def setUp(self) -> None:
        if self.set_up:
            self.context = self.set_up()
        else:
            self.context = None
    
    def test(self):
        actual_stdout, rprint = replacement_print()
        snippet = self.snippet_closure(self.context)
        actual_return = snippet(rprint)
        # TODO: fix type problems here, add tests for primitives
        actual = actual_stdout if actual_stdout else [] + \
            actual_return if actual_return else []
        exp = self.expected()
        for a, e in zip(actual, exp):
            self.assertEqual(a, e)

    def tearDown(self) -> None:
        self.tear_down(self.context)



def make_test_case(
    snippet_closure:   Callable[[Context], Snippet],
    expected:          Callable[[], ExpOutput],
    assertionFuncName: Optional[SupportedAssertions] = 'assertEqual',
    set_up:            Optional[Callable[[], Context]]     = None,
    tear_down:         Optional[Callable[[Context], None]] = None
) -> _Test:
    """Creates a `unittest.TestCase`-extending class
    which will be responsible for injecting the test
    snippet and the expected output into the testing loop.
    """
    # create the test method name after the test snippet:
    method_name = "test_" + snippet_closure.__name__

    # create the test case instance:
    instance = _Test(
        method_name,
        set_up,
        snippet_closure,
        expected,
        tear_down,
        assertionFuncName
    )

    # rename the class after the test snippet:
    instance.__class__.__name__ = snippet_closure.__name__.title().replace("_", "")
    
    return instance
