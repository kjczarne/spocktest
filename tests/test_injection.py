import os
import unittest
import textwrap
from spocktest.inject import inject
from spocktest.defaults import SNIPPET_INJECT
from spocktest.state import STATE


class TestInjection(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.snippets = {
            'test_inject1': 'a = 1',
            'test_inject2': 'b = 2\nc = 3'
        }

    def test_injection(self):
        # we reset the state first to prevent any clobbering
        # coming from other tests:
        STATE.reset()

        inject(
            os.path.join(
                os.path.dirname(__file__),
                'res'
            ),
            SNIPPET_INJECT,
            self.snippets,
            debug=True
        )

        actual = STATE.debug_container[0].splitlines()
        expected = [
            "# Sample documentation",
            "",
            "## Sample subsection",
            "",
            "```python",
            "a = 1",
            "```",
            "",
            "```python",
            "b = 2",
            "c = 3",
            "```"
        ]
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
