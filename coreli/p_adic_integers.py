"""
Implementing p-adic integers.

    References
    ========== 

    [1] Computations with p-adic numbers. Xavier Caruso. Preprint, 2017.
        https://arxiv.org/abs/1701.06794
"""

from typing import Callable, List, Union
import functools
from sympy import Rational
from coreli.utils import list_int_to_list_str, int_to_base


class Padic(object):
    """Wrapper around p-adic integers with p fixed, i.e. it represents the ring Z_p.
    Note that p does not need to be prime for Z_p(+,x) to be defined but Z_p is a field iff p is prime.

    :Example:
    >>> Z2 = Padic(2)
    >>> Z2.from_int(25).to_str(10)
    '...0000011001'
    >>> x = Z2(digit_function = lambda n: n%2)
    >>> x.to_str(10)
    '...1010101010'
    """

    def __init__(self, p: int):
        self.p = p

    def __call__(self, digit_function: Callable[[int], int]):
        return PadicInt(self.p, digit_function)

    def from_int(self, x: int) -> "PadicInt":
        """Constructs a p-adic integer from an integer x. The n-th digit is f^n(x) mod p,
        with f the Collatz-like map f(x) = (x-i)/p if x = i mod p.

        :Example:
        >>> Z2 = Padic(2)
        >>> Z2.from_int(25).to_str(10)
        '...0000011001'
        >>> Z2.from_int(-4).to_str(20)
        '...11111111111111111100'
        >>> Z3 = Padic(3)
        >>> Z3.from_int(-10).to_str(10)
        '...2222222122'
        """

        def digit_function(n):
            @functools.lru_cache
            def digit_function_aux(n):
                if n == 0:
                    return x
                previous_iterate = digit_function_aux(n - 1)
                return previous_iterate // self.p

            return digit_function_aux(n) % self.p

        return PadicInt(self.p, digit_function, underlying_rational=x)


class PadicInt(object):
    default_str_precision = 10  # Default number of digits used by __str__

    def __init__(
        self,
        p: int,
        digit_function: Callable[[int], int] = lambda n: 0,
        underlying_rational: Union[None, int, Rational] = None,
    ):
        """Constructs a p-adic integer, i.e. a base-p string that is infinite on the most signficant side,
        p does not need to be prime (see docstring of class Padic).

        Args:
                p (int): digits of the number are in 0 ... p-1
                digit_function (Callable[[int], int]): function that gives the nth digit of the number
                underlying_rational (Union[None, int, Rational]): if this p-adic integer comes from a rational,
                    this  hint will allow to keep track of that rational along operations applied on the number.
                    This is automatically set by factories such as Padic.from_int / Padic.from_rational.

        """
        self.p: int = p
        self.digit_function: Callable[[int], int] = digit_function
        self.underlying_rational: Union[
            None, int, Rational
        ] = underlying_rational

    def digits(self, n: int) -> List[int]:
        """Returns the first n digits of the number. Raises a value error if a digit is >= p."""
        digits = [self.digit_function(i) for i in range(n)]
        if len(list(filter(lambda d: d >= self.p, digits))) > 0:
            raise ValueError(
                f"{self.p}-adic integer ...{digits} contains digit(s) >= {self.p}"
            )
        return digits

    def to_str(self, n: int) -> str:
        """Give the first n digits as a string. The least significant digit is on the right."""
        digits = list_int_to_list_str(self.digits(n))
        return "..." + "".join(digits[::-1])

    def __str__(self) -> str:
        """By default, we show 10 digits."""
        return self.to_str(self.default_str_precision)

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: Union["PadicInt", int]) -> "PadicInt":
        """Computes p-adic addition.

        :Example:
        >>> Z2 = Padic(2)
        >>> x = Z2.from_int(25)
        >>> y = Z2.from_int(47)
        >>> (x + y).to_str(10)
        '...0001001000'
        >>> z = Z2(digit_function = lambda n: n%2)
        >>> (z + z + x).to_str(20)
        '...01010101010101101101'

        """

        # Convert to p-adic if given an int
        if isinstance(other, int):
            other = Padic(self.p).from_int(other)

        if self.p != other.p:
            raise ValueError(
                f"Cannot add p-adic integers with different p: {self.p} {other.p}"
            )

        @functools.lru_cache
        def addition_digit_function(n: int) -> int:
            carry = 0
            if n > 0:
                _, carry = addition_digit_function(n - 1)

            sum_ = self.digit_function(n) + other.digit_function(n) + carry
            new_carry = sum_ // self.p

            return sum_ % self.p, new_carry

        # Updating the underlying rational if it is set for both operands
        underlying_rational = None
        if None not in (self.underlying_rational, other.underlying_rational):
            underlying_rational = (
                self.underlying_rational + other.underlying_rational
            )

        if (
            self.underlying_rational is not None
            and other.underlying_rational is not None
        ):
            underlying_rational = (
                self.underlying_rational + other.underlying_rational
            )
        return PadicInt(
            self.p,
            lambda n: addition_digit_function(n)[0],
            underlying_rational=underlying_rational,
        )
