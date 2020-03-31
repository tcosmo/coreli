""" This file contains the relevant tools to study predecessor sets in the Collatz graph.\
    In particular, it is proven in `https://arxiv.org/abs/1907.00775 <https://arxiv.org/abs/1907.00775>`_\
    that these sets can be partionned in **Regular Languages**.\
    We provide the tools to construct the associated regular expressions.
"""
import random
import enum
import copy
from typing import List, Callable, Tuple
from coreli.base_conversion_routines import *
from coreli.modular_routines import *

class SpanPredNodeType(enum.Enum):
    """ Each node in the regular expression tree has one these types.\
        More details in `https://arxiv.org/abs/1907.00775 <https://arxiv.org/abs/1907.00775>`_.
    """
    EMPTY = 0
    INITIAL_SEGMENT = 1
    KLEENE = 2
    JOIN = 3
    BIT = 4

class SpanPredNode(object):
    """ A node in the `SpanPredRegularTree`
    """
    def __init__(self, node_type: 'SpanPredNodeType', annotation: Tuple[int],
                       str_value: str, children: List['SpanPredNode']) -> None:
        """Construct a node of the Span Regular Expression tree.
            Args:
                node_type (SpanPredNodeType): which information is the node encoding
                annotation (Tuple[int]): extra information related to the construction,
                contains at least the `x` and `k` for which the node was constructed
                str_value (str): the bit string retained by the node
                children (List[SpanPredNode]): list of the node's children
        """
        self.node_type = node_type
        self.annotation = annotation
        self.str_value = str_value
        self.children = children

    def copy_without_children(self) -> 'SpanPredNode':
        """ It can be useful to copy all the information of a node but\
            its children."""
        return SpanPredNode(self.node_type,self.annotation,self.str_value,[])

    @classmethod
    def chain_link(cls, chain: 'SpanPredNode') -> 'SpanPredNode':
        """ Links a chain of `SpanPredNode`.
        """
        def construct_root(i):
            if i == len(chain)-1:
                return chain[-1]
            to_return = chain[i].copy_without_children()
            to_return.children = [construct_root(i+1)]
            return to_return
        
        return construct_root(0) 

    def sample_chain(self, kleene_choice: Tuple[int]) -> str:
        """ Sample a regular expression chain tree using Kleene star\
            as per number given by `kleene_choice`.
        """
        current_sample = ''
        new_kleene_choice = kleene_choice
        if self.node_type == SpanPredNodeType.KLEENE:
            if len(kleene_choice) == 0:
                raise ValueError('There are more Kleene star in {}'.format(self.simpler_str())\
                                  +'than given by `kleene_choice`')
            current_choice = kleene_choice[0]
            current_sample += self.str_value*current_choice
            new_kleene_choice = kleene_choice[1:]
        else:
            current_sample += self.str_value
        
        if len(self.children) == 0:
            return current_sample

        if len(self.children) > 1:
            raise ValueError('Can only operate on a chain tree. If you have a'\
                              +'non chain tree please operate on branches.')

        return current_sample + self.children[0].sample_chain(new_kleene_choice)

    def __str__(self):
        
        if self.node_type == SpanPredNodeType.EMPTY:
            return ''
        me = '({})'.format(self.str_value)
        
        if self.node_type == SpanPredNodeType.KLEENE:
            me += '*'
        
        if len(self.children) == 0:
            return me

        if len(self.children) == 1:
            me += str(self.children[0])
            return me
        
        me += '('
        for i,child in enumerate(self.children):
            me += '('+str(child)+')'
            if i != len(self.children)-1:
                me +='|'
        me += ')'
        return me

    def simpler_str(self, only_me: bool = False) -> str:
        """ Returns a less pedantic str than __str__.
            If `only_me` is set, the children wont be appended.
        """
        if self.node_type == SpanPredNodeType.EMPTY:
            return 'Empty'
        
        if self.node_type == SpanPredNodeType.KLEENE:
            me = '({})*'.format(self.str_value)
        else:
            me = '{}'.format(self.str_value)

        if len(self.children) == 0 or only_me:
            return me
        
        if len(self.children) == 1:
            me += self.children[0].simpler_str()
            return me
        
        me += '('
        for i,child in enumerate(self.children):
            me += str(child)
            if i != len(self.children)-1:
                me +='|'
        me += ')'
        return me

