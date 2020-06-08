""" This files contains the relevant to construct rational cycles.
"""
from coreli.parity_vectors import *
import cypari

def rational_cycle_solution(compact):
    """ Returns the rational number of which cycle is supported by the\
    given parity vector (if not given in the CompactRep format it will be converted).
    
    The explicit formula for the solution is (see Wirsching):
        x = (\sum_{i=0}^{l(s)-1} 3^{l(s)-1-i}2^{i+s_0+...+s_i})/(2^||s|| - 3^l(s))
        
        
    :Example:
        >>> rational_cycle_solution(Parvec([1]))
        -1

        >>> rational_cycle_solution(Parvec([1,1,0]))
        -5

        >>> rational_cycle_solution(Parvec([1,1,1,1,0,1,1,1,0,0,0]))
        -17

        >>> rational_cycle_solution(Parvec([1,1,0,1,0,0]))
        23/37

        >>> rational_cycle_solution(Parvec([0,0,1,0,0]))
        4/29

        >>> rational_cycle_solution(Parvec([1,1,0,1,1]))
        -85/49

        >>> rational_cycle_solution(Parvec([1,0,0,1,1,1]))
        -179/17
    """
    
    if type(compact) != CompactRep:
        if type(compact) == Parvec:
            compact = compact.to_compact()
        else:
            return
    
    formula_str = "+".join(["3^({})*2^({})".format(compact.span-1-i,i+sum(compact.compact[:i+1])) for i in range(compact.span)])
    formula_str = '(' +formula_str + ')/(2^{}-3^{})'.format(compact.norm, compact.span)
    return cypari.pari(formula_str)