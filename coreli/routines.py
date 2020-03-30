""" Contains the most fundamental routines needed when working with the Collatz process.
"""

from typing import List, Callable

def T0(x: int) -> int:
    return x//2

def T1(x: int) -> int:
    return (3*x+1)//2

def T(x: int) -> int:
    """The Collatz map. See: https://en.wikipedia.org/wiki/Collatz_conjecture.

    :Example:
        >>> T(3)
        5
        >>> T(5)
        8
        >>> T(8)
        4
    """
    return T0(x) if x%2 == 0 else T1(x)

def CS(x: int, stopping_criterion: Callable[[int,int], bool] = lambda x,n: x == 1) -> List[int]:
    """Compute the Collatz Sequence of integer `x` until a given
    `stopping_criterion` is met.

    Args:
        x (int): Any integer.
        stopping_criterion (Callable[[int,int], bool]): A stopping criterion \
            depending on `x` and on the number of iterations `n`. By default, \
            all steps before 1 is reached are computed: \
                :code:`stopping_criterion = lambda x,n: x == 1`

    Returns:
        List[int]: List of the computed Collatz steps.

    :Example:
        >>> CS(3)
        [3, 5, 8, 4, 2, 1]
    """

    cs = [x]
    n = 0
    while not stopping_criterion(cs[-1],n):
        cs.append(T(cs[-1]))
        n += 1
    return cs

def is_admissible(action: int, x: int) -> bool:
    """ Determine whether the `action` (0 or 1 corresponding to T0 or T1) is feasible\
        for x. T0 is feasible for `x` iff `x` is even and T1 iff `x` is odd. """
    return x%2 == action