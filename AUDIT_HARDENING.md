# Adversarial audit hardening

This note records the two concrete weaknesses identified during an adversarial review of the first public verification package and how the current repository addresses them.

## 1. Adjacent-edge overlap

The first verifier tested all 35 unordered pairs of non-adjacent polygon edges for intersection, but adjacent edges were skipped because they share their prescribed endpoint. That was not, by itself, enough to exclude a collinear overlap between two consecutive edges.

The strengthened verifiers now compute

```text
orient(X_i, X_{i+1}, X_{i+2})
```

for every `i` modulo 10. The exact values are

```text
[8097960, -4710868, 442778, 1162185, 3425790,
 3473810, 250870, 468454, -2939658, 6244418]
```

Every value is nonzero. Therefore each adjacent pair has distinct supporting lines and can meet only at its prescribed common endpoint. Together with the 35 exact non-adjacent intersection checks, this closes the simplicity certificate.

## 2. Shared square parametrization

The original primary verifier and the first independent cross-check both used the center/offset representation

```text
c + u, c + Ju, c - u, c - Ju.
```

Although they used different linear solvers and different auxiliary geometric tests, an error in the shared derivation of the central 4x4 systems could in principle have survived both programs.

The repository now contains [`independent_vertex_side_verify.py`](independent_vertex_side_verify.py), which instead represents a square by a first corner `P` and a side vector `S`:

```text
P0 = P
P1 = P + S
P2 = P + S + J S
P3 = P + J S
```

This produces a separately derived family of 4x4 linear systems in the unknowns `(x,y,sx,sy)`. Exact rational row reduction independently reproduces:

```text
10000 total ordered edge assignments
10 singular assignments, exactly (i,i,i,i)
0 inconsistent singular systems
144 segment-valid nonsingular assignments
4 positive-side assignments
positive assignments:
  (2,4,5,6)
  (4,5,6,2)
  (5,6,2,4)
  (6,2,4,5)
```

and the same exact maximum

```text
56381275521625791352241234309
-----------------------------------------------
28343589374868261752462760000
```

with the same positive gap

```text
305903228110732152684285691
-----------------------------------------------
28343589374868261752462760000.
```

It also verifies that the four positive assignments are cyclic relabelings of the same unordered set of four square corners.

## 3. Stronger assertions

The primary verifier now asserts, rather than merely prints:

- the exact minimum squared boundary distance;
- all ten nonzero adjacent-turn determinants;
- exactly 144 segment-valid nonsingular assignments;
- exactly 4 positive-side assignments;
- the maximizing edge assignment `(2,4,5,6)`;
- the exact maximum squared side;
- the exact positive value of `2-L^2`.

## 4. Clean-environment reproduction

The strengthened verification package is pinned by commit

```text
26dcb8e54b0b18215fa37ff48cba26696658b552
```

GitHub Actions successfully ran all three exact verifiers at that commit on Python 3.10, 3.12, and 3.13.

The audit did not find a counterexample to the certificate. These changes are defensive hardening intended to reduce the number of assumptions a reviewer must take on trust.
