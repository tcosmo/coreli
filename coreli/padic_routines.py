""" This fine contains all the routines related 
to p-adic numbers. In particular it contains the extension
of the Collatz process to Z_2.
"""
import cypari
from coreli.routines import *

def rational_p_adic_to_Q(p, initial_segment, period):
    """ Converts a periodic p-adic expansion in the corresponding irreducible fraction in Q.
    
    :Example:
        >>> rational_p_adic_to_Q(2,'101','1')
        -3
        
        >>> rational_p_adic_to_Q(2,'1','10')
        1/3
        
        >>> rational_p_adic_to_Q(2,'101','')
        5
        
        >>> rational_p_adic_to_Q(3,'2','1')
        1/2  
    """
    
    if len(period) == 0:
        period = '0'
    
    value_initial_segment = int(initial_segment[::-1], p)
    value_period = int(period[::-1],p)
    
    padic_fraction = "1/(1-{}^{})".format(p,len(period))
    
    formula_str = "{} + {}^({})*({})*({})".format(value_initial_segment,p,len(initial_segment),
                                                 value_period,padic_fraction)
    return cypari.pari(formula_str)
    
def Collatz_rational_2_adic(segment_init, period):
    """ Returns the Collatz sequence (until cycle) of the rational 2-adic number 
    given by its initial segment and period. The function also returns the closest
    element to 0 in the cycle that is reached.

    :Example:
        >>> Collatz_rational_2_adic('1','10')
        ([1/3, 1, 2, 1], 1)

        >>> Collatz_rational_2_adic('01','01')
        ([-2/3, -1/3, 0, 0], 0)

        >>> Collatz_rational_2_adic('0111','01')
        ([10/3, 5/3, 3, 5, 8, 4, 2, 1, 2], 1)

        >>> Collatz_rational_2_adic('1','011')
        ([-5/7, -4/7, -2/7, -1/7, 2/7, 1/7, 5/7, 11/7, 20/7, 10/7, 5/7], 5/7)

        >>> Collatz_rational_2_adic('1011','1')
        ([-3, -4, -2, -1, -1], -1)

        >>> Collatz_rational_2_adic('101101','1')
        ([-19, -28, -14, -7, -10, -5, -7], -5)
    """
    rational_2adic = rational_p_adic_to_Q(2,segment_init,period)
    CollatzSeq = [rational_2adic]
    seen = {}
    while True:
        numerator = cypari.pari('numerator({})'.format(rational_2adic))

        # Cannot just call T_0 and T_1 because
        # `cypari` doesnt like the fact that they use
        # // instead of /
        if numerator%2 == 0:
            rational_2adic = rational_2adic/2
        else:
            rational_2adic = (3*rational_2adic+1)/2
        CollatzSeq.append(rational_2adic)
        if rational_2adic in seen:
            period = []
            record = False
            for element in CollatzSeq:
                if element == rational_2adic:
                    record = True
                if record:
                    period.append(element)
            sign = 1 if min(period) >= 0 else -1
            return CollatzSeq,sign*min(map(abs,period))
        
        seen[rational_2adic] = True