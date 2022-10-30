import coreli.tinytiles as tt
from coreli.tinytiles.model import SquareGlues, Tiling


Collatz_tileset: tt.Tileset = [(0,0,0,0),(0,1,1,0),(0,2,0,1),
                   (1,0,1,1),(1,1,0,2),(1,2,1,2)]
    
Extended_Collatz_tileset: tt.Tileset = [(0,0,0,0),(0,1,1,0),(0,2,0,1),
                   (1,0,1,1),(1,1,0,2),(1,2,1,2),(1,'S',0,2),(0,'S',0,'S')]

def south_east_corner(south: str, east: str) -> Tiling:
    """ Returns Collatz tiling corresponding to south east corner
    with ternary word to the east and binary word to the south.
    """

    n = len(south)+1

    tiling = {}
    for i, trit in enumerate(east[::-1]):
        if trit not in ['0','1','2']:
            raise ValueError(f"East word {east} is not a ternary string")
        tiling[n-1,i+1] = SquareGlues(None,None,None,int(trit))

    for i, bit  in enumerate(south):
        if trit not in ['0','1']:
            raise ValueError(f"South word {south} is not a binary string")
        tiling[i,0] = SquareGlues(int(bit),None,None,None)

    return Tiling(tiling, Collatz_tileset)

def south_west_corner(south: str, west: str) -> Tiling:
    """ Returns Collatz tiling corresponding to south west corner
    with ternary word to the west and binary word to the south.
    """

    tiling = {}
    for i, trit in enumerate(west[::-1]):
        if trit not in ['0','1','2']:
            raise ValueError(f"West word {west} is not a ternary string")
        tiling[0,i+1] = SquareGlues(None,int(trit),None,None)

    for i, bit  in enumerate(south):
        if trit not in ['0','1']:
            raise ValueError(f"South word {south} is not a binary string")
        tiling[i+1,0] = SquareGlues(int(bit),None,None,None)

    return Tiling(tiling, Collatz_tileset)

def north_east_corner(north: str, east: str) -> Tiling:
    """ Returns Collatz tiling corresponding to north east corner
    with ternary word to the east and binary word to the north.
    """

    n = len(north)+1

    tiling = {}
    for i, trit in enumerate(east[::-1]):
        if trit not in ['0','1','2']:
            raise ValueError(f"East word {east} is not a ternary string")
        tiling[n-1,i+1] = SquareGlues(None,None,None,int(trit))

    for i, bit  in enumerate(north):
        if trit not in ['0','1']:
            raise ValueError(f"North word {north} is not a binary string")
        tiling[i,len(north)+2] = SquareGlues(None,None,int(bit),None)

    return Tiling(tiling, Collatz_tileset)

def base6_diagonal(diagonal: str) -> Tiling:
    """ Returns Collatz tiling corresponding to north-west-going
    base 6 diagonal.
    """
    tiling = {}

    for i,s in enumerate(diagonal):
        if s not in ['0','1','2','3','4','5']:
            raise ValueError(f"Diagonal word {diagonal} is not base-6")
        
        tiling[i,len(diagonal)-i] = Collatz_tileset[int(s)]

    return Tiling(tiling, Collatz_tileset) 

def base32_diagonal(diagonal: str) -> Tiling:
    """ Returns Collatz tiling corresponding to south-west-going
    base 3/2 diagonal.
    """
    tiling = {}

    for i,s in enumerate(diagonal[::-1]):
        if s not in ['0','1','2','3','4','5']:
            raise ValueError(f"Diagonal word {diagonal} is not base 3/2")
        
        tiling[i,i] = Collatz_tileset[int(s)]

    return Tiling(tiling, Collatz_tileset) 