# Sharp Big Peg: an exact 10-vertex counterexample

[![Exact verification](https://github.com/Grisha-Pochuev/sharp-big-peg-counterexample/actions/workflows/verify.yml/badge.svg)](https://github.com/Grisha-Pochuev/sharp-big-peg-counterexample/actions/workflows/verify.yml)

This repository contains an explicit **10-vertex counterexample** to David Bernier's **Sharp Polygonal Big Peg conjecture**, together with exact, reproducible verification code.

David Bernier stated the challenge and offered a **$200 prize** for an explicit counterexample with at most 64 vertices:

https://dbernier.ca/2026/06/16/the-sharp-big-peg-conjecture/

## Problem

Let `Q` be a simple closed polygonal curve whose bounded component contains a disk of radius `1`. The Sharp Polygonal Big Peg conjecture asserts that `Q` has a square whose four vertices lie on the boundary of `Q` and whose side length is at least `sqrt(2)`.

A counterexample therefore needs to satisfy all of the following:

1. `Q` is a simple closed polygonal curve;
2. its bounded component contains a unit disk;
3. every square with all four vertices on the boundary has side length strictly less than `sqrt(2)`.

The construction in this repository uses only **10 vertices**, well below the 64-vertex limit.

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

Thus

```text
v_i = (x_i, y_i) = (X_i, Y_i) / 1200.
```

Join consecutive vertices and join `v_9` back to `v_0`.

The full mathematical write-up is in [`SOLUTION.md`](SOLUTION.md). That file is the solution prepared in the project and is kept as the primary proof description.

## Exact certificate

The exact verification establishes:

- the polygon is simple;
- the origin belongs to its bounded component;
- every boundary segment is at distance strictly greater than `1` from the origin, so the closed unit disk centered at the origin is contained inside;
- all possible boundary-inscribed squares are exhausted by a finite exact calculation;
- the largest such square has side strictly less than `sqrt(2)`.

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

Hence `L < sqrt(2)`.

## Why the square enumeration is exhaustive

Write an oriented square in cyclic order as

```text
c + u,  c + J u,  c - u,  c - J u,
```

where `J` is rotation by 90 degrees.

Each of the four square corners lies on one of the ten polygon edges. Therefore every square determines at least one ordered edge assignment

```text
(e0, e1, e2, e3) in {0,...,9}^4.
```

There are exactly

```text
10^4 = 10000
```

such assignments.

For each assignment, the condition that each corner lie on the supporting line of its assigned edge gives a `4 x 4` linear system in the four unknown coordinates of `c` and `u`. For every nonsingular assignment there is at most one candidate. The candidate is retained only if every corner lies on its assigned **closed segment**, not merely its supporting line.

A square corner that lies exactly at a polygon vertex is not missed: that point belongs to the two adjacent closed edges, and all ordered edge assignments are enumerated.

The exact calculation gives:

```text
10000 total ordered edge assignments
10 singular assignments
144 nonsingular solutions with all four corners on the assigned segments
4 positive-side oriented square assignments
```

The ten singular assignments are exactly `(i,i,i,i)`, `i=0,...,9`. They require all four square corners to lie on one line and therefore cannot contain a nondegenerate square.

The four positive assignments are cyclic labelings of the same geometric square. One labeling is `(2,4,5,6)`.

## Reproduce the original verification

The primary verifier is the original project file:

[`sharp_big_peg_counterexample_verify.py`](sharp_big_peg_counterexample_verify.py)

It is dependency-free and uses only Python integers and `fractions.Fraction` for mathematical decisions. Floating point is used only for decimal output after all exact assertions have passed.

Requirements: **Python 3 and the standard library only.**

Run:

```bash
python3 sharp_big_peg_counterexample_verify.py
```

A successful run starts with

```text
PASS: exact Sharp Big Peg counterexample certificate
```

and reports, among other values,

```text
vertices = 10
positive_ray_crossings = 1
min_boundary_distance_squared = 2403854890969/2400326560000
valid_nonsingular_edge_assignments = 144
positive_oriented_square_assignments = 4
singular_assignments = 10 (only (i,i,i,i))
max_square_edge_assignment = (2, 4, 5, 6)
max_square_side_squared = 56381275521625791352241234309/28343589374868261752462760000
2_minus_max_square_side_squared = 305903228110732152684285691/28343589374868261752462760000
```

## Independent cross-check

For additional protection against an implementation-specific error, the repository also contains a second exact implementation:

[`independent_verify.py`](independent_verify.py)

It intentionally uses different computational choices from the primary verifier:

- **exact Gaussian elimination with `Fraction`** instead of determinant/Cramer's-rule solving;
- an **exact winding-number test** for the origin instead of the primary positive-ray crossing implementation;
- an **exact affine-parameter segment test** for candidate corners.

Run:

```bash
python3 independent_verify.py
```

It independently reproduces the same critical exact invariants and ends with

```text
PASS: independent exact cross-check
```

This second implementation is not logically necessary for the certificate, but agreement between two structurally different exact implementations makes accidental implementation error easier to detect.

## Verification from scratch

A reviewer does not need to trust either Python program. The raw construction and claimed exact invariants are also provided in machine-readable form:

[`counterexample.json`](counterexample.json)

A fresh implementation can independently do the following:

1. read the ten rational vertices;
2. test all non-adjacent polygon edges for intersection using exact arithmetic;
3. verify that the origin is in the bounded component;
4. compute the exact distance from the origin to each polygon segment and verify that the minimum squared distance is greater than `1`;
5. enumerate all `10^4` ordered assignments of four square corners to ten polygon edges;
6. for each assignment, solve the four supporting-line equations exactly;
7. retain the candidate only when all four corners lie on their assigned closed segments;
8. check that the only singular assignments are `(i,i,i,i)`;
9. compare the exact squared side length of every nondegenerate retained square with `2`.

No numerical tolerance, random search, nonlinear optimizer, SAT solver, proprietary software, or third-party Python package is required.

## Automatic clean-environment verification

GitHub Actions runs **both exact implementations** automatically on pushes and pull requests, under Python 3.10, 3.12, and 3.13:

[`.github/workflows/verify.yml`](.github/workflows/verify.yml)

The badge at the top of this README links to those runs. A green run means that both published checkers executed successfully from a fresh GitHub-hosted environment on all configured Python versions.

The automated run is a reproducibility aid; the proof of completeness of the finite enumeration is explained in [`SOLUTION.md`](SOLUTION.md) and above so that the checker itself can be audited or independently reimplemented.

## Repository contents

- [`SOLUTION.md`](SOLUTION.md) — mathematical solution from the project sources.
- [`sharp_big_peg_counterexample_verify.py`](sharp_big_peg_counterexample_verify.py) — original exact dependency-free verification certificate from the project sources.
- [`independent_verify.py`](independent_verify.py) — second exact implementation using a different linear-system solver and containment test.
- [`counterexample.json`](counterexample.json) — machine-readable construction and exact certificate values.
- [`.github/workflows/verify.yml`](.github/workflows/verify.yml) — automatic reproduction of both verifiers.

## Reproducibility properties

The verification is designed to be:

- **exact** — correctness does not depend on floating-point comparisons;
- **exhaustive** — all 10,000 ordered edge assignments are considered;
- **deterministic** — no randomness is involved;
- **dependency-free** — standard Python is sufficient;
- **auditable** — the construction, proof description, code, and exact output values are all public;
- **independently reproducible** — the raw rational data are separated from the implementation.

## Author and contact

Repository maintained by **Grisha Pochuev**.

Independent checks, alternative implementations, bug reports, and mathematical criticism are welcome through GitHub issues.
