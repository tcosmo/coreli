""" Collatz maps definitions.

    References
    ========== 
    
    [1] The Ultimate Challenge: The 3x+1 Problem, Edited by Jeffrey C. Lagarias. American Mathematical Society, Providence RI 2010, pp. 3--29
        https://arxiv.org/abs/2111.02635
"""
from typing import Union
from coreli.padic_integers import PadicInt
from sympy import Rational


def C(x: Union[int, Rational, PadicInt]) -> Union[int, Rational, PadicInt]:
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
        >>> from coreli.padic_integers import Padic
        >>> Z2 = Padic(2)
        >>> minus_one_third = Z2(digit_function = lambda n: (n+1)%2)
        >>> C(minus_one_third).to_str()
        '...0000000000'
        >>> from coreli.utils import iterate
        >>> some_2_adic = Z2(digit_function = lambda n: iterate(C,n,n)%2)
        >>> C(some_2_adic).to_str(20)
        '...00001000100001010000'
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
        if x.digit_function(0) == 0:
            return x >> 1
        return (
            x + x + x + 1
        )  # addition algorithm more efficient than multiplication


def T(x: int) -> Union[int, Rational, PadicInt]:
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
        >>> from coreli.padic_integers import Padic
        >>> Z2 = Padic(2)
        >>> minus_one_third = Z2(digit_function = lambda n: (n+1)%2)
        >>> T(minus_one_third).to_str()
        '...0000000000'
        >>> from sympy.ntheory.primetest import is_square
        >>> some_2_adic = Z2(digit_function = lambda n: int(is_square(n)))
        >>> some_2_adic.to_str(40)
        '...0001000000000010000000010000001000010011'
        >>> T(some_2_adic).to_str(40)
        '...0001100000000011000000011000001100011101'
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
        if x.digit_function(0) == 0:
            return x >> 1
        return (
            x + x + x + 1
        ) >> 1  # addition algorithm more efficient than multiplication
