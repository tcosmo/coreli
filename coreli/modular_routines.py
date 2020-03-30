""" Contains the Collatz routines needed when working in Z/3^kZ.
"""

def inv2(k:int) -> int:
    """ Return the inverse of 2 in :math:`\mathbb{Z}/3^k \mathbb{Z}`. \
        The element 2 can always be inverted in :math:`\mathbb{Z}/3^k \mathbb{Z}`. \
        It means for all :math:`k` there exists :math:`y\in\mathbb{Z}/3^k \mathbb{Z}` \
        such that :math:`2y = 1`. The value of :math:`y` is given by the formula :math:`\\frac{3^k+1}{2}`. 

    :Example:
        >>> inv2(2)
        5
        >>> inv2(3)
        14
    """
    return (3**k + 1)//2

def T0_k(x: int, k: int) -> int:
    """Computes the operation :math:`2^{-1}x` in :math:`\mathbb{Z}/3^k \mathbb{Z}`. 
    
    :Example:
        >>> T0_k(8,3)
        4
        >>> T0_k(7,3)
        17
    """
    return (inv2(k)*x)%(3**k)

def T1_k(x:int, k: int) -> int:
    """Computes the operation :math:`2^{-1}(3x+1)` in :math:`\mathbb{Z}/3^k \mathbb{Z}`. 
    
    :Example:
        >>> T1_k(5,3)
        8
        >>> T1_k(6,3)
        23
    """
    return (inv2(k)*(3*x+1))%(3**k)

def T_modular(action:int, k:int, x:int) -> int:
    """ Computes T0_k or T1_k depending on the value of `action` (0 or 1).
    """
    return T0_k(x,k) if action == 0 else T1_k(x,k)