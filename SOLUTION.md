# A 10-vertex counterexample to the Sharp Polygonal Big Peg conjecture

## Statement refuted

Let `Q` be a simple closed polygonal curve whose bounded component contains a disk of radius 1. The Sharp Polygonal Big Peg conjecture asserts that `Q` has a boundary-inscribed square of side at least `sqrt(2)`.

The polygon below is a counterexample.

## The polygon

Let `D = 1200` and take, in cyclic order,

\[
\begin{aligned}
v_0&=(4114,-558)/1200,\\
v_1&=(2022,1568)/1200,\\
v_2&=(-1234,1006)/1200,\\
v_3&=(-868,2516)/1200,\\
v_4&=(-1089,2814)/1200,\\
v_5&=(-3769,1169)/1200,\\
v_6&=(-3459,81)/1200,\\
v_7&=(141,-1348)/1200,\\
v_8&=(571,-1449)/1200,\\
v_9&=(1105,-485)/1200.
\end{aligned}
\]

Join consecutive vertices and join `v_9` back to `v_0`.

## 1. Simplicity and the unit disk

All pairwise non-adjacent edge intersection tests are evaluated exactly with integer orientation determinants. None intersect, so the polygon is simple.

The positive horizontal ray from the origin crosses the boundary exactly once, hence the origin belongs to the bounded component.

For each edge, the squared distance from the origin to the segment is computed exactly. The minimum is attained on edge `v_6 v_7` and equals

\[
\frac{2403854890969}{2400326560000}
=1.0014699378942005\ldots >1.
\]

Thus the entire boundary is strictly outside the closed unit disk centered at the origin. Since the origin is inside the polygon and the disk is connected, the whole closed unit disk lies in the bounded component.

## 2. Exhaustion of all boundary-inscribed squares

Write an oriented square as

\[
c+u,\qquad c+Ju,\qquad c-u,\qquad c-Ju,
\]

where `J` is rotation by 90 degrees.

Assign the four square corners, in this order, to four polygon edges. There are

\[
10^4=10000
\]

ordered edge assignments. For a fixed assignment, the requirement that a given corner lie on the supporting line of its assigned edge is linear in the four unknown real coordinates of `c` and `u`. Therefore each assignment gives a 4 by 4 linear system.

The accompanying verifier performs the entire calculation with exact integer/rational arithmetic:

* exactly 10 assignments are singular, namely `(i,i,i,i)` for `i=0,...,9`; these put all four corners on a single line and cannot contain a nondegenerate square;
* among all nonsingular assignments, 144 solutions have all four corners on their assigned **segments** (rather than merely their supporting lines);
* only four of those 144 have positive side length, and these four are just the four cyclic labelings of the same geometric square;
* its edge assignment is `(2,4,5,6)` up to cyclic relabeling.

The exact squared side length of the largest (indeed unique nondegenerate) boundary-inscribed square is

\[
L^2=
\frac{56381275521625791352241234309}
     {28343589374868261752462760000}
=1.9892073221896882\ldots .
\]

Moreover

\[
2-L^2=
\frac{305903228110732152684285691}
     {28343589374868261752462760000}>0.
\]

Hence

\[
L<\sqrt2,
\]

numerically

\[
L=1.4103926127818764\ldots < 1.4142135623730951\ldots .
\]

Therefore this ten-vertex polygon contains a unit disk but has no boundary-inscribed square of side at least `sqrt(2)`. It is a counterexample to the Sharp Polygonal Big Peg conjecture.

## Verification

Run

```bash
python sharp_big_peg_counterexample_verify.py
```

The verifier is dependency-free and uses exact Python integers and `fractions.Fraction` for every mathematical predicate. Floating point is used only when printing decimal approximations after all exact assertions have passed.
