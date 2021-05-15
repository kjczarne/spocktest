import unittest


class Test1(unittest.TestCase):

    def test_snippet_1(self):
        a = 1
        a += 1
        # SNIPPET_END
        self.assertEqual(a, 2)
