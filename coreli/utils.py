from typing import List, Union

def list_int_to_list_str(l: List[int]) -> List[str]:
    """Converts each int of a list to a str.

    :Example:
        >>> list_int_to_list_str([1,1,0,1])
        ['1', '1', '0', '1']
        >>> list_int_to_list_str([5,12,31,7])
        ['5', '12', '31', '7']
    """
    return list(map(lambda x: str(x), l))


def int_to_base(
    x: int, base: int, length: Union[None,int] = None, to_str: bool = True
) -> Union[str, List[int]]:
    """Converts a non-negative integer to its base representation.
    Note that in the list representation, the least significant digit comes first whereas,
    in the string representation, the least significant digit comes last.

    Args:
            x (int): the positive integer to convert
            base (int): the target base
            to_str (bool): whether the result is given as a string or a list of digits
            length (None or int): if not None, the output representation will be padded 
            with leading 0s so its length is equal to `length`. If `length` is smaller 
            than the representation's size, the function will raise

    :Example:
        >>> int_to_base(13,2)
        '1101'
        >>> int_to_base(13,2,9)
        '000001101'
        >>> int_to_base(13,2,to_str=False)
        [1, 0, 1, 1]
        >>> int_to_base(313,5)
        '2223'
        >>> int_to_base(313,5,to_str=False)
        [3, 2, 2, 2]
        >>> int_to_base(0,87)
        '0'
    """

    if x < 0:
        raise ValueError(f"Input to base-{base} conversion is negative: {x}")

    digits = []
    while x != 0:
        digits.append(x % base)
        x //= base

    if len(digits) == 0:
        digits = [0]


    if length is not None:
        if length < len(digits):
            raise ValueError(f"Length {length} is smaller than the length of {digits}")
        digits += [0]*(length-len(digits))

    if not to_str:
        return digits

    return "".join(list_int_to_list_str(digits)[::-1])


def iterate(f, n, x_0) -> int:
    """Returns the nth iterate of f from x_0, i.e., f^n(x_0)."""
    last_result = x_0
    for _ in range(n):
        last_result = f(last_result)
    return last_result


def iterates(f, n, x_0) -> List[int]:
    """Returns the list of the n+1 first iterates of f (including x_0): [x_0, f(x_0), ..., f^n(x_0)]."""
    to_return = [x_0]
    for _ in range(n):
        to_return.append(f(to_return[-1]))
    return to_return