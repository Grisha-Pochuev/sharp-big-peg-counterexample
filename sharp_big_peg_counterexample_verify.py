#!/usr/bin/env python3
"""
Exact, dependency-free verifier for a 10-vertex counterexample to
David Bernier's Sharp Polygonal Big Peg conjecture.

All mathematical predicates use Python integers/Fraction only.
No floating-point decision is used.

The polygon vertices are X[i] / D, in cyclic order.
The script verifies:
  (1) the polygon is simple, including non-overlap of adjacent edges;
  (2) the origin is in its bounded component;
  (3) every boundary segment has distance > 1 from the origin,
      hence the closed unit disk centered at the origin is contained inside;
  (4) every square with all four vertices on the polygon boundary has
      side length < sqrt(2).

For (4), label a square counterclockwise as
    c+u, c+J u, c-u, c-J u,
where J is rotation by +90 degrees.  For each of 10^4 ordered assignments
of the four square corners to polygon edges, the four supporting-line
conditions form a 4x4 linear system.  All arithmetic is exact.  A solution
is retained only if each corner lies on the assigned segment.
"""

from fractions import Fraction
from itertools import product

D = 1200
X = [
    ( 4114,  -558),
    ( 2022,  1568),
    (-1234,  1006),
    ( -868,  2516),
    (-1089,  2814),
    (-3769,  1169),
    (-3459,    81),
    (  141, -1348),
    (  571, -1449),
    ( 1105,  -485),
]
N = len(X)

EXPECTED_MIN_D2 = Fraction(2403854890969, 2400326560000)
EXPECTED_MAX_SIDE2 = Fraction(
    56381275521625791352241234309,
    28343589374868261752462760000,
)
EXPECTED_GAP = Fraction(
    305903228110732152684285691,
    28343589374868261752462760000,
)
EXPECTED_MAX_ASSIGNMENT = (2, 4, 5, 6)


