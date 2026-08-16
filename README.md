# Sharp Big Peg: an exact 10-vertex counterexample

[![Exact verification](https://github.com/Grisha-Pochuev/sharp-big-peg-counterexample/actions/workflows/verify.yml/badge.svg)](https://github.com/Grisha-Pochuev/sharp-big-peg-counterexample/actions/workflows/verify.yml)

This repository contains an explicit **10-vertex counterexample** to David Bernier's **Sharp Polygonal Big Peg conjecture**, together with exact, reproducible verification code and multiple independently implemented cross-checks.

David Bernier stated the challenge and offered a **$200 prize** for an explicit counterexample with at most 64 vertices:

https://dbernier.ca/2026/06/16/the-sharp-big-peg-conjecture/

## Problem

Let `Q` be a simple closed polygonal curve whose bounded component contains a disk of radius `1`. The Sharp Polygonal Big Peg conjecture asserts that `Q` has a square whose four vertices lie on the boundary of `Q` and whose side length is at least `sqrt(2)`.

A counterexample therefore needs to satisfy all of the following:

1. `Q` is a simple closed polygonal curve;
2. its bounded component contains a unit disk;
3. every square with all four vertices on the boundary has side length strictly less than `sqrt(2)`.

The construction here uses only **10 vertices**, well below the 64-vertex limit.

## Counterexample

Let `D = 1200`. In cyclic order, take

| i | `D x_i` | `D y_i` |
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

Thus `v_i = (X_i,Y_i)/1200`. Join consecutive vertices and join `v_9` back to `v_0`.

The mathematical write-up is in [`SOLUTION.md`](SOLUTION.md). A strengthened article source is also kept in the repository once released.

## Exact certificate

The exact verification establishes:

- the polygon is simple;
- adjacent edges have no overlap beyond their prescribed common endpoint;
- the origin belongs to the bounded component;
- every boundary segment is at distance strictly greater than `1` from the origin, so the closed unit disk centered at the origin is contained inside;
- all possible boundary-inscribed squares are exhausted by a finite exact calculation;
- the largest such square has side strictly less than `sqrt(2)`.

The ten consecutive-triple orientation determinants are

```text
[8097960, -4710868, 442778, 1162185, 3425790,
 3473810, 250870, 468454, -2939658, 6244418]
```

Every value is nonzero. Hence each pair of adjacent edges has distinct supporting lines and can meet only at its prescribed common endpoint. All 35 unordered pairs of non-adjacent edges are separately tested for closed-segment intersection.

The minimum squared distance from the origin to the boundary is

```text
2403854890969 / 2400326560000
= 1.0014699378942005... > 1.
```

The exact squared side length of the largest boundary-inscribed square is

```text
56381275521625791352241234309
-----------------------------------------------
28343589374868261752462760000
= 1.9892073221896882... < 2.
```

Equivalently,

```text
2 - L^2 =
305903228110732152684285691
-----------------------------------------------
28343589374868261752462760000
> 0.
```

Hence `L < sqrt(2)` exactly, not merely numerically.

## Why the square enumeration is exhaustive

Write an oriented square in cyclic order as

```text
c + u,  c + J u,  c - u,  c - J u,
```

where `J` is rotation by 90 degrees.

Each of the four square corners lies on one of the ten closed polygon edges. Therefore every square determines at least one ordered edge assignment

```text
(e0, e1, e2, e3) in {0,...,9}^4.
```

There are exactly `10^4 = 10000` such assignments.

For each assignment, the condition that each corner lie on the supporting line of its assigned edge gives a `4 x 4` linear system in the four unknown coordinates of `c` and `u`. For every nonsingular assignment there is at most one candidate. The candidate is retained only if every corner lies on its assigned **closed segment**, not merely its supporting line.

A square corner exactly at a polygon vertex is not missed: that point belongs to the two adjacent closed edges, and all ordered edge assignments are enumerated.

The exact calculation gives

```text
10000 total ordered edge assignments
10 singular assignments
144 nonsingular solutions with all four corners on the assigned segments
4 positive-side oriented square assignments
```

The singular assignments are exactly `(i,i,i,i)` for `i=0,...,9`. They require all four square corners to lie on one supporting line and therefore cannot contain a nondegenerate square.

The four positive assignments are

```text
(2,4,5,6)
(4,5,6,2)
(5,6,2,4)
(6,2,4,5)
```

and are cyclic labelings of one geometric square.

## Primary exact verifier

The primary certificate is

[`sharp_big_peg_counterexample_verify.py`](sharp_big_peg_counterexample_verify.py).

It is dependency-free and uses Python integers and `fractions.Fraction` for every mathematical decision. It uses exact determinants and Cramer's rule for the square systems.

Run:

```bash
python3 sharp_big_peg_counterexample_verify.py
```

A successful run begins with

```text
PASS: exact Sharp Big Peg counterexample certificate
```

The verifier now **asserts**, rather than merely prints, the central audit invariants:

- the exact minimum boundary distance;
- all ten nonzero adjacent-turn determinants;
- exactly 144 segment-valid nonsingular assignments;
- exactly 4 positive-side assignments;
- maximum assignment `(2,4,5,6)`;
- the exact rational value of the maximum squared side;
- the exact positive gap `2-L^2`.

## Independent cross-check 1: Gaussian elimination

[`independent_verify.py`](independent_verify.py) retains the center/offset square parametrization but intentionally changes several implementations:

- exact `Fraction` Gaussian elimination instead of determinant/Cramer's-rule solving;
- an exact winding-number test for the origin instead of the primary ray-crossing implementation;
- an exact affine-parameter segment test;
- its own exact checks of adjacent and non-adjacent edge behavior.

Run:

```bash
python3 independent_verify.py
```

It ends with

```text
PASS: independent exact cross-check
```

## Independent cross-check 2: different square parametrization

A third verifier was added specifically to reduce the risk of a shared error in the central square-system derivation:

[`independent_vertex_side_verify.py`](independent_vertex_side_verify.py).

Unlike the first two programs, it does **not** describe a square by its center `c` and offset `u`. It uses a first corner `P` and a side vector `S`:

```text
P0 = P
P1 = P + S
P2 = P + S + J S
P3 = P + J S
```

Its `4 x 4` systems therefore use different unknowns and different coefficient formulas. Exact rational row reduction independently reproduces:

```text
10 singular assignments, exactly (i,i,i,i)
0 inconsistent singular systems
144 segment-valid nonsingular assignments
4 positive-side assignments
maximum assignment (2,4,5,6)
exactly the same maximum squared side
exactly the same positive gap 2-L^2
```

It also verifies that the four positive assignments give the same unordered set of four corners.

Run:

```bash
python3 independent_vertex_side_verify.py
```

A successful run begins with

```text
PASS: independent vertex/side exact cross-check
```

## Verification from scratch

A reviewer does not need to trust any supplied Python implementation. The raw construction and claimed exact invariants are provided in [`counterexample.json`](counterexample.json).

A fresh implementation can independently:

1. read the ten rational vertices;
2. check every consecutive triple is non-collinear, so adjacent edges do not overlap;
3. test all 35 non-adjacent edge pairs for intersection using exact arithmetic;
4. verify that the origin is in the bounded component;
5. compute the exact distance from the origin to each polygon segment and verify that the minimum squared distance is greater than `1`;
6. enumerate all `10^4` ordered assignments of four square corners to ten polygon edges;
7. for each assignment, solve the four supporting-line equations exactly;
8. retain a candidate only when all four corners lie on their assigned closed segments;
9. classify the singular assignments explicitly;
10. compare the exact squared side length of every nondegenerate retained square with `2`.

No numerical tolerance, random search, nonlinear optimizer, SAT solver, proprietary software, or third-party Python package is required.

## Automatic clean-environment verification

GitHub Actions runs **all three exact implementations** on pushes and pull requests under Python 3.10, 3.12, and 3.13:

[`.github/workflows/verify.yml`](.github/workflows/verify.yml)

The badge at the top of this README links to the current runs. A green workflow means that the three published certificates executed successfully from fresh GitHub-hosted environments on all configured Python versions.

## Repository contents

- [`SOLUTION.md`](SOLUTION.md) - mathematical solution from the original project sources.
- [`sharp_big_peg_counterexample_verify.py`](sharp_big_peg_counterexample_verify.py) - primary exact dependency-free certificate.
- [`independent_verify.py`](independent_verify.py) - second exact implementation using Gaussian elimination and alternate geometric predicates.
- [`independent_vertex_side_verify.py`](independent_vertex_side_verify.py) - third exact implementation using a different square parametrization.
- [`counterexample.json`](counterexample.json) - machine-readable construction and strengthened exact invariants.
- [`.github/workflows/verify.yml`](.github/workflows/verify.yml) - clean-environment execution of all three verifiers.

## Reproducibility properties

The verification is designed to be:

- **exact** - correctness does not depend on floating-point comparisons;
- **exhaustive** - all 10,000 ordered edge assignments are considered;
- **deterministic** - no randomness is involved;
- **dependency-free** - the Python standard library is sufficient;
- **auditable** - the construction, derivation, code, and exact output values are public;
- **independently reproducible** - raw rational data are separated from the implementations;
- **cross-checked at the model level** - the third verifier uses a different parametrization of a square, not merely a different linear solver.

## Audit hardening

An adversarial review identified two places where the original public certificate could be made stronger even though independent recomputation did not invalidate the counterexample:

1. adjacent-edge non-overlap had been stated in the write-up but was not explicitly asserted by the primary program;
2. the first two square verifiers shared the same center/offset square parametrization.

The current version closes both weaknesses: adjacent-edge behavior is now checked exactly, and the vertex/side verifier supplies a separate derivation of the central finite systems. The primary verifier also asserts the claimed enumeration counts and exact maximum rather than only printing them.

## Author

Repository maintained by **Grisha Pochuev**.

Independent checks, alternative implementations, bug reports, and mathematical criticism are welcome through GitHub issues.
