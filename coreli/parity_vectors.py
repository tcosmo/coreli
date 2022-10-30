from typing import Tuple, Union
from coreli.Collatz_maps import T
from coreli.Collatz_tilings import Collatz_tileset
from coreli.padic_integers import PadicInt, least_significant_digit
from coreli.tinytiles.model import SquareGlues, Tiling
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

    [3] On the combinatorial structure of 3N + 1 predecessor sets. Günther Wirsching. 
        Discrete Mathematics 148.1-3, pp. 265-286. 1996. 
        doi: 10.1016/0012-365x(94)00243-c.

    [4] Parity Sequences of the 3x+1 Map on the 2-adic Integers and Euclidean
        Embedding. Olivier Rozier. Integers 19. 2019.
        https://arxiv.org/abs/1805.00133

    [5] Binary expression of ancestors in the Collatz graph. Tristan Stérin.
        RP 2020: Proceedings of the 14th International Conference on Reachability 
        Problems, (Paris, France, October 19-21, 2020), pp 115-130. 2020.
        https://arxiv.org/abs/1907.00775

"""

class ParityVector(object):
    """ A parity vector is a list of 0s and 1s which corresponds to the 
    parity of elements of a Collatz sequences (with map T).
    (i.e. which of the maps x/2 or (3x+1)/2 is taken at each step)

    It is known that (see [1,2,4]):
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
        of Z_2 (see [2,4]).

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
    
    def __len__(self):
        return len(self.parity_vector)

    def odd_len(self):
        """ Returns the number of 1s (odd terms) in the parity vector which is a metric that is often used
        when working with parity vector.
        """
        return len(list(filter(lambda x: x==1,self.parity_vector)))

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

        There are explicit formulae for α and β, seen [4]. But here we use an iterative 
        algorithm described in [5].

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

        n = len(self)
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

    def rotate(self, n: int = 1) -> "ParityVector":
        def rotate_list(l,n):
            sign = -1 if n < 0 else 1
            n = sign*(abs(n)%len(l))
            return l[n:] + l[:n]
        rotated_pv = rotate_list(self.parity_vector,n)
        return ParityVector(rotated_pv)

    def most_complex_tile(self) -> Union[None,int]:
        """ Returns the "most complex tile" of a parity vector. 
        See Tristan Stérin's thesis, Chapter 1, Section 1.5, for definition.

        >>> ParityVector([1,1,0,1]*2).most_complex_tile()
        2

        >>> ParityVector([1,1,0,1]*2).rotate()
        [1, 0, 1, 1, 1, 0, 1, 1]
        >>> ParityVector([1,1,0,1]*2).rotate().most_complex_tile()
        3

        >>> ParityVector([1,1,0,1]*2).rotate(-1)
        [1, 1, 1, 0, 1, 1, 1, 0]
        >>> ParityVector([1,1,0,1]*2).rotate(-1).most_complex_tile()
        5
        """
        tiling = self.to_tiling()
        tiling.all_steps()
        tile = tiling.get_top_left_tile()

        if tile is None or not isinstance(tile,int):
            return None
        
        return tile
        


    def cyclic_rational(self) -> Rational:
        """ Returns the unique rational x such that T^n(x) = x and the parity vector
        corresponds to the n first Collatz steps of x.

        Explicit formula deducible from 2.13 in [3] (page 41). 

        This rational also happen to be 2-adic, 3-adic and 6-adic integer since its numerator
        is of the form 2^n - 3^k (its not a multiple of 2, 3, or 6).

        :Example:
            >>> ParityVector([1]).cyclic_rational()
            -1
            >>> ParityVector([1,1,0]).cyclic_rational()
            -5
            >>> ParityVector([1,1,1,1,0,1,1,1,0,0,0]).cyclic_rational()
            -17
            >>> ParityVector([1,1,0,1,0,0]).cyclic_rational()
            23/37
            >>> ParityVector([0,0,1,0,0]).cyclic_rational()
            4/29
            >>> ParityVector([1,1,0,1,1]).cyclic_rational()
            -85/49
            >>> ParityVector([1,0,0,1,1,1]).cyclic_rational()
            -179/17
        """

        indices_of_1s = [i for i, x in enumerate(self.parity_vector) if x == 1]

        n = len(self)
        k = self.odd_len()
        sum = 0
        
        for i, s in enumerate(indices_of_1s):
            sum += 3**(k-1-i)*2**(s)
        
        return Rational(sum, 2**n - 3**k)

    def to_tiling(self) -> Tiling:
        """ Builds the Collatz tiling associated to the parity vector.
        """
        pos = [len(self)-1,self.odd_len()]
        tiling: Tiling = {}
        
        for pbit in self.parity_vector:
            tpos = tuple(pos)
            #print(tpos)  
            if pbit == 0:
                if tpos not in tiling:
                    tiling[tpos] = [None]*4
                tiling[tpos][0] = 0
                pos[0] -= 1
            else:
                tpos_east = tpos[0]+1,tpos[1]
                tpos_south = tpos[0],tpos[1]-1
                if tpos_east not in tiling:
                    tiling[tpos_east] = [None]*4
                if tpos_south not in tiling:
                    tiling[tpos_south] = [None]*4
                #print("east",tpos_east)
                tiling[tpos_east][3] = 1
                tiling[tpos_south][0] = 0
                pos[0] -= 1
                pos[1] -= 1
        
        for pos in tiling:
            tiling[pos] = SquareGlues(*tiling[pos])
        
        return Tiling(tiling, Collatz_tileset)