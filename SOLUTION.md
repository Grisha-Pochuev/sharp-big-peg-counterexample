# A 10-vertex counterexample to the Sharp Polygonal Big Peg conjecture

## 1. Statement refuted

Let `Q` be a simple closed polygonal curve whose bounded component contains a disk of radius `1`. The Sharp Polygonal Big Peg conjecture asserts that `Q` has a boundary-inscribed square of side at least `sqrt(2)`.

The polygon below is a counterexample.

## 2. The polygon

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

All coordinates are rational. Consequently every predicate used below can be reduced to exact integer or rational arithmetic.

## 3. Simplicity

For points `a,b,c`, define the orientation determinant

\[
\operatorname{orient}(a,b,c)
=(b_x-a_x)(c_y-a_y)-(b_y-a_y)(c_x-a_x).
\]

Two non-adjacent closed segments can be tested for intersection using only signs and zeros of such determinants, together with exact coordinate comparisons in the collinear cases.

There are only ten edges. The verifier tests every pair of non-adjacent edges exactly and finds no intersection. Consecutive vertices are distinct, and consecutive edge directions are non-collinear for this polygon, so adjacent edges meet only at their common endpoint.

Hence the polygonal curve is simple.

## 4. The unit disk lies inside

### 4.1 The origin is inside

Use the positive horizontal ray from the origin. An exact half-open crossing test counts one positive-ray boundary crossing. Therefore the origin lies in the bounded component of the simple polygon.

### 4.2 The boundary stays outside the closed unit disk

For an edge from `a` to `b`, let `e=b-a`. If the perpendicular projection of the origin onto the supporting line lies on the segment, the squared distance is

\[
\frac{(a_xb_y-a_yb_x)^2}{\lVert e\rVert^2 D^2}.
\]

Otherwise it is the smaller of the squared distances from the origin to the two endpoints. The verifier evaluates this exactly for every edge.

The minimum occurs on edge `v_6v_7` and equals

\[
\frac{2403854890969}{2400326560000}
=1.0014699378942005\ldots>1.
\]

Thus the polygon boundary is disjoint from the closed unit disk centered at the origin.

Because the origin is in the bounded component, and because the closed unit disk is connected and cannot cross the polygon boundary, the entire closed unit disk is contained in that same bounded component.

## 5. Exhaustion of all boundary-inscribed squares

The only nontrivial part is proving that **every** square with all four vertices on the polygon boundary has been considered.

### 5.1 Parametrizing a square

Let

\[
c=(c_x,c_y),\qquad u=(u_x,u_y),
\]

and let `J` denote counterclockwise rotation by 90 degrees:

\[
J(u_x,u_y)=(-u_y,u_x).
\]

Every oriented square, including degenerate squares when `u=0`, can be written in cyclic order as

\[
p_0=c+u,\qquad
p_1=c+Ju,\qquad
p_2=c-u,\qquad
p_3=c-Ju.
\]

Its squared side length is

\[
L^2=\lVert Ju-u\rVert^2=2(u_x^2+u_y^2).
\]

Thus a nondegenerate square is exactly the case `u != 0`.

### 5.2 Assigning corners to polygon edges

The polygon has ten closed edges `E_0,...,E_9`. For each ordered tuple

\[
(e_0,e_1,e_2,e_3)\in\{0,\ldots,9\}^4,
\]

require `p_k` to lie on edge `E_{e_k}`.

There are exactly

\[
10^4=10000
\]

such assignments.

Every boundary-inscribed square is represented by at least one of these assignments: each of its four corners lies on at least one polygon edge. If a corner is exactly a polygon vertex, it belongs to both adjacent closed edges, and all assignments are still enumerated.

### 5.3 Four exact linear equations

Let edge `E_e` go from `a` to `b`, with direction

\[
d=b-a=(d_x,d_y).
\]

An integer normal is

\[
n=(-d_y,d_x).
\]

The supporting line is

\[
n\cdot x=n\cdot a.
\]

For a fixed ordered edge assignment, substituting

\[
p_0=c+u,
\quad p_1=c+Ju,
\quad p_2=c-u,
\quad p_3=c-Ju
\]

into the four supporting-line equations gives a `4 x 4` linear system in

\[
(c_x,c_y,u_x,u_y).
\]

All matrix entries and right-hand sides are integers when coordinates are kept in the common `D=1200` grid units.

If the determinant is nonzero, the assignment has exactly one candidate solution. The verifier computes it by Cramer's rule using integer determinants only.

It then performs an exact closed-segment test for each of the four corners. A candidate is accepted only when each corner lies on its assigned segment, rather than merely on its supporting line.

### 5.4 Singular systems

Among all 10,000 assignments, exactly ten systems are singular:

\[
(i,i,i,i),\qquad i=0,\ldots,9.
\]

Such an assignment requires all four square corners to lie on one supporting line. Four vertices of a nondegenerate square cannot be collinear. Hence no singular assignment can hide a nondegenerate boundary-inscribed square.

This observation is also checked computationally: the verifier asserts that the complete list of singular assignments is exactly the ten tuples above.

### 5.5 Exact enumeration result

Among the 9,990 nonsingular assignments:

- `144` solutions have all four candidate corners on their assigned closed segments;
- only `4` have positive side length;
- those four are the four cyclic labelings of a single geometric square;
- one labeling has edge assignment `(2,4,5,6)`.

Therefore this is the unique nondegenerate boundary-inscribed square, up to cyclic relabeling.

Its exact squared side length is

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
L<\sqrt2.
\]

Numerically,

\[
L=1.4103926127818764\ldots
<1.4142135623730951\ldots=\sqrt2.
\]

## 6. Conclusion

The ten-vertex polygon is simple, contains the closed unit disk centered at the origin, and has no boundary-inscribed square with side length at least `sqrt(2)`.

Therefore it is a counterexample to the Sharp Polygonal Big Peg conjecture.

## 7. Exact reproducibility

Run

```bash
python3 verify.py
```

The checker uses only Python integers and `fractions.Fraction` for mathematical predicates. Decimal floating-point values are printed only for convenience after all exact assertions have succeeded.

The data required for a completely separate implementation are in [`counterexample.json`](counterexample.json). An independent implementation need not copy any code from `verify.py`: it only needs the seven-step verification procedure described in the README and Sections 3--5 above.
