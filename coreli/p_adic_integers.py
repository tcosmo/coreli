"""
Implementing p-adic integers.

    References
    ========== 

    [1] Computations with p-adic numbers. Xavier Caruso. Preprint, 2017.
        https://arxiv.org/abs/1701.06794
"""

from typing import Callable, List, Union
from coreli.utils import list_int_to_list_str, to_base_b

ZERO_DIGIT_FUNCTION = lambda n: 0


class PadicInt(object):
    def __init__(
        self,
        p: int,
        digit_function: Callable[[int], int] = ZERO_DIGIT_FUNCTION,
    ):
        """Constructs a p-adic integer.
        Args:
                p (int): digits of the number are in 0 ... p-1
                digit_function (Callable[[int], int]): function that gives the nth digit of the number

        """
        self.p: int = p
        self.digit_function: Callable[[int], int] = digit_function

    @staticmethod
    def from_int(p: int, x: int) -> "PadicInt":
        """Constructs a p-adic integer from an integer.

        Note: have to use str() in below example because of bug in python doctest with '...' in output.
        :Example:
        >>> str(PadicInt.from_int(2,25))
        '...0000011001'
        >>> str(PadicInt.from_int(2,-4))
        '...1111111100'
        >>> str(PadicInt.from_int(3,-10))
        '...2222222122'
        """

        digits = to_base_b(abs(x), p, False)
        if x >= 0:
            digit_function = lambda n: 0 if n >= len(digits) else digits[n]
            return PadicInt(p, digit_function)

        new_digits = [p - d - 1 for d in digits]

        digit_function = lambda n: p - 1 if n >= len(digits) else new_digits[n]

        return PadicInt(p, digit_function) + 1

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
        return self.to_str(10)

    def __repr__(self) -> str:
        return str(self)

    # TODO: optimise (memoise sum,carry) and test
    def __add__(self, other: Union["PadicInt", int]) -> "PadicInt":
        """Computes p-adic addition."""

        # Convert to p-adic if given an int
        if isinstance(other, int):
            other = PadicInt.from_int(self.p, other)

        if self.p != other.p:
            raise ValueError(
                f"Cannot add p-adic integers with different p: {self.p} {other.p}"
            )

        def addition_digit_function(n: int) -> int:
            carry = 0
            if n > 0:
                _, carry = addition_digit_function(n - 1)

            sum_ = self.digit_function(n) + other.digit_function(n) + carry
            new_carry = sum_ // self.p

            return sum_ % self.p, new_carry

        return PadicInt(self.p, lambda n: addition_digit_function(n)[0])
