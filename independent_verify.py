#!/usr/bin/env python3
"""Independent exact cross-check for the Sharp Big Peg counterexample.

This checker intentionally differs from sharp_big_peg_counterexample_verify.py:
- exact Fraction Gaussian elimination instead of determinant/Cramer's rule;
- winding-number containment test instead of the positive-ray crossing test;
- segment membership checked by an exact affine parameter.

Only Python's standard library is used. No floating-point value decides a predicate.
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


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def orient(a, b, c):
    return cross(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1])


def point_on_segment(p, a, b):
    if orient(a, b, p) != 0:
        return False
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def closed_segments_intersect(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 == 0 and point_on_segment(c, a, b):
        return True
    if o2 == 0 and point_on_segment(d, a, b):
        return True
    if o3 == 0 and point_on_segment(a, c, d):
        return True
    if o4 == 0 and point_on_segment(b, c, d):
        return True
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)


def winding_number_origin():
    w = 0
    for i in range(N):
        a = X[i]
        b = X[(i + 1) % N]
        if a[1] <= 0 < b[1]:
            if orient(a, b, (0, 0)) > 0:
                w += 1
        elif b[1] <= 0 < a[1]:
            if orient(a, b, (0, 0)) < 0:
                w -= 1
    return w


def edge_distance2(i):
    a = X[i]
    b = X[(i + 1) % N]
    ex, ey = b[0] - a[0], b[1] - a[1]
    e2 = ex * ex + ey * ey
    proj_num = -(a[0] * ex + a[1] * ey)
    if 0 <= proj_num <= e2:
        area2 = cross(a[0], a[1], b[0], b[1])
        return Fraction(area2 * area2, e2 * D * D)
    da = a[0] * a[0] + a[1] * a[1]
    db = b[0] * b[0] + b[1] * b[1]
    return Fraction(min(da, db), D * D)


def build_system(assignment):
    rows = []
    rhs = []
    for k, e in enumerate(assignment):
        ax, ay = X[e]
        bx, by = X[(e + 1) % N]
        dx, dy = bx - ax, by - ay
        nx, ny = -dy, dx
        if k == 0:
            uxcoef, uycoef = nx, ny
        elif k == 1:
            uxcoef, uycoef = ny, -nx
        elif k == 2:
            uxcoef, uycoef = -nx, -ny
        else:
            uxcoef, uycoef = -ny, nx
        rows.append([Fraction(nx), Fraction(ny), Fraction(uxcoef), Fraction(uycoef)])
        rhs.append(Fraction(nx * ax + ny * ay))
    return rows, rhs


def solve_4x4(A, b):
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    n = 4
    for col in range(n):
        pivot = next((r for r in range(col, n) if M[r][col] != 0), None)
        if pivot is None:
            return None
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        pv = M[col][col]
        M[col] = [z / pv for z in M[col]]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if f != 0:
                M[r] = [M[r][j] - f * M[col][j] for j in range(n + 1)]
    return tuple(M[i][n] for i in range(n))


def corner_points(sol):
    cx, cy, ux, uy = sol
    return (
        (cx + ux, cy + uy),
        (cx - uy, cy + ux),
        (cx - ux, cy - uy),
        (cx + uy, cy - ux),
    )


def fraction_point_on_grid_segment(p, e):
    a = X[e]
    b = X[(e + 1) % N]
    ex, ey = b[0] - a[0], b[1] - a[1]
    if Fraction(ex) * (p[1] - a[1]) - Fraction(ey) * (p[0] - a[0]) != 0:
        return False
    if ex != 0:
        t = (p[0] - a[0]) / ex
    else:
        t = (p[1] - a[1]) / ey
    return 0 <= t <= 1


# A. simple polygon
assert N == 10 and N <= 64
for i in range(N):
    assert X[i] != X[(i + 1) % N]
adjacent_turns = [orient(X[i], X[(i + 1) % N], X[(i + 2) % N]) for i in range(N)]
assert all(t != 0 for t in adjacent_turns)
for i in range(N):
    for j in range(i + 1, N):
        if j == i + 1 or (i == 0 and j == N - 1):
            continue
        assert not closed_segments_intersect(X[i], X[(i + 1) % N], X[j], X[(j + 1) % N])

# B. origin in bounded component
w = winding_number_origin()
assert w != 0

# C. closed unit disk contained
edge_d2 = [edge_distance2(i) for i in range(N)]
min_d2 = min(edge_d2)
assert min_d2 == EXPECTED_MIN_D2
assert min_d2 > 1

# D. all boundary-inscribed squares
singular = []
valid = 0
positive = []
max_side2 = Fraction(0)
max_assignment = None
for assignment in product(range(N), repeat=4):
    A, b = build_system(assignment)
    sol = solve_4x4(A, b)
    if sol is None:
        singular.append(assignment)
        continue
    corners = corner_points(sol)
    if not all(fraction_point_on_grid_segment(corners[k], assignment[k]) for k in range(4)):
        continue
    valid += 1
    ux, uy = sol[2], sol[3]
    side2 = Fraction(2, D * D) * (ux * ux + uy * uy)
    if side2 > 0:
        positive.append((assignment, side2))
    if side2 > max_side2:
        max_side2 = side2
        max_assignment = assignment

assert singular == [(i, i, i, i) for i in range(N)]
assert valid == 144
assert len(positive) == 4
assert [a for a, _ in positive] == [
    (2, 4, 5, 6),
    (4, 5, 6, 2),
    (5, 6, 2, 4),
    (6, 2, 4, 5),
]
assert max_assignment == EXPECTED_MAX_ASSIGNMENT
assert max_side2 == EXPECTED_MAX_SIDE2
assert 2 - max_side2 == EXPECTED_GAP
assert max_side2 < 2

print("PASS: independent exact cross-check")
print("winding_number =", w)
print("adjacent_turn_determinants =", adjacent_turns)
print("min_boundary_distance_squared =", min_d2)
print("valid_nonsingular_edge_assignments =", valid)
print("positive_oriented_square_assignments =", len(positive))
print("singular_assignments =", len(singular))
print("max_square_edge_assignment =", max_assignment)
print("max_square_side_squared =", max_side2)
print("2_minus_max_square_side_squared =", 2 - max_side2)