def orient(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def on_segment(a, b, p):
    return (orient(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def segments_intersect(a, b, c, d):
    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    if o1 == 0 and on_segment(a, b, c):
        return True
    if o2 == 0 and on_segment(a, b, d):
        return True
    if o3 == 0 and on_segment(c, d, a):
        return True
    if o4 == 0 and on_segment(c, d, b):
        return True
    return ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0))


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def det4(M):
    s = 0
    for j in range(4):
        A = [[M[r][c] for c in range(4) if c != j] for r in range(1, 4)]
        s += (1 if j % 2 == 0 else -1) * M[0][j] * det3(A)
    return s


def replace_column(M, b, j):
    A = [row[:] for row in M]
    for i in range(4):
        A[i][j] = b[i]
    return A


def edge_distance_squared(i):
    """Exact squared distance from 0 to edge i, in physical coordinates."""
    ax, ay = X[i]
    bx, by = X[(i + 1) % N]
    ex, ey = bx - ax, by - ay
    e2 = ex * ex + ey * ey
    tnum = -(ax * ex + ay * ey)
    if 0 <= tnum <= e2:
        cr = ax * by - ay * bx
        return Fraction(cr * cr, e2 * D * D)
    return Fraction(min(ax * ax + ay * ay, bx * bx + by * by), D * D)


def build_square_system(assignment):
    M, b = [], []
    for k, e in enumerate(assignment):
        ax, ay = X[e]
        bx, by = X[(e + 1) % N]
        dx, dy = bx - ax, by - ay
        nx, ny = -dy, dx
        if k == 0:
            qx, qy = nx, ny
        elif k == 1:
            qx, qy = ny, -nx
        elif k == 2:
            qx, qy = -nx, -ny
        else:
            qx, qy = -ny, nx
        M.append([nx, ny, qx, qy])
        b.append(nx * ax + ny * ay)
    return M, b


# ---------------------------------------------------------------------------
# 1. Simple polygon
# ---------------------------------------------------------------------------
assert N <= 64
for i in range(N):
    assert X[i] != X[(i + 1) % N]

# Adjacent edges share one prescribed endpoint.  To rule out any additional
# overlap, check that each consecutive triple of vertices is non-collinear.
# Distinct supporting lines through the common endpoint can meet only there.
adjacent_turns = [
    orient(X[i], X[(i + 1) % N], X[(i + 2) % N])
    for i in range(N)
]
assert all(t != 0 for t in adjacent_turns), ("collinear adjacent edges", adjacent_turns)

# Every non-adjacent pair of closed edges is then checked for intersection.
for i in range(N):
    a, b = X[i], X[(i + 1) % N]
    for j in range(i + 1, N):
        if j == i + 1 or (i == 0 and j == N - 1):
            continue
        c, d = X[j], X[(j + 1) % N]
        assert not segments_intersect(a, b, c, d), ("self-intersection", i, j)


# ---------------------------------------------------------------------------
# 2. Origin lies inside: exact half-open positive-x ray crossing count
# ---------------------------------------------------------------------------
positive_ray_crossings = 0
for i in range(N):
    x1, y1 = X[i]
    x2, y2 = X[(i + 1) % N]
    if (y1 > 0) != (y2 > 0):
        num = x1 * y2 - x2 * y1
        den = y2 - y1
        if den < 0:
            num, den = -num, -den
        if num > 0:
            positive_ray_crossings += 1
assert positive_ray_crossings % 2 == 1


# ---------------------------------------------------------------------------
# 3. Unit disk centered at 0 is strictly inside
# ---------------------------------------------------------------------------
edge_d2 = [edge_distance_squared(i) for i in range(N)]
min_boundary_d2 = min(edge_d2)
assert min_boundary_d2 == EXPECTED_MIN_D2
assert min_boundary_d2 > 1


# ---------------------------------------------------------------------------
# 4. Exact exhaustive square enumeration
# ---------------------------------------------------------------------------
singular = []
valid_nonsingular = 0
positive_squares = 0
max_side2 = Fraction(0, 1)
max_assignment = None

for assignment in product(range(N), repeat=4):
    M, b = build_square_system(assignment)
    det = det4(M)
    if det == 0:
        singular.append(assignment)
        continue

    nums = [det4(replace_column(M, b, j)) for j in range(4)]
    if det < 0:
        det = -det
        nums = [-z for z in nums]
    cx, cy, ux, uy = nums

    corners = [
        (cx + ux, cy + uy),
        (cx - uy, cy + ux),
        (cx - ux, cy - uy),
        (cx + uy, cy - ux),
    ]

    ok = True
    for k, e in enumerate(assignment):
        ax, ay = X[e]
        bx, by = X[(e + 1) % N]
        ex, ey = bx - ax, by - ay
        e2 = ex * ex + ey * ey
        px, py = corners[k]
        sn = (px - ax * det) * ex + (py - ay * det) * ey
        if sn < 0 or sn > det * e2:
            ok = False
            break
    if not ok:
        continue

    valid_nonsingular += 1
    side2 = Fraction(2 * (ux * ux + uy * uy), det * det * D * D)
    if side2 > 0:
        positive_squares += 1
    if side2 > max_side2:
        max_side2 = side2
        max_assignment = assignment

expected_singular = [(i, i, i, i) for i in range(N)]
assert singular == expected_singular, singular
assert valid_nonsingular == 144
assert positive_squares == 4
assert max_assignment == EXPECTED_MAX_ASSIGNMENT
assert max_side2 == EXPECTED_MAX_SIDE2
assert 2 - max_side2 == EXPECTED_GAP
assert max_side2 < 2


print("PASS: exact Sharp Big Peg counterexample certificate")
print("vertices =", N)
print("common_coordinate_denominator =", D)
print("positive_ray_crossings =", positive_ray_crossings)
print("adjacent_turn_determinants =", adjacent_turns)
print("min_boundary_distance_squared =", min_boundary_d2)
print("min_boundary_distance_squared_decimal =", float(min_boundary_d2))
print("valid_nonsingular_edge_assignments =", valid_nonsingular)
print("positive_oriented_square_assignments =", positive_squares)
print("singular_assignments =", len(singular), "(only (i,i,i,i))")
print("max_square_edge_assignment =", max_assignment)
print("max_square_side_squared =", max_side2)
print("max_square_side_squared_decimal =", float(max_side2))
print("max_square_side_decimal =", float(max_side2) ** 0.5)
print("2_minus_max_square_side_squared =", 2 - max_side2)
