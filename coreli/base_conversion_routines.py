""" Contains helper functions for base conversion.
"""
def int_to_binary(x: int, n_bits: int = None) -> str:
    """ Standard binary representation of numbers. You can specify the number of bits\
        of the outputed string (leading 0s will be inserted).

        :Example:
            >>> int_to_binary(10)
            '1010'
            >>> int_to_binary(10,5)
            '01010'
    """
    x_bin = bin(x)[2:]
    if n_bits is None:
        return x_bin

    if n_bits < len(x_bin):
        raise ValueError('Cannot write {} (`{}`) on {} bits'.format(x,x_bin,n_bits))
    return '0'*(n_bits-len(x_bin))+x_bin

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