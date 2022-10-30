from typing import Dict, Tuple, List, Union
from collections import namedtuple

Coordinates = namedtuple('Coordinates', ['x','y'])
SquareGlues = namedtuple('SquareGlues', ['north', 'east', 'south', 'west'])
tTiling = Dict[Coordinates,SquareGlues]
Tileset = List[SquareGlues]

class Tiling(object):
    def __init__(self, tiling: tTiling, tileset: Tileset):
        self.tiling: tTiling = tiling
        self.tileset: Tileset = tileset

    def __getitem__(self, key):
        return self.tiling[key]

    def get_world_boundaries(self) -> Tuple[int,int]:
        """ Assuming positive coords only. """
        max_x = 0
        max_y = 0
        for x,y in self.tiling.keys():
            max_x = max(x,max_x)
            max_y = max(y,max_y)
        return max_x, max_y

    def get_neighboring_glues(self,pos) -> SquareGlues:
        to_ret: SquareGlues = [None]*4
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        for i, (dir_x,dir_y) in enumerate(directions):
                new_pos = pos[0]+dir_x, pos[1]+dir_y
                
                if pos in self.tiling and self.tiling[pos][i] is not None:
                    to_ret[i] = self.tiling[pos][i]
                elif new_pos in self.tiling:
                    to_ret[i] = self.tiling[new_pos][(i+2)%4]
        return to_ret

    def find_matching_tile_in_tileset(self, glues: SquareGlues, threshold:int) -> Union[None, SquareGlues]:
        to_ret = None
        for tile_type in self.tileset:
            score = 0
            for i in range(4):
                if tile_type[i] == None or glues[i] == None:
                    continue
                
                if tile_type[i] == glues[i]:
                    score += 1
                
                if score >= threshold:
                    return tile_type

    def get_top_left_tile(self) -> Union[None,SquareGlues]:
        world_w, world_h = self.get_world_boundaries()
        
        top_left = 0,world_h
        
        if top_left not in self.tiling:
            return None
        
        try:
            return self.tileset.index(self.tiling[top_left])
        except ValueError as e:
            return self.tiling[top_left]

    def all_steps(self, threshold=2, can_build_on_null_glues=True) -> None:
        while self.step(threshold, can_build_on_null_glues):
            continue
    
    def step(self, threshold=2, can_build_on_null_glues=True) -> None:
        """ One step of tile attachement.
        Inefficient n^2 implementation.
        """
        world_w, world_h = self.get_world_boundaries()

        for x in range(world_w+1):
            for y in range(world_h+1):
                pos = x,y
                
                
                if pos in self.tiling and None not in self.tiling[pos]:
                    continue
                    
                if pos in self.tiling and not can_build_on_null_glues and None in self.tiling[pos]:
                    continue
                
                neighboring_glues = self.get_neighboring_glues(pos)
                
                
                tile = self.find_matching_tile_in_tileset(neighboring_glues,threshold)
                #print(pos,neighboring_glues,tile)
                if tile is not None:
                    self.tiling[pos] = tile
                    return True
        return False 

    from drawSvg import Drawing
    def draw_svg(self) -> Drawing:
        from coreli.tinytiles.svg_view import draw_tiling
        return draw_tiling(self)