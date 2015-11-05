import unittest
from timer import secToString


class TestTimer(unittest.TestCase):
    def test_secToString(self):
        str = secToString(10)
