import unittest
from src import __version__

class TestVersion(unittest.TestCase):
    def test_version_matches_file(self):
        with open('VERSION') as vf:
            file_version = vf.read().strip()
        self.assertEqual(__version__, file_version)

if __name__ == '__main__':
    unittest.main()
