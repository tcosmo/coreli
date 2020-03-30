from typing import List, Callable

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
    return x//2 if x%2 == 0 else (3*x+1)//2

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