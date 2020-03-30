import unittest
from coreli import *


class TestRoutines(unittest.TestCase):

    def test_T(self):
        self.assertEqual(T(3),5) 
        self.assertEqual(T(5),8) 
