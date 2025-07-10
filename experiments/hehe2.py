import sys

sys.path.append("../")

import coreli
import sympy

import svg


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


class ValuedArrow(object):
    x = sympy.Symbol("x")

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
                    (2 * self.value // 2) - 3 * (self.value // 3)
                ) * sympy.Rational(1, 2)
            else:
                return 2 * self.x / 3 + (
                    (3 * self.value // 3) - 2 * (self.value // 2)
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

    def get_value_from_south_east(self, pos: tuple[int, int], direction: int) -> int:
        if pos not in self.world:
            self.init_pos(pos)

        if self.world[pos][direction] is not None:
            return self.world[pos][direction]

        pos_south = (pos[0], pos[1] - 1)
        get_south_val = lambda: self.get_value_from_south_east(pos_south, self.NORTH)

        pos_east = (pos[0] + 1, pos[1])
        get_east_val = lambda: self.get_value_from_south_east(pos_east, self.WEST)

        if direction == self.SOUTH:
            # '←' is just used to represent horizontal
            self.place_arrow(ValuedArrow("←", get_south_val()), pos)
        elif direction == self.EAST:
            # '↑' is just used to represent vertical
            self.place_arrow(ValuedArrow("↑", get_east_val()), pos)
        else:
            south = get_south_val()
            east = get_east_val()
            tile_id = crt(south, east, 2, 3)
            # '↘' is just used to represent diagonal (tile)
            self.place_arrow(ValuedArrow("↘", tile_id), pos)

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

    def read(self, arrow_pattern, pos=(0, 0), compute_missing=False):
        to_return = []
        for arrow in arrow_pattern:
            # using 0 as placeholder
            valued_arrow = ValuedArrow(arrow, 0)
            tile_coord = self.tile_coordinate_of_arrow(pos, valued_arrow)
            direction = self.SOUTH if valued_arrow.is_horizontal() else self.EAST
            if tile_coord not in self.world:
                if not compute_missing:
                    raise ValueError(f"Pos {tile_coord} not found")
                else:
                    self.get_value_from_south_east(tile_coord, direction)
                    if tile_coord not in self.world:
                        raise ValueError(f"Pos {tile_coord} not found")
            if valued_arrow.is_horizontal() or valued_arrow.is_vertical():
                to_return.append(self.world[tile_coord][direction])
            else:
                south = self.world[tile_coord][self.SOUTH]
                east = self.world[tile_coord][self.EAST]

                if south is None or east in None:
                    to_return.append(None)
                else:
                    to_return.append(crt(south, east, 2, 3))
            dx, dy = valued_arrow.get_move()
            pos = (pos[0] + dx, pos[1] + dy)
        return to_return

    # def compute_translated_vap(self, vap: ValuedPath, pos: tuple[int,int]) -> ValuedPath:


def draw_world_svgpy(world, cell_size=20):
    # Find world extents for viewBox
    xs = [x for (x, y) in world.keys()]
    ys = [y for (x, y) in world.keys()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = (max_x - min_x + 1) * cell_size
    height = (max_y - min_y + 1) * cell_size

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

    for (x, y), edges in world.items():
        cx = (x - min_x) * cell_size
        cy = (max_y - y) * cell_size  # SVG Y-axis goes down

        x0, y0 = cx, cy
        x1, y1 = cx + cell_size, cy + cell_size

        N, E, S, W = edges

        # Draw lines if not None, with styling based on value
        if N is not None:
            params = stroke_params(N)
            canvas.elements.append(svg.Line(x1=x0, y1=y0, x2=x1, y2=y0, **params))
        if E is not None:
            params = stroke_params(E)
            canvas.elements.append(svg.Line(x1=x1, y1=y0, x2=x1, y2=y1, **params))
        if S is not None:
            params = stroke_params(S)
            canvas.elements.append(svg.Line(x1=x0, y1=y1, x2=x1, y2=y1, **params))
        if W is not None:
            params = stroke_params(W)
            canvas.elements.append(svg.Line(x1=x0, y1=y0, x2=x0, y2=y1, **params))

        # If fully defined (all edges not None), compute and draw tile_id
        if None not in edges:
            tile_id = crt(S, E, 2, 3)
            if tile_id is not None:
                text_x = cx + cell_size / 2
                text_y = cy + cell_size / 2
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

    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 1):
            cx = (x - min_x) * cell_size
            cy = (max_y - y) * cell_size  # SVG Y-axis goes down
            canvas.elements.append(
                svg.Circle(
                    cx=cx, cy=cy, r=1, stroke="grey", fill="black", stroke_width=0
                )
            )

    return canvas
