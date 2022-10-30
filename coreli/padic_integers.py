""" Implementing p-adic integers.

    References
    ========== 

    [1] Computations with p-adic numbers. Xavier Caruso. Preprint, 2017.
        https://arxiv.org/abs/1701.06794
"""

from typing import Callable, List, Union, Dict, Tuple
import functools
from sympy import Rational
from math import gcd
from coreli.utils import list_int_to_list_str


class Padic(object):
    """Wrapper around p-adic integers with p fixed, i.e. it represents the ring Z_p.
    Note that p does not need to be prime for Z_p(+,x) to be defined but Z_p is a field iff p is prime.

    :Example:
    >>> Z2 = Padic(2)
    >>> Z2.from_int(25).to_str()
    '...0000011001'
    >>> x = Z2(digit_function = lambda n: n%2)
    >>> x.to_str()
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
        >>> Z2.from_int(25).to_str()
        '...0000011001'
        >>> Z2.from_int(-4).to_str(20)
        '...11111111111111111100'
        >>> Z3 = Padic(3)
        >>> Z3.from_int(-10).to_str()
        '...2222222122'
        """

        def digit_function(n: int) -> int:
            @functools.lru_cache
            def digit_function_aux(n: int) -> int:
                if n == 0:
                    return x
                previous_iterate = digit_function_aux(n - 1)
                return previous_iterate // self.p

            return digit_function_aux(n) % self.p

        return PadicInt(self.p, digit_function, underlying_rational=x)

    def from_rational(self, x: "Rational") -> "PadicInt":
        """Constructs a p-adic integer from a rational x with denominator that is coprime with p. The n-th digit is f^n(x) mod p, with f the Collatz-like map f(x) = (x-i)/p if x = i mod p.

        :Example:
        >>> Z2 = Padic(2)
        >>> Z2.from_rational(Rational(-1,3)).to_str()
        '...0101010101'
        >>> Z2.from_rational(Rational(-1,23)).to_str(20)
        '...00101100100001011001'
        >>> Z3 = Padic(3)
        >>> Z3.from_rational(Rational(77,13)).to_str()
        '...2002002022'
        """

        if gcd(self.p, x.denominator) != 1:
            raise ValueError(
                f"Rational {x} cannot be expressed {self.p}-adically because its denominator is not co-prime with p."
            )

        def digit_function(n: int) -> int:
            @functools.lru_cache
            def digit_function_aux(n: int) -> Rational:
                if n == 0:
                    return x
                previous_iterate = digit_function_aux(n - 1)
                i = previous_iterate.numerator % self.p
                return (previous_iterate - i) / self.p

            return digit_function_aux(n).numerator % self.p

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
        self.digit_function: Callable[[int], int] = functools.lru_cache(
            digit_function
        )
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

    def to_str(self, n: int = default_str_precision) -> str:
        """Give the first n digits as a string. The least significant digit is on the right."""
        digits = list_int_to_list_str(self.digits(n))
        return "..." + "".join(digits[::-1])

    def __str__(self) -> str:
        """By default, we show 10 digits."""
        return self.to_str(self.default_str_precision)

    def __repr__(self) -> str:
        return str(self)

    def __radd__(self, other: Union["PadicInt", int]) -> "PadicInt":
        """This is needed for Python to treat 12 + x (with 12 an int) the same way as x + 12
        (it would raise TypeError error otherwise)
        """
        return self + other

    def __add__(self, other: Union["PadicInt", int]) -> "PadicInt":
        """Computes p-adic addition.

        :Example:
        >>> Z2 = Padic(2)
        >>> x = Z2.from_int(25)
        >>> (47 + x).to_str()
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

    def __rmul__(self, other: Union["PadicInt", int]) -> "PadicInt":
        """This is needed for Python to treat 47*x (with 47 an int) the same way as x*47
        (it would raise TypeError error otherwise)
        """
        return self * other

    def __mul__(self, other: Union["PadicInt", int]) -> "PadicInt":
        """Computes p-adic multiplication.

        :Example:
        >>> Z2 = Padic(2)
        >>> x = Z2.from_int(3)
        >>> (2*x).to_str()
        '...0000000110'
        >>> (5*x).to_str()
        '...0000001111'
        >>> (27*x).to_str()
        '...0001010001'
        >>> (x*x).to_str()
        '...0000001001'
        >>> y = Z2(digit_function=lambda x: (x+1)%2)
        >>> (3*y + 1).to_str()
        '...0000000000'
        """

        # Convert to p-adic if given an int
        if isinstance(other, int):
            other = Padic(self.p).from_int(other)

        if self.p != other.p:
            raise ValueError(
                f"Cannot multiply p-adic integers with different p: {self.p} {other.p}"
            )

        @functools.lru_cache
        def multiplication_digit_function(n: int) -> int:
            carry = 0
            if n > 0:
                _, carry = multiplication_digit_function(n - 1)

            # Cauchy produt rule
            sum_ = (
                sum(
                    [
                        self.digit_function(k) * other.digit_function(n - k)
                        for k in range(n + 1)
                    ]
                )
                + carry
            )
            new_carry = sum_ // self.p

            return sum_ % self.p, new_carry

        # Updating the underlying rational if it is set for both operands
        underlying_rational = None
        if None not in (self.underlying_rational, other.underlying_rational):
            underlying_rational = (
                self.underlying_rational * other.underlying_rational
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
            lambda n: multiplication_digit_function(n)[0],
            underlying_rational=underlying_rational,
        )

    def __lshift__(self, shift: int):
        """Implements x << shift, which adds `shift` 0s to the end of x.
        :Example:
        >>> Z2 = Padic(2)
        >>> x = Z2.from_int(3)
        >>> x.to_str()
        '...0000000011'
        >>> (x << 3).to_str()
        '...0000011000'
        >>> Z3 = Padic(3)
        >>> y = Z3.from_int(19)
        >>> (y << 4).to_str()
        '...0002010000'
        """

        def left_shifted_digit_function(n: int):
            if n < shift:
                return 0
            return self.digit_function(n - shift)

        underlying_rational = None
        if underlying_rational is not None:
            underlying_rational *= self.p**shift

        return PadicInt(
            self.p,
            left_shifted_digit_function,
            underlying_rational=underlying_rational,
        )

    def __rshift__(self, shift: int):
        """Implements x >> shift, which remove `shift` digits of the end of x.
        :Example:
        >>> Z2 = Padic(2)
        >>> x = Z2.from_int(6)
        >>> x.to_str()
        '...0000000110'
        >>> (x >> 1).to_str()
        '...0000000011'
        >>> (x >> 2).to_str()
        '...0000000001'
        >>> (x >> 3).to_str()
        '...0000000000'
        >>> Z3 = Padic(3)
        >>> x = Z3.from_int(1036)
        >>> x.to_str()
        '...0001102101'
        >>> (x >> 3).to_str()
        '...0000001102'
        """

        def right_shifted_digit_function(n: int):
            return self.digit_function(n + shift)

        underlying_rational = None
        if underlying_rational is not None:
            if isinstance(underlying_rational, int):
                underlying_rational //= self.p**shift
            else:  # Careful // on sympy Rational would have different behavior
                underlying_rational /= self.p**shift

        return PadicInt(
            self.p,
            right_shifted_digit_function,
            underlying_rational=underlying_rational,
        )

    def rational_periodic_representation(self, to_str = True) -> Union[str,Tuple[str,str]]:
        """Rational p-adic integers are exactly the p-adics integers with eventually periodic representation. Hence we can write them (w1)* w0 with w0 and w1 finite base-p strings.

        [1] Keith Conrad. “The p-adic expansion of rational numbers”. https://kconrad.math.uconn.edu/blurbs/gradnumthy/rationalsinQp.pdf.

        :Example:
        >>> Z2 = Padic(2)
        >>> x = Z2.from_int(0)
        >>> x.rational_periodic_representation()
        '(0)*'
        >>> x = Z2.from_int(-17)
        >>> x.rational_periodic_representation()
        '(1)* 01111'
        >>> x = Z2.from_rational(Rational(1778,53))
        >>> x.rational_periodic_representation()
        '(0010000111001111101100101011011110001100000100110101)* 101010'
        >>> x = Z2.from_rational(Rational(-1,23))
        >>> x.rational_periodic_representation()
        '(00001011001)*'

        >>> Z3 = Padic(3)
        >>> x = Z3.from_rational(Rational(346,86))
        >>> x.rational_periodic_representation()
        '(102221010010202201110120001212212020021112)* 22'
        """

        if self.underlying_rational is None:
            raise ValueError(
                "Rational periodic representation can only be computed on p-adic integers that have `underlying_rational` defined."
            )

        # We compute the periodic representation by keeping track
        # of all numerators enumerated under iteration of f(x) = (x-i)/p with
        # i = x.numerator % p
        seen_numerators: Dict[int, int] = {}
        # We wrap around Rational in case `self.underlying_rational` is an int
        x = Rational(self.underlying_rational)
        digit_list = []
        k = 0
        while x.numerator not in seen_numerators:
            seen_numerators[x.numerator] = k
            i = x.numerator % self.p
            digit_list.append(i)
            x = (x - i) / self.p
            k += 1
        k = seen_numerators[x.numerator]
        w0 = "".join(list_int_to_list_str(digit_list[:k][::-1]))
        w1 = "".join(list_int_to_list_str(digit_list[k:][::-1]))

        if to_str:
            if len(w0) == 0:
                return f"({w1})*"

            return f"({w1})* {w0}"

        return w1, w0

def least_significant_digit(x: Union[int, Rational, PadicInt], base = 2) -> int:
    """ Returns the least significant digit of an integer in a base or rational p-adic or p-adic.

    :Example:
        >>> least_significant_digit(25)
        1
        >>> least_significant_digit(47,3)
        2
        >>> from sympy import Rational
        >>> least_significant_digit(Rational(2,15))
        0
    """
    if isinstance(x,int):
        return x % base

    if isinstance(x,Rational):
        if gcd(base, x.denominator) == 1:
            return x.numerator % base
        else:
            raise ValueError(
                f"Rational {x} cannot be expressed {base}-adically because its denominator is not co-prime with p."
            )
    
    if isinstance(PadicInt):
        return x.digits(0)[0]