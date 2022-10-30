from collections import namedtuple
from typing import Dict, Tuple, Union, List


Coordinates = namedtuple("Coordinates", "x", "y")


class SquareGlues(object):
    def __init__(
        self,
        north: Union[int, None] = None,
        east: Union[int, None] = None,
        south: Union[int, None] = None,
        west: Union[int, None] = None,
    ):
        self.north: Union[int, None] = north
        self.east: Union[int, None] = east
        self.south: Union[int, None] = south
        self.west: Union[int, None] = west


class World(object):
    def __init__(self):
        self.tiles: Dict[Coordinates, SquareGlues]


SquareGlues = Tuple[
    Union[int, None], Union[int, None], Union[int, None], Union[int, None]
]  # n,e,s,w
World = Dict[Coordinates, SquareGlues]
Tileset = List[SquareGlues]
