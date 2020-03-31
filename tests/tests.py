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
        tree = SpanPredRegularTree(8,3)
        print()
        tree.pprint_branches(print_root_once=True)

        tree = SpanPredRegularTree(8,0)
        print()
        tree.pprint_branches(print_root_once=True)

    def test_nb_branches(self):
        tree = SpanPredRegularTree(8,3)
        tree.extract_branches()
        self.assertEqual(tree.nb_branches, len(tree.branches))

        tree2 = SpanPredRegularTree(13,5)
        tree2.extract_branches()
        self.assertEqual(tree2.nb_branches, len(tree2.branches))

        tree2 = SpanPredRegularTree(3,3)
        tree2.extract_branches()
        self.assertEqual(tree2.nb_branches, len(tree2.branches))
