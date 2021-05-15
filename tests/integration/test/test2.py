import unittest


class Test2(unittest.TestCase):

    def test_snippet_2(self):
        b = 2
        b += 2
        # SNIPPET_END
        self.assertEqual(b, 4)