class SpanPredRegularTree(object):
    """ The set of predecessors of :math:`x` at "span-distance" :math:`k`\
        (i.e. any :math:`y` that goes to `x` following a parity vector of span `k`)\
        is a Regular Language. The associate Regular Expression is a tree and this class\
        constructs it.
    """
    def __init__(self, x: int, k: int):
        """ We are computing the expression of the predecessors of :math:`x` at\
            "span-distance" distance :math:`k`."""
        self.x = x
        self.k = k
        self.branches = None
        self.root = self.construct_tree()

    @staticmethod
    def get_nb_branches(k: int) -> int:
        """ The number of branches of the tree only depends on k and is 
            given by a closed formula.
        """
        return 2**(k-1)*3**((k*(k-3)+2)//2)

    @property
    def nb_branches(self) -> int:
        """ Instance wrapper around `get_nb_branches`. """
        if self.x %3 == 0:
            return 1 #Tree is 'Empty' which gives 1 branch instead of 0 awkwardly enough
        return self.get_nb_branches(self.k)

    @staticmethod
    def parity_string(x: int, y: int, k: int, n_cycle: int = 0) -> str:
        """ For :math:`x` and :math:`y`, elements of Z/3^kZ the function computes\
            the parities of all elements of the form\
            :math:`2^{-i}*x` until :math:`y` is reached `n_cycle+1` times (excluded).
        """
        if (x%3)*(y%3) == 0:
            raise ValueError('{} or {} is a multiple of three!'.format(x,y))
        if x >= 3**k or y >= 3**k:
            raise ValueError('{} or {} is not in Z/3^{}Z'.format(x,y,k))

        parity_str = ''
        curr_cycle = 0
        x_0 = x

        while not (x == y and curr_cycle == n_cycle):
            parity_str += str(x%2)
            x = mul_inv2(x,k)
            if x == x_0:
                curr_cycle += 1

        return parity_str[::-1]#encodings reverse the order

    def construct_tree(self) -> 'SpanPredNode':
        """ Constructs the regular expression tree, it follows the construction\
            of Th. 4.16 in `https://arxiv.org/abs/1907.00775 <https://arxiv.org/abs/1907.00775>`_."""
        x,k = self.x, self.k
        if k == 0:
            str_value = '0'
            node0 = SpanPredNode(SpanPredNodeType.KLEENE, 
                                 (0, 0), str_value, [])
            if x == 0:
                return node0
            else:
                node = SpanPredNode(SpanPredNodeType.INITIAL_SEGMENT, 
                                    (x, 0), int_to_binary(x), [node0])
            return node

        if x%3 == 0:
            ''' The predecessor set of a multiple of 3, when k!=0 is empty'''
            node = SpanPredNode(SpanPredNodeType.EMPTY, 
                                (x, k),
                                '', [])
            return node

        if x >= 3**k:
            tree_below = SpanPredRegularTree(x%(3**k),k).root
            return SpanPredNode(SpanPredNodeType.INITIAL_SEGMENT, 
                                (x, k),
                                int_to_binary(x//(3**k)), [tree_below])

        children_nodes = []
        group_k = enumerate_group_k(k-1)
        for y in group_k:
            tree_below = SpanPredRegularTree(y,k-1).root

            bit_node = SpanPredNode(SpanPredNodeType.BIT,
                        (x,k,y),
                        str(1-y%2), [tree_below])

            join_node = SpanPredNode(SpanPredNodeType.JOIN,
            (x,k,T1_k(y,k)), SpanPredRegularTree.parity_string(T1_k(y,k),x,k), 
            [bit_node])

            children_nodes.append(join_node)
        
        kleene_node = SpanPredNode(SpanPredNodeType.KLEENE,
        (x,k), SpanPredRegularTree.parity_string(x,x,k,1), children_nodes)

        return kleene_node


    def get_random_samples(self, n_samples:int = 1, max_kleene:int = 3) -> str:
        """ Returns random samples of strings matching the tree's regexp.
        
            Args:
                n_samples (int): number of samples to generate
                max_kleene (int): number of maximum application of kleene star
                in samples
        """
        to_return = []
        self.extract_branches()

        for _ in range(n_samples):
            i_branch = random.randint(0,self.nb_branches-1)
            kleene_choice = tuple(random.randint(0,max_kleene) for _ in range(self.k+1))
            to_return.append(self.branches[i_branch].sample_chain(kleene_choice))

        return to_return

    def extract_branches(self) -> None:
        """ Return the list of all the tree's branches.
        """
        if not self.branches is None:
            return
        self.branches = []
        def explore_branch(curr_node: 'SpanPredNode', 
                           curr_branch: List['SpanPredNode']) -> None:
            if len(curr_node.children) == 0:
                to_link = curr_branch + [curr_node]
                self.branches.append(SpanPredNode.chain_link(to_link))
                return

            for child in curr_node.children:
                curr_node_mod = curr_node.copy_without_children()
                explore_branch(child, curr_branch + [curr_node_mod])
        
        explore_branch(self.root, [])

    def pprint_branches(self, print_root_once: bool = False,
                              print_in_custom_order: bool = True) -> None:
        """ Pretty prints all the branches of the tree. 

            Args:
                print_root_once (bool): all branches starts with the same root\
                if set to true, the root will be printed only once to avoid\
                redundancy.
                print_in_custom_order (bool): The order in which the branches where\
                computed is not necessarily the most convenient to work with. There is\
                a custom order which is simpler to read and this boolean implements it.
        """
        self.extract_branches()

        if print_root_once:
            print(self.branches[0].simpler_str(only_me=True))
            print()
        
        if self.branches[0].node_type == SpanPredNodeType.EMPTY:
            return

        if not print_in_custom_order:
            for branch in self.branches:
                if not print_root_once:
                    print(branch.simpler_str())
                else:
                    print(branch.children[0].simpler_str())
            return

        nb_branches_inferior = self.get_nb_branches(self.k-1)
        nb_elem_per_block = self.nb_branches//nb_branches_inferior

        for i_block in range(nb_branches_inferior):
            for j_elem in range(nb_elem_per_block):
                branch = self.branches[j_elem*nb_branches_inferior + i_block]
                if not print_root_once:
                    print(branch.simpler_str())
                else:
                    print(branch.children[0].simpler_str())
            print()

    def __str__(self):
        return str(self.root)