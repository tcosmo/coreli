import unittest
from coreli import *

class TestRoutines(unittest.TestCase):
    def test_T(self):
        self.assertEqual(T(3),5) 
        self.assertEqual(T(5),8) 

class TestParvec(unittest.TestCase):
    def test_parvec(self):
        pv = Parvec([0,1,1,0,1])
        self.assertRaises(ValueError, lambda: Parvec([0,1,2,0,1]))
        self.assertEqual(pv.norm, 5)
        self.assertEqual(pv.span,3)