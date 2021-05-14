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
            expected = textwrap.dedent(
                """
                # This should appear in the snippet code
                a = 1
                b = 2
                a != b  # True
                """
            )
            print(actual)
            # self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
