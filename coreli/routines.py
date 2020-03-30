def T(x: int) -> int:
    """The Collatz map. See: https://en.wikipedia.org/wiki/Collatz_conjecture
    """
    return x//2 if x%2 == 0 else (3*x+1)//2
