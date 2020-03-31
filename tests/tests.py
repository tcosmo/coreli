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

    def test_to_compact(self):
        pvs = Parvec.get_random_parvec(100,100)
        for pv in pvs:
            compact = pv.to_compact()
            self.assertListEqual(pv.parvec, compact.to_parvec().parvec)
            self.assertEqual(pv.norm,compact.norm)
            self.assertEqual(pv.span,compact.span)

    def test_to_parvec(self):
        compacts = CompactRep.get_random_compact(100,100)
        for compact in compacts:
            pv = compact.to_parvec()
            self.assertListEqual(compact.compact, pv.to_compact().compact)
            self.assertEqual(pv.norm,compact.norm)
            self.assertEqual(pv.span,compact.span)

class TestBaseConversion(unittest.TestCase):
    def test_int_to_binary(self):
        self.assertEqual(int_to_binary(3), '11')
        self.assertEqual(int_to_binary(3,5), '00011')
        self.assertRaises(ValueError, lambda: int_to_binary(3,1))


class TestPredecessors(unittest.TestCase):
    def test_construct_tree(self):
        to_test = [(8,3), (8,2), (8,4), (13,5), (25,2), (13,2), (3,4)]
        for x,k in to_test:
            tree = SpanPredRegularTree(x,k)
            where_to_stop = x//(3**k)
            random_samples = tree.get_random_samples(10)
            for sample in random_samples:
                if sample == '':
                    continue
                self.assertEqual(CS_bin(sample)[-1-where_to_stop], 
                                 int_to_binary(x))

    def test_nb_branches(self):
        to_test = [(8,3), (13,5), (3,3)]
        for x,k in to_test:
            tree = SpanPredRegularTree(x,k)
            tree.extract_branches()
            self.assertEqual(tree.nb_branches, len(tree.branches))
