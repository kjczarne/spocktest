import unittest


class Test4(unittest.TestCase):

    def test_snippet_4(self):
        d = 4
        d += 4
        # SNIPPET_END
        self.assertEqual(d, 4)
