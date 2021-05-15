import unittest


class Test3(unittest.TestCase):

    def test_snippet_3(self):
        c = 3
        c += 3
        # SNIPPET_END
        self.assertEqual(c, 3)
