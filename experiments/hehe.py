import itertools
from graphviz import Digraph


def rotate(l, n):
    return l[-n:] + l[:-n]


# pv_template = (1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1)


def template_to_product(template):
    return map(lambda b: [0, 1] if b == 0 else [0, 1, 2], template)


def pv_space_size(template):
    p = 1
    for b in template:
        if b == 0:
            p *= 2
        else:
            p *= 3
    return p


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


# # Example usage:
# a, b, A, B = 1, 2, 2, 3
# x = crt(a, b, A, B)
# print(f"x ≡ {x} mod {A*B}")


def solve(right, bottom):
    """
    for a in itertools.product([0,1],[0,1,2]):
      print(a, solve(a[1],a[0]))
    """
    tile = crt(bottom, right, 2, 3)
    return tile // 2, tile // 3


def line(right_most, bottom):
    top = []

    curr_right = right_most
    for b in bottom:
        curr_right, curr_top = solve(curr_right, b)
        top.append(curr_top)

    return curr_right, top


def next_cyclic_valuation_b6(pv, pv_template):
    bottom = []
    new_pv = []
    for i, b in enumerate(pv_template[::-1]):
        if b == 0:
            bottom.append(pv[::-1][i])
        if b == 1:
            left_most, top = line(pv[::-1][i], bottom[::-1])
            # print(pv[::-1][i], bottom[::-1], left_most, top)
            new_pv.append(left_most)
            new_pv += top[::-1]
            # print(new_pv)
            bottom = []
    # print(new_pv[::-1])
    return tuple(rotate(new_pv[::-1], 1))


# pv = pv_template
# next_of_pv = {}
# for pv in itertools.product(*template_to_product(pv_template)):
#     next_of_pv[pv] = next_cyclic_valuation_b6(pv, pv_template)


from collections import defaultdict


def compute_components(graph):
    visited = set()
    components = []
    node_to_component = {}

    # Build reverse graph
    reverse_graph = defaultdict(list)
    for u, v in graph.items():
        reverse_graph[v].append(u)

    def explore(start):
        component = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node is None or node in visited:
                continue
            visited.add(node)
            component.add(node)
            # Explore forward
            next_node = graph.get(node)
            if next_node not in visited:
                stack.append(next_node)
            # Explore backward
            for prev in reverse_graph[node]:
                if prev not in visited:
                    stack.append(prev)
        return component

    for node in graph:
        if node not in visited:
            component = explore(node)
            components.append(component)
            for n in component:
                node_to_component[n] = component

    return components, node_to_component


# components, node_to_component = compute_components(next_of_pv)

# zero = tuple([0] * len(pv_template))
# minus_one = tuple([2 if b == 1 else 1 for b in pv_template])


def two_not_in_pv(pv):
    return 2 not in pv


# print(len(next_of_pv))
# print(len(components))
# print(len(node_to_component[pv_template]))
# print(len(node_to_component[zero]))
# print(len(node_to_component[minus_one]))

# print()
# for c in components:
#     print(len(c), end="")
#     if len(c) == len(node_to_component[pv_template]):
#         print("*", end="")
#     if len(c) == len(node_to_component[zero]):
#         print("°", end="")
#     print()

# for c in components:
#     if len(c) == len(node_to_component[zero]):
#         for e in c:
#             print(e)
#     print()

# import matplotlib.pyplot as plt

# plt.hist([len(c) for c in components])
# plt.show()


# for elem in node_to_component[pv_template]:
#     print(elem)

# print()
# k = 0
# for pv in list(filter(two_not_in_pv, node_to_component[zero])):
#     print(pv)
#     k += 1

# print()
# print(k)
# print(pv_template)


def graph_to_dot(graph, highlight_nodes=None):
    """
    Convert a functional graph (dict of node -> successor) to a Graphviz DOT string.

    highlight_nodes: optional set of nodes to color differently.
    """
    lines = ["digraph G {"]
    lines.append("  rankdir=LR;")  # left-to-right layout
    lines.append("  node [shape=circle, fontsize=10];")

    for node, successor in graph.items():
        node_str = f'"{node}"'
        succ_str = f'"{successor}"'
        lines.append(f"  {node_str} -> {succ_str};")

    if highlight_nodes:
        for node in highlight_nodes:
            lines.append(f'  "{node}" [style=filled, fillcolor=lightblue];')

    lines.append("}")
    return "\n".join(lines)


def render_full_graph(graph, highlight_nodes=None, max_nodes=None, filename="graph"):
    """
    Render the entire graph. Optionally highlight some nodes.
    If max_nodes is set, stops after rendering that many edges.
    """
    dot = Digraph()
    dot.attr(rankdir="LR", fontsize="10")
    highlight_nodes = set(highlight_nodes or [])
    count = 0

    for src, dst in graph.items():
        if max_nodes and count >= max_nodes:
            break

        # Add nodes with optional highlight
        for node in (src, dst):
            if node not in dot.node_attr:
                dot.node(
                    str(node),
                    shape="circle",
                    style="filled",
                    fillcolor="lightblue" if node in highlight_nodes else "white",
                )

        # Add edge
        dot.edge(str(src), str(dst))
        count += 1

    dot.render(filename, view=True, format="png")


# # Highlight the component of pv_template
# highlight_nodes = node_to_component[pv_template]

# # Show full graph with highlight
# render_full_graph(next_of_pv, highlight_nodes=highlight_nodes, filename="full_graph")


def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


for pv_template in itertools.product([0, 1], repeat=8):
    pv = pv_template
    next_of_pv = {}
    for pv in itertools.product(*template_to_product(pv_template)):
        next_of_pv[pv] = next_cyclic_valuation_b6(pv, pv_template)
    components, node_to_component = compute_components(next_of_pv)
    zero = tuple([0] * len(pv_template))
    minus_one = tuple([2 if b == 1 else 1 for b in pv_template])

    print(
        pv_template,
        # len(node_to_component[zero]),
        # min([len(c) for c in components]),
        # is_power_of_two(len(node_to_component[zero])),
        # len(node_to_component[zero]) == len(node_to_component[minus_one]),
        len(node_to_component[zero]) == min([len(c) for c in components]),
        is_power_of_two(len(node_to_component[zero])),
    )

# There is a pattern of when the class of 0 is the smallest class
# and it is always the smallest class when pv_template starts with a 1

# TODO: bullet proof code
# TODO: study rotations of PV
