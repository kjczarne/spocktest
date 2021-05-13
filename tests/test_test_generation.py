from typing import Callable
import unittest
from spocktest.fixture import make_test_case
from spocktest.model import Context, PrintCallback

def snippet_closure_print(context: Context):
    def snippet_print(print: PrintCallback):
        # this would be placed in the documentation
        print(1 + 2)
    return snippet_print

def snippet_closure_return(context: Context):
    def snippet_return(print: PrintCallback):
        return 1 + 2
    return snippet_return


def expected():
    return 3


def expected_failure():
    return 5


class TestTestGeneration(unittest.TestCase):

    def test_test_generation_print(self):
        make_test_case(
            snippet_closure_print,
            expected
        ).run()
    
    def test_test_generation_return(self):
        make_test_case(
            snippet_closure_return,
            expected
        ).run()
    
    def test_test_generation_xfail(self):
        make_test_case(
            snippet_closure_return,
            expected_failure,
            'assertNotEqual'
        ).run()


if __name__ == "__main__":
    unittest.main()
