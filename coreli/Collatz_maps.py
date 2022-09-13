""" Collatz maps definitions.

    References
    ========== 
    
    [1] The Ultimate Challenge: The 3x+1 Problem, Edited by Jeffrey C. Lagarias. American Mathematical Society, Providence RI 2010, pp. 3--29
        https://arxiv.org/abs/2111.02635
"""
from typing import Union
from coreli.p_adic_integers import PadicInt
from sympy import Rational


def C(x: Union[int, Rational, PadicInt]) -> int:
    """The Collatz map, defined on ints, rational with odd denominator and 2-adic integers.

    References
    ==========

    [1] Jeffrey C. Lagarias. “The 3x + 1 Problem and Its Generalizations”. In: The American Mathe-
        matical Monthly 92.1 (1985), pp. 3-23. issn: 00029890, 19300972.
        url: http://www.jstor.org/stable/2322189.

    :Example:
        >>> C(2)
        1
        >>> C(3)
        10
        >>> C(Rational(-2,23))
        -1/23
        >>> C(Rational(-1,23))
        20/23
    """

    if isinstance(x, int):
        if x % 2 == 0:
            return x // 2
        return 3 * x + 1

    if isinstance(x, Rational):
        if x.denominator % 2 == 0:
            raise ValueError(
                f"Can only run the Collatz map on rational with odd denominator: {x} does not comply"
            )
        if x.numerator % 2 == 0:
            return x / 2
        return 3 * x + 1

    if isinstance(x, PadicInt):
        if x.p != 2:
            raise ValueError(
                f"Can only run the Collatz map on 2-adic integers: input is {x.p}-adic does not comply"
            )
        raise NotImplementedError


def T(x: int) -> int:
    """The Collatz map, slightly accelerated, defined on ints, rational with odd denominator and 2-adic integers.

    References
    ==========

    [1] Jeffrey C. Lagarias. “The 3x + 1 Problem and Its Generalizations”. In: The American Mathe-
        matical Monthly 92.1 (1985), pp. 3-23. issn: 00029890, 19300972.
        url: http://www.jstor.org/stable/2322189..

    :Example:
        >>> T(2)
        1
        >>> T(3)
        5
        >>> T(Rational(-2,23))
        -1/23
        >>> T(Rational(-1,23))
        10/23
    """
    if isinstance(x, int):
        if x % 2 == 0:
            return x // 2
        return (3 * x + 1) // 2

    if isinstance(x, Rational):
        if x.denominator % 2 == 0:
            raise ValueError(
                f"Can only run the Collatz map on rational with odd denominator: {x} does not comply"
            )
        if x.numerator % 2 == 0:
            return x / 2
        return (3 * x + 1) / 2

    if isinstance(x, PadicInt):
        if x.p != 2:
            raise ValueError(
                f"Can only run the Collatz map on 2-adic integers: input is {x.p}-adic does not comply"
            )
        raise NotImplementedError
