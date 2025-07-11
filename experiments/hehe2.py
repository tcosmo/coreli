import sys

sys.path.append("../")

import coreli
import sympy

import svg

from copy import deepcopy


def extended_gcd(a, b):
    """Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd"""
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)


def crt(a, b, A, B):
    """Chinese Remainder Theorem for coprime A and B.
    Returns x such that x ≡ a mod A and x ≡ b mod B."""
    g, m1, m2 = extended_gcd(A, B)
    if g != 1:
        raise ValueError("A and B must be coprime")

    # Compute the solution modulo A * B
    x = (a * m2 * B + b * m1 * A) % (A * B)
    return x


def compose(f, g, x):
    return f.subs(x, g)


def compose_list(l, x):
    if l == []:
        return x
    return compose(l[0], compose_list(l[1:]))


class ValuedArrow(object):
    x = sympy.Symbol("x")

    @staticmethod
    def opp(arrow):
        if arrow == "→":
            return "←"
        elif arrow == "←":
            return "→"
        elif arrow == "↓":
            return "↑"
        elif arrow == "↑":
            return "↓"
        elif arrow == "↘":
            return "↖"
        elif arrow == "↖":
            return "↘"
        elif arrow == "↙":
            return "↗"
        elif arrow == "↗":
            return "↙"
        return None

    def __init__(self, arrow, value):
        if arrow not in ["→", "←", "↓", "↑", "↘", "↖", "↙", "↗"]:
            raise ValueError("Arrow not valid")
        self.arrow = arrow
        self.value = value
        self.varrow = (arrow, value)

    def is_diagonal(self) -> bool:
        return self.arrow in ["↘", "↖", "↙", "↗"]

    def is_horizontal(self) -> bool:
        return self.arrow in ["→", "←"]

    def is_vertical(self) -> bool:
        return self.arrow in ["↓", "↑"]

    def height(self) -> int:
        return -1 * self.get_move()[1]

    def get_move(self) -> tuple[int, int]:  # x,y
        if self.arrow == "→":
            return (1, 0)
        elif self.arrow == "←":
            return (-1, 0)
        elif self.arrow == "↓":
            return (0, -1)
        elif self.arrow == "↑":
            return (0, 1)
        elif self.arrow == "↘":
            return (1, -1)
        elif self.arrow == "↖":
            return (-1, 1)
        elif self.arrow == "↙":
            return (-1, -1)
        elif self.arrow == "↗":
            return (1, 1)

        raise ValueError("not valid")

    def __str__(self):
        return str(self.varrow)

    def __repr__(self):
        return str(self)

    def func(self):
        if self.arrow in ["←", "→"]:
            if self.value not in [0, 1]:
                raise ValueError("Value not valid")
            if self.arrow == "→":
                return 2 * self.x + self.value
            else:
                return (self.x - self.value) * sympy.Rational(1, 2)
        elif self.arrow in ["↓", "↑"]:
            if self.value not in [0, 1, 2]:
                raise ValueError("Value not valid")
            if self.arrow == "↓":
                return 3 * self.x + self.value
            else:
                return (self.x - self.value) * sympy.Rational(1, 3)
        elif self.arrow in ["↙", "↗"]:
            if self.value not in [0, 1, 2, 3, 4, 5]:
                raise ValueError("Value not valid")
            if self.arrow == "↙":
                return 3 * self.x / 2 + (
                    (2 * (self.value // 2)) - 3 * ((self.value // 3))
                ) * sympy.Rational(1, 2)
            else:
                return 2 * self.x / 3 + (
                    (3 * (self.value // 3)) - 2 * ((self.value // 2))
                ) * sympy.Rational(1, 3)
        elif self.arrow in ["↘", "↖"]:
            if self.value not in [0, 1, 2, 3, 4, 5]:
                raise ValueError("Value not valid")
            if self.arrow == "↘":
                return 6 * self.x + self.value
            else:
                return (self.x - self.value) * sympy.Rational(1, 6)


class ValuedPath(object):
    x = sympy.Symbol("x")

    def __init__(self, valued_path: tuple[ValuedArrow | tuple[str, int]]):
        if len(valued_path) > 0 and type(valued_path[0]) != ValuedArrow:
            self.valued_path = tuple(
                map(lambda c: ValuedArrow(c[0], c[1]), valued_path)
            )
        else:
            self.valued_path = valued_path

    def values(self):
        return [t.value for t in self.valued_path]

    def arrows(self):
        return [t.arrow for t in self.valued_path]

    @staticmethod
    def from_parity_vector(pv: coreli.ParityVector | list[int]):
        if type(pv) == list:
            return ValuedPath(
                tuple(map(lambda x: ("←", 0) if x == 0 else ("↙", 4), pv))
            )
        return ValuedPath(
            tuple(map(lambda x: ("←", 0) if x == 0 else ("↙", 4), pv.parity_vector))
        )

    def func(self):
        new_f = self.valued_path[0].func()
        for va in self.valued_path[1:]:
            new_f = va.func().subs(self.x, new_f)
        return new_f

    def __str__(self):
        return str(self.valued_path)

    def __repr__(self):
        return str(self)

    def len(self):
        return len(self.valued_path)

    def height(self):
        return sum([a.height() for a in self.valued_path])

    def next_cyclic_vap(self, arrow):
        extended_vap = deepcopy(self)
        extended_vap.valued_path = (
            extended_vap.valued_path
            + extended_vap.valued_path
            + extended_vap.valued_path
        )
        world = World()
        world.place_initial_valued_path(extended_vap)

        # using 0 as placeholder
        varrow = ValuedArrow(arrow, 0)
        dx, dy = varrow.get_move()

        new_origin = (-1 * self.len() + dx, -1 * self.height() + dy)

        next_vap = world.read(self.arrows(), pos=new_origin, compute_missing=True)

        origin = (-1 * self.len(), -1 * self.height())
        value = None
        if varrow.is_horizontal():
            tile_coord = world.tile_coordinate_of_arrow(origin, varrow)
            value = world.world[tile_coord][world.SOUTH]
        if varrow.is_vertical():
            tile_coord = world.tile_coordinate_of_arrow(origin, varrow)
            value = world.world[tile_coord][world.EAST]
        if varrow.is_diagonal():
            tile_coord = world.tile_coordinate_of_arrow(origin, varrow)
            south = world.world[tile_coord][world.SOUTH]
            east = world.world[tile_coord][world.EAST]
            value = crt(south, east, 2, 3)

        return next_vap, ValuedArrow(ValuedArrow.opp(arrow), value)


def tile_id_to_sides(tile_id):
    return [tile_id // 3, tile_id % 3, tile_id % 2, tile_id // 2]


def tile_from_south_east(south, east):
    tile_id = crt(south, east, 2, 3)
    return tile_id_to_sides(tile_id)


class World(object):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def dir_to_str(direction):
        if direction == World.NORTH:
            return "N"
        elif direction == World.EAST:
            return "E"
        elif direction == World.SOUTH:
            return "S"
        elif direction == World.WEST:
            return "W"

    def __init__(self):
        self.world = {}

    def init_pos(self, pos):
        if pos not in self.world:
            self.world[pos] = [None, None, None, None]

    def place_arrow(self, valued_arrow: ValuedArrow, pos: tuple[int, int]):
        pos_north = (pos[0], pos[1] + 1)
        pos_east = (pos[0] + 1, pos[1])
        pos_south = (pos[0], pos[1] - 1)
        pos_west = (pos[0] - 1, pos[1])

        if valued_arrow.is_diagonal():
            self.init_pos(pos_north)
            self.init_pos(pos_east)
            self.init_pos(pos_south)
            self.init_pos(pos_west)

            self.world[pos] = tile_id_to_sides(valued_arrow.value)
            self.world[pos_north][self.SOUTH] = self.world[pos][self.NORTH]
            self.world[pos_east][self.WEST] = self.world[pos][self.EAST]
            self.world[pos_south][self.NORTH] = self.world[pos][self.SOUTH]
            self.world[pos_west][self.EAST] = self.world[pos][self.WEST]

            # TODO: check mismatches?

        elif valued_arrow.is_vertical():
            self.init_pos(pos)
            self.init_pos(pos_east)
            self.world[pos][self.EAST] = valued_arrow.value
            self.world[pos_east][self.WEST] = valued_arrow.value
        elif valued_arrow.is_horizontal():
            self.init_pos(pos)
            self.init_pos(pos_south)
            self.world[pos][self.SOUTH] = valued_arrow.value
            self.world[pos_south][self.NORTH] = valued_arrow.value

    def get_value_from_south_east(
        self, pos: tuple[int, int], direction: int, verbose=False
    ) -> int:
        if verbose:
            print("\t", pos, self.dir_to_str(direction))
        if pos not in self.world:
            self.init_pos(pos)

        if self.world[pos][direction] is not None:
            if verbose:
                print(
                    "\t\t",
                    "already defined",
                    self.world[pos][direction],
                    "at",
                    pos,
                    self.dir_to_str(direction),
                )
            return self.world[pos][direction]

        pos_south = (pos[0], pos[1] - 1)
        get_south_val = lambda: self.get_value_from_south_east(pos_south, self.NORTH)

        pos_east = (pos[0] + 1, pos[1])
        get_east_val = lambda: self.get_value_from_south_east(pos_east, self.WEST)

        if direction == self.SOUTH:
            # '←' is just used to represent horizontal
            value = get_south_val()
            self.place_arrow(ValuedArrow("←", value), pos)
            if verbose:
                print("\t\t", "place south arrow", value, "at", pos)
        elif direction == self.EAST:
            # '↑' is just used to represent vertical
            value = get_east_val()
            self.place_arrow(ValuedArrow("↑", value), pos)
            if verbose:
                print("\t\t", "place east arrow", value, "at", pos)
        else:
            south = get_south_val()
            east = get_east_val()
            tile_id = crt(south, east, 2, 3)
            # '↘' is just used to represent diagonal (tile)
            self.place_arrow(ValuedArrow("↘", tile_id), pos)
            if verbose:
                print("\t\t", "place tile", tile_id, "at", pos)

        return self.world[pos][direction]

    @staticmethod
    def tile_coordinate_of_arrow(pos, valued_arrow: ValuedArrow):
        x, y = pos
        arrow = valued_arrow.arrow
        if arrow == "→":
            return (x + 1, y)
        elif arrow == "←":
            return pos
        elif arrow == "↓":
            return (x, y - 1)
        elif arrow == "↑":
            return pos
        elif arrow == "↘":
            return (x + 1, y - 1)
        elif arrow == "↖":
            return pos
        elif arrow == "↙":
            return (x, y - 1)
        elif arrow == "↗":
            return (x + 1, y)

    def place_initial_valued_path(self, vap: ValuedPath):
        curr_pos = (0, 0)
        for valued_arrow in vap.valued_path:
            (dx, dy) = valued_arrow.get_move()
            self.place_arrow(
                valued_arrow, self.tile_coordinate_of_arrow(curr_pos, valued_arrow)
            )
            curr_pos = (curr_pos[0] + dx, curr_pos[1] + dy)

    def read(self, arrow_pattern, pos=(0, 0), compute_missing=False) -> ValuedPath:
        to_return = []
        for arrow in arrow_pattern:
            # using 0 as placeholder
            valued_arrow = ValuedArrow(arrow, 0)
            tile_coord = self.tile_coordinate_of_arrow(pos, valued_arrow)
            direction = self.SOUTH if valued_arrow.is_horizontal() else self.EAST

            # print(arrow, tile_coord, tile_coord in self.world)
            # if tile_coord in self.world:
            #     print(
            #         "\t",
            #         "already defined",
            #         self.world[tile_coord],
            #     )

            if tile_coord not in self.world:
                if not compute_missing:
                    raise ValueError(f"Pos {tile_coord} not found")

            if compute_missing:
                if not valued_arrow.is_diagonal():
                    self.get_value_from_south_east(tile_coord, direction)
                else:
                    self.get_value_from_south_east(tile_coord, self.EAST)
                    self.get_value_from_south_east(tile_coord, self.SOUTH)

            if tile_coord not in self.world:
                raise ValueError(f"Pos {tile_coord} not found")

            if valued_arrow.is_horizontal() or valued_arrow.is_vertical():
                to_return.append((arrow, self.world[tile_coord][direction]))
            else:
                # print(tile_coord, self.world[tile_coord])
                south = self.world[tile_coord][self.SOUTH]
                east = self.world[tile_coord][self.EAST]

                if south is None or east is None:
                    to_return.append((arrow, None))
                else:
                    tile_id = crt(south, east, 2, 3)
                    self.place_arrow(ValuedArrow("↘", tile_id), tile_coord)
                    to_return.append((arrow, tile_id))

            dx, dy = valued_arrow.get_move()
            pos = (pos[0] + dx, pos[1] + dy)

        return ValuedPath(tuple(to_return))

    # def compute_translated_vap(self, vap: ValuedPath, pos: tuple[int,int]) -> ValuedPath:


def draw_world_svgpy(world, cell_size=20, show_grid=True, highlight_points=[]):
    # Find world extents for viewBox
    xs = [x for (x, y) in world.keys()]
    ys = [y for (x, y) in world.keys()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = (max_x - min_x + 3) * cell_size
    height = (max_y - min_y + 3) * cell_size

    background = svg.Rect(x=0, y=0, width=width, height=height, fill="grey")

    canvas = svg.SVG(width=width, height=height, elements=[background])

    # Helper to map value to stroke width/color
    def stroke_params(val):
        if val == 0:
            return {"stroke": "beige", "stroke_width": 2}
        elif val == 1:
            return {"stroke": "green", "stroke_width": 2}
        elif val == 2:
            return {"stroke": "red", "stroke_width": 2}
        else:
            return {"stroke": "black", "stroke_width": 1}

    def world_to_svg(x, y):
        cx = (x - min_x + 2) * cell_size
        cy = (max_y - y + 2) * cell_size  # SVG Y-axis goes down
        return cx, cy

    # print(width, height)
    # print(min_x)
    for (x, y), edges in world.items():
        cx, cy = world_to_svg(x, y)

        x0, y0 = cx, cy
        x1, y1 = cx - cell_size, cy - cell_size

        N, E, S, W = edges

        # Draw lines if not None, with styling based on value
        if N is not None:
            params = stroke_params(N)
            canvas.elements.append(svg.Line(x1=x0, y1=y1, x2=x1, y2=y1, **params))
        if E is not None:
            params = stroke_params(E)
            canvas.elements.append(svg.Line(x1=x0, y1=y0, x2=x0, y2=y1, **params))
        if S is not None:
            params = stroke_params(S)
            canvas.elements.append(svg.Line(x1=x0, y1=y0, x2=x1, y2=y0, **params))
        if W is not None:
            params = stroke_params(W)
            canvas.elements.append(svg.Line(x1=x1, y1=y0, x2=x1, y2=y1, **params))

        # If fully defined (all edges not None), compute and draw tile_id
        if None not in edges:
            tile_id = crt(S, E, 2, 3)
            if tile_id is not None:
                text_x = cx - cell_size / 2
                text_y = cy - cell_size / 2
                canvas.elements.append(
                    svg.Text(
                        text=str(tile_id),
                        x=text_x,
                        y=text_y,
                        text_anchor="middle",
                        dominant_baseline="middle",
                        font_size=cell_size / 1.5,
                        fill="black",
                    )
                )

    if show_grid:
        for x in range(min_x - 3, max_x + 3):
            for y in range(min_y - 3, max_y + 3):
                cx, cy = world_to_svg(x, y)
                canvas.elements.append(
                    svg.Circle(cx=cx, cy=cy, r=1, fill="black", stroke_width=0)
                )

    for point in highlight_points:
        x, y = point
        cx, cy = world_to_svg(x, y)
        canvas.elements.append(
            svg.Circle(cx=cx, cy=cy, r=3, fill="magenta", stroke_width=0)
        )

    return canvas
