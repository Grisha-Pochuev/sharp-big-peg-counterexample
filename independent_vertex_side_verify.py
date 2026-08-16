#!/usr/bin/env python3
"""Third exact verifier using a different square parametrization.

Unlike the two center/offset verifiers, this program represents a square by
its first corner P=(x,y) and a side vector S=(sx,sy):

    P0 = P
    P1 = P + S
    P2 = P + S + J S
    P3 = P + J S,

where J(sx,sy)=(-sy,sx).  Thus its central 4x4 systems are derived from a
different set of unknowns and different coefficient formulas.

All decisions use exact Fraction/integer arithmetic from Python's standard
library.  This is a cross-check, not a search heuristic.
"""
from fractions import Fraction
from itertools import product

D = 1200
X = [
    (4114, -558), (2022, 1568), (-1234, 1006), (-868, 2516),
    (-1089, 2814), (-3769, 1169), (-3459, 81), (141, -1348),
    (571, -1449), (1105, -485),
]
N = len(X)

EXPECTED_MAX_SIDE2 = Fraction(
    56381275521625791352241234309,
    28343589374868261752462760000,
)
EXPECTED_GAP = Fraction(
    305903228110732152684285691,
    28343589374868261752462760000,
)
EXPECTED_POSITIVE = [
    (2, 4, 5, 6),
    (4, 5, 6, 2),
    (5, 6, 2, 4),
    (6, 2, 4, 5),
]


def line_data(e):
    ax, ay = X[e]
    bx, by = X[(e + 1) % N]
    dx, dy = bx - ax, by - ay
    nx, ny = -dy, dx
    return nx, ny, nx * ax + ny * ay


def build_vertex_side_system(assignment):
    """System in z=(x,y,sx,sy) for P0,P1,P2,P3 on four edge lines."""
    A, b = [], []
    for k, e in enumerate(assignment):
        nx, ny, h = line_data(e)
        if k == 0:
            csx, csy = 0, 0
        elif k == 1:
            csx, csy = nx, ny
        elif k == 2:
            csx, csy = nx + ny, -nx + ny
        else:
            csx, csy = ny, -nx
        A.append([Fraction(nx), Fraction(ny), Fraction(csx), Fraction(csy)])
        b.append(Fraction(h))
    return A, b


def exact_rref_status(A, b):
    """Return ('unique', solution), ('singular', None), or ('inconsistent', None)."""
    M = [A[i][:] + [b[i]] for i in range(4)]
    row = 0
    pivots = []
    for col in range(4):
        pivot = next((r for r in range(row, 4) if M[r][col] != 0), None)
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        pv = M[row][col]
        M[row] = [z / pv for z in M[row]]
        for r in range(4):
            if r == row:
                continue
            f = M[r][col]
            if f:
                M[r] = [M[r][j] - f * M[row][j] for j in range(5)]
        pivots.append(col)
        row += 1
    for r in range(4):
        if all(M[r][c] == 0 for c in range(4)) and M[r][4] != 0:
            return "inconsistent", None
    if len(pivots) < 4:
        return "singular", None
    sol = [Fraction(0) for _ in range(4)]
    for r, col in enumerate(pivots):
        sol[col] = M[r][4]
    return "unique", tuple(sol)


def corners_from_vertex_side(sol):
    x, y, sx, sy = sol
    return (
        (x, y),
        (x + sx, y + sy),
        (x + sx - sy, y + sy + sx),
        (x - sy, y + sx),
    )


def point_on_edge_exact(p, e):
    ax, ay = X[e]
    bx, by = X[(e + 1) % N]
    ex, ey = bx - ax, by - ay
    if Fraction(ex) * (p[1] - ay) - Fraction(ey) * (p[0] - ax) != 0:
        return False
    if ex != 0:
        t = (p[0] - ax) / ex
    else:
        t = (p[1] - ay) / ey
    return 0 <= t <= 1


singular = []
inconsistent = []
valid = 0
positive = []
max_side2 = Fraction(0)
max_assignment = None
max_solution = None

for assignment in product(range(N), repeat=4):
    A, b = build_vertex_side_system(assignment)
    status, sol = exact_rref_status(A, b)
    if status == "singular":
        singular.append(assignment)
        continue
    if status == "inconsistent":
        inconsistent.append(assignment)
        continue

    corners = corners_from_vertex_side(sol)
    if not all(point_on_edge_exact(corners[k], assignment[k]) for k in range(4)):
        continue

    valid += 1
    sx, sy = sol[2], sol[3]
    side2 = (sx * sx + sy * sy) / (D * D)
    if side2 > 0:
        positive.append((assignment, side2, corners))
    if side2 > max_side2:
        max_side2 = side2
        max_assignment = assignment
        max_solution = sol

expected_singular = [(i, i, i, i) for i in range(N)]
assert singular == expected_singular
assert inconsistent == []
assert valid == 144
assert [a for a, _, _ in positive] == EXPECTED_POSITIVE
assert len(positive) == 4
assert max_assignment == (2, 4, 5, 6)
assert max_side2 == EXPECTED_MAX_SIDE2
assert 2 - max_side2 == EXPECTED_GAP
assert max_side2 < 2

# The four positive assignments must be cyclic relabelings of one geometric square.
def canonical_corner_set(corners):
    return frozenset(corners)

assert len({canonical_corner_set(c) for _, _, c in positive}) == 1

print("PASS: independent vertex/side exact cross-check")
print("singular_assignments =", len(singular), "(only (i,i,i,i))")
print("inconsistent_singular_systems =", len(inconsistent))
print("valid_nonsingular_edge_assignments =", valid)
print("positive_oriented_square_assignments =", len(positive))
print("positive_assignments =", [a for a, _, _ in positive])
print("max_square_edge_assignment =", max_assignment)
print("max_square_side_squared =", max_side2)
print("2_minus_max_square_side_squared =", 2 - max_side2)
print("max_square_vertex_side_solution =", max_solution)
