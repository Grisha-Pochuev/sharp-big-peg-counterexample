# Sharp Big Peg: an exact 10-vertex counterexample

[![Exact verification](https://github.com/Grisha-Pochuev/sharp-big-peg-counterexample/actions/workflows/verify.yml/badge.svg)](https://github.com/Grisha-Pochuev/sharp-big-peg-counterexample/actions/workflows/verify.yml)

This repository gives an explicit **10-vertex counterexample** to David Bernier's **Sharp Polygonal Big Peg conjecture**, together with a deterministic verifier using exact integer/rational arithmetic.

The original challenge was posted by David Bernier on June 16, 2026:

https://dbernier.ca/2026/06/16/the-sharp-big-peg-conjecture/

## The problem

Let `Q` be a simple closed polygonal curve whose bounded component contains a disk of radius `1`. The Sharp Polygonal Big Peg conjecture asserts that `Q` must have a square whose four vertices lie on the boundary of `Q` and whose side length is at least `sqrt(2)`.

Bernier's challenge asks for an explicit counterexample with at most 64 polygon vertices, together with a rigorous exact or certified verification that every boundary-inscribed square has side length strictly less than `sqrt(2)`.

## Result

We give such a counterexample using only **10 vertices**.

Let `D = 1200`. In cyclic order, take

| i | `D * x_i` | `D * y_i` |
|---|---:|---:|
| 0 | 4114 | -558 |
| 1 | 2022 | 1568 |
| 2 | -1234 | 1006 |
| 3 | -868 | 2516 |
| 4 | -1089 | 2814 |
| 5 | -3769 | 1169 |
| 6 | -3459 | 81 |
| 7 | 141 | -1348 |
| 8 | 571 | -1449 |
| 9 | 1105 | -485 |

Thus `v_i = (x_i,y_i) = (X_i,Y_i)/1200`. Join consecutive vertices and join `v_9` back to `v_0`.

The exact certificate establishes:

1. the polygon is simple;
2. the origin lies in its bounded component;
3. every boundary segment is at distance strictly greater than `1` from the origin, so the closed unit disk centered at the origin is contained in the polygon;
4. every square whose four vertices lie on the polygon boundary has side length strictly less than `sqrt(2)`.

The minimum squared distance from the origin to the polygon boundary is

```text
2403854890969 / 2400326560000
= 1.0014699378942005... > 1.
```

The largest boundary-inscribed square has exact squared side length

```text
56381275521625791352241234309
-----------------------------------------------
28343589374868261752462760000
= 1.9892073221896882... < 2.
```

In particular,

```text
2 - L^2 =
305903228110732152684285691
-----------------------------------------------
28343589374868261752462760000
> 0,
```

so `L < sqrt(2)`.

## Why the square search is exhaustive

Write an oriented square as

```text
c + u,   c + J u,   c - u,   c - J u,
```

where `c` is the center and `J` is rotation through 90 degrees.

Assign, in cyclic order, each of the four square corners to one of the ten polygon edges. There are exactly

```text
10^4 = 10000
```

ordered assignments.

For a fixed assignment, requiring each square corner to lie on the supporting line of its assigned edge gives four linear equations in the four real unknowns

```text
c_x, c_y, u_x, u_y.
```

For every nonsingular assignment there is therefore at most one square. The verifier solves every such system exactly by integer determinants, then checks exactly whether each corner lies on the assigned **segment**, not merely on its supporting line.

The exhaustive calculation finds:

```text
10000 total ordered edge assignments
10 singular assignments
144 nonsingular solutions with all four corners on their assigned segments
4 positive-side oriented solutions
```

The four positive solutions are the four cyclic labelings of one geometric square. Its edge assignment is `(2,4,5,6)` up to cyclic relabeling.

The only singular assignments are `(i,i,i,i)` for `i = 0,...,9`; all four corners would then lie on one line, so none can represent a nondegenerate square.

This enumeration also covers squares having a corner exactly at a polygon vertex: such a point lies on either adjacent segment, and all ordered segment assignments are enumerated.

A fuller mathematical account is in [`SOLUTION.md`](SOLUTION.md).

## Independent verification

The certificate is deliberately designed so that it does **not** require trusting floating-point geometry, numerical optimization, a proprietary solver, or any third-party Python package.

Requirements:

- Python 3;
- the Python standard library only.

Run:

```bash
python3 verify.py
```

Expected final certificate data:

```text
PASS: exact Sharp Big Peg counterexample certificate
vertices = 10
common_coordinate_denominator = 1200
positive_ray_crossings = 1
min_boundary_distance_squared = 2403854890969/2400326560000
valid_nonsingular_edge_assignments = 144
positive_oriented_square_assignments = 4
singular_assignments = 10 (only (i,i,i,i))
max_square_edge_assignment = (2, 4, 5, 6)
max_square_side_squared = 56381275521625791352241234309/28343589374868261752462760000
2_minus_max_square_side_squared = 305903228110732152684285691/28343589374868261752462760000
```

Every mathematical decision in `verify.py` uses Python integers or `fractions.Fraction`. Floating point is used only to print human-readable decimal approximations *after* the exact assertions have passed.

### Verification without trusting this repository's calculations

An independent reviewer can reimplement the certificate from scratch using only the data in [`counterexample.json`](counterexample.json) and the mathematical procedure in [`SOLUTION.md`](SOLUTION.md):

1. test all non-adjacent polygon-edge pairs for intersection using orientation determinants;
2. use an exact ray-crossing test to verify that the origin is inside;
3. compute the exact point-to-segment distance for each of the ten edges and verify every value is greater than `1`;
4. enumerate all `10^4` ordered assignments of square corners to polygon edges;
5. solve the resulting four-by-four linear system for each assignment with exact rational arithmetic;
6. retain a solution only when every corner lies on its assigned closed segment;
7. compare the squared side length of every retained nondegenerate square with `2`.

No heuristic or tolerance choice enters this verification.

## Automatic verification

The GitHub Actions workflow [`verify.yml`](.github/workflows/verify.yml) runs the exact verifier automatically on pushes and pull requests. A green workflow therefore means that the repository's published certificate has been reproduced from a clean Python environment.

This is useful as a reproducibility check, but the workflow is not a substitute for inspecting the short mathematical argument and the verifier itself.

## Repository contents

- [`README.md`](README.md) — problem, counterexample, headline certificate, and reproduction instructions.
- [`SOLUTION.md`](SOLUTION.md) — detailed mathematical argument explaining why the finite computation is exhaustive.
- [`verify.py`](verify.py) — dependency-free exact verifier.
- [`counterexample.json`](counterexample.json) — machine-readable polygon data and claimed exact invariants.
- [`.github/workflows/verify.yml`](.github/workflows/verify.yml) — automatic clean-environment verification.

## Reproducibility principles

The verifier is:

- **deterministic** — no random choices;
- **exhaustive** — all 10,000 ordered edge assignments are considered;
- **exact** — no floating-point predicate decides correctness;
- **dependency-free** — only the Python standard library is needed;
- **small enough to audit** — the complete checker is a single source file.

## Citation / contact

Repository maintained by **Grisha Pochuev**.

If you independently verify the result, find an error, or produce a second implementation of the certificate, opening an issue in this repository is welcome.
