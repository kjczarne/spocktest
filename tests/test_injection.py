import os
import unittest
import textwrap
from spocktest.inject import inject


class TestInjection(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.snippets = {
            'test_inject1': 'a = 1',
            'test_inject2': 'b = 2\nc = 3'
        }

    def test_injection(self):
        actual = inject(
            os.path.join(
                os.path.dirname(__file__),
                'res'
                # ,
                # 'inject.md'
            ),
            r'# --Snippet--: {{ID}}',
            self.snippets,
            debug=True
        ).splitlines()
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
