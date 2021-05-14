import unittest
import textwrap
from spocktest.extract import get_snippet_code
from spocktest.defaults import SNIPPET_END, SNIPPET_ID


class TestGetSnippetCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.line_markers_finish = [
            SNIPPET_END
        ]
        cls.ex1 = textwrap.dedent(
            """
            def test_snippet_some(print):
                # This should appear in the snippet code
                a = 1
                b = 2
                a != b  # True
                # SNIPPET_END
            
            def test_snippet_another(print):
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
                SNIPPET_ID,
                f
            )
            expected = {
                'some': '# This should appear in the snippet ' + \
                    'code\na = 1\nb = 2\na != b  # True', 
                'another': '# This should also appear in docs' + \
                    '\nc = 3\nprint(c)'
            }
            self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
