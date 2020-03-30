""" Contains helper functions for base conversion.
"""
def int_to_binary(x: int) -> str:
    """ Standard binary representation of numbers.

        :Example:
            >>> int_to_binary(10)
            '1010'
    """
    return bin(x)[2:]

def binary_to_int(x_bin: str) -> int:
    """ Inverse of `int_to_binary`.

        :Example:
            >>> binary_to_int('1010')
            10
    """
    return int(x_bin,2)

def base(x: int, k: int) -> str:
    """ Converts the integer `x` to its string representation in base `k`.

        :Example:
            >>> base(323, 3)
            '102222'
    """
    if x == 0:
        return '0'
    rep = ""
    while x != 0:
        rep += str(x%k)
        x //= k
    return rep[::-1]

def base23(x_bin: str) -> str:
    """ Converts binary to ternary.
    
        :Example:
            >>> base23('1010')
            '101'
    """
    return base(binary_to_int(x_bin),3)

def base32(x_ter: str) -> str:
    """ Converts ternary to binary.
    
        :Example:
            >>> base32('101')
            '1010'
    """
    return base(int(x_ter,3),2)