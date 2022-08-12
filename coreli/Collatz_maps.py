""" Collatz maps definitions.

    References
    ========== 
    
    [1] The Ultimate Challenge: The 3x+1 Problem, Edited by Jeffrey C. Lagarias. American Mathematical Society, Providence RI 2010, pp. 3--29
        https://arxiv.org/abs/2111.02635
"""


def C(x: int) -> int:
    """The Collatz map.

    :Example:
        >>> C(2)
        1
        >>> C(3)
        10
    """
    if x % 2 == 0:
        return x // 2
    return 3 * x + 1


def T(x: int) -> int:
    """The Collatz map, slightly accelerated.

    :Example:
        >>> T(2)
        1
        >>> T(3)
        5
    """
    if x % 2 == 0:
        return x // 2
    return (3 * x + 1) // 2
