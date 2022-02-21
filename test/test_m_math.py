import unittest

from m_math import add_function


class TestCase(unittest.TestCase):
    def test_add_1_2(self):
        s = add_function(1, 2)
        self.assertTrue(s == 3)
    
    def test_add_1_2_3(self):
        s = add_function(1, 2, 3)
        self.assertTrue(s == 6)


