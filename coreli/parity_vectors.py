from typing import Tuple, Union
from coreli.Collatz_maps import T
from coreli.padic_integers import PadicInt, least_significant_digit
from coreli.utils import int_to_base, iterate,iterates
from sympy import Rational

""" Implementing Collatz parity vectors.

    References
    ========== 

    [1] A stopping time problem on the positive integers. Riho Terras. 
        Acta Arithmetica 30.3, pp. 241-252. 1976.
        http://eudml.org/doc/205476

    [2] The 3x + 1 Problem and Its Generalizations. Jeffrey C. Lagarias. 
        The American Mathematical Monthly 92.1, pp. 3-23. 1985.
        http://www.jstor.org/stable/2322189

    [3] Parity Sequences of the 3x+1 Map on the 2-adic Integers and Euclidean
        Embedding. Olivier Rozier. Integers 19. 2019.
        https://arxiv.org/abs/1805.00133

    [4] Binary expression of ancestors in the Collatz graph. Tristan Stérin.
        RP 2020: Proceedings of the 14th International Conference on Reachability 
        Problems, (Paris, France, October 19-21, 2020), pp 115-130. 2020.
        https://arxiv.org/abs/1907.00775

"""

class ParityVector(object):
    """ A parity vector is a list of 0s and 1s which corresponds to the 
    parity of elements of a Collatz sequences (with map T).
    (i.e. which of the maps x/2 or (3x+1)/2 is taken at each step)

    It is known that (see [1,2,3]):
        - All parity vectors are feasible in N, i.e. for any parity vector
        of length n there is a natural number that follows the parities given by the 
        parity vector in its first n T-Collatz steps.

        - More precisely, for any parity vector of length n, there is a smallest 
        integer α in N such that the first n T-Collatz steps follow the parities 
        given by the parity vector, and then, all integers of the form a2^n + α
        also follow the parities given by the parity vector. We say that 
        (α,β) is the first "occurrence" of the parity vector, with β = T^n(α).

        - There is a bijection between parity vectors of length n and numbers < 2^n,
        i.e. two distinct numbers < 2^n have distinct length-n parity vectors.

        - When considering infinite parity vectors (i.e. associated to infinite 
        T-Collatz sequences), we get a continuous bijection Q from Z_2 to Z_2, 
        mapping Collatz-inputs in Z_2 to their parity vector, seen as an element 
        of Z_2 (see [2,3]).

        - It is known that if Q(x) is eventually periodic then x is eventually periodic
        i.e. x is rational.

        - It is conjectured that if x is eventually periodic then Q(x) is eventually 
        periodic, Lagarias Periodicity Conjecture [2]. If this conjecture is true,
        then there is no divergent Collatz orbit in N.
    """
    def __init__(self, parity_vector):
        if len(list(filter(lambda x: x not in [0,1], parity_vector))) != 0:
            raise ValueError(f"A parity vector must contain only 0s and 1s, which is not the case for {parity_vector}")
        self.parity_vector = parity_vector
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return str(self.parity_vector)

    @classmethod
    def from_Collatz(cls, x: Union[int, Rational, PadicInt], n: int) -> "ParityVector":
        """ Returns the parity vector corresponding to n application of Collatz map T.
        The parity vector will be of size n+1.

        :Example:
            >>> ParityVector.from_Collatz(23,10)
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        """
        return cls(list(map(least_significant_digit, iterates(T, n, x))))

    def first_occurrence(self, symbolic=False) -> Union[Tuple[int,int],Tuple[str,str]]:
        """ Returns the couple (α,β) such that α is the smallest number in N
        such that its first n T-Collatz steps follow the parities given by 
        the length-n parity vector. And, β = T^n(α).

        There are explicit formulae for α and β, seen [3]. But here we use an iterative 
        algorithm described in [4].

        If `symbolic` is true, the function returns α in base 2 and n bits and β in base 3
        and k bits with k the number of 1s in the parity vector.

        :Example:
        >>> ParityVector([1,1,0,1]).first_occurrence()
        (11, 20)
        >>> ParityVector([1,1,0,1]).first_occurrence(symbolic=True)
        ('1011', '202')
        >>> ParityVector([1,0,0,0,1]).first_occurrence(symbolic=True)
        ('00101', '02')
        """

        n = len(self.parity_vector)
        alpha = 0
        beta = 0
        k = 0

        for i,b in enumerate(self.parity_vector):
            if b != beta%2:
                alpha += 2**i

            if b == 1:
                k += 1

            modular_inverse_of_two = (3**k+1)//2
            if b == 0:
                beta = (beta * modular_inverse_of_two)%(3**k)
            else:
                beta = ((3*beta + 1 )*modular_inverse_of_two)%(3**(k))
            
        assert(beta == iterate(T,n,alpha))
        
        if not symbolic:
            return alpha, beta

        return int_to_base(alpha,2,n), int_to_base(beta,3,k)




    