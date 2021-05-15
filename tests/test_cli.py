import unittest
import sys
import os
from pathlib import Path
from spocktest.main import main


class TestCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.expected_doc1 = [
            '# Doc1',
            '',
            '```python',
            'a = 1',
            'a += 1',
            '```',
            '',
            '```python',
            'c = 3',
            'c += 3',
            '```'
        ]

        cls.expected_doc2 = [
            '# Doc2',
            '',
            '```python',
            'b = 2',
            'b += 2',
            '```',
            '',
            '```python',
            'd = 4',
            'd += 4',
            '```'
        ]

        cls.test_path = \
            os.path.join(
                os.path.dirname(__file__),
                'integration',
                'test'
            )

        cls.doc_path = \
            os.path.join(
                os.path.dirname(__file__),
                'integration',
                'doc'
            )

        cls.output_path = \
            os.path.join(
                os.path.dirname(__file__),
                'integration',
                'output'
            )

    def test_cli(self):
        sys.argv = [
            'spocktest',
            self.test_path,
            self.doc_path,
            '-o',
            self.output_path
        ]

        main()

        with open(Path(self.output_path) / 'sub1' / 'doc1.md', 'r') as f:
            actual_doc1 = f.read().splitlines()
        with open(Path(self.output_path) / 'sub2' / 'doc2.md', 'r') as f:
            actual_doc2 = f.read().splitlines()
        
        self.assertListEqual(self.expected_doc1, actual_doc1)
        self.assertListEqual(self.expected_doc2, actual_doc2)


if __name__ == "__main__":
    unittest.main()
