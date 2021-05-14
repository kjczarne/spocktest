import unittest
import textwrap
from spocktest.extract import get_snippet_code


class TestGetSnippetCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.line_markers_finish = [
            "# SNIPPET_END"
        ]
        cls.ex1 = textwrap.dedent(
            """
            def some_test_snippet(print):
                # This should appear in the snippet code
                a = 1
                b = 2
                a != b  # True
                # SNIPPET_END
            
            def another_test_snippet(print):
                # This should also appear in docs
                c = 3
                print(c)
                # SNIPPET_END
            """
        )

    def test_get_snippet_code(self):
        for f in self.line_markers_finish:
            actual = get_snippet_code(
                self.ex1, 
                r'(?<=def ){{ID}}(?=\(print\))',
                f
            )
            expected = {
                'some_test_snippet': '# This should appear in the snippet ' + \
                    'code\na = 1\nb = 2\na != b  # True\n# SNIPPET_END\n', 
                'another_test_snippet': '# This should also appear in docs' + \
                    '\nc = 3\nprint(c)\n# SNIPPET_END'
            }
            self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
