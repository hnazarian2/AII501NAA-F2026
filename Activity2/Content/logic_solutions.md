# Activity 2 — Questions 2, 3, and 4

Notation: T = True, F = False; ¬ = NOT; ∧ = AND; ∨ = OR; ⇒ = implication; ⇔ = biconditional.

## Question 2 — Propositional Logic: Satisfiability 

### 2(a) Smoke ⇒ Fire

| Smoke | Fire | Smoke ⇒ Fire |
|:--:|:--:|:--:|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

**Answer: Neither valid nor unsatisfiable.** The sentence is true for three assignments and false for one. It is satisfiable but not valid.

### 2(b) ((Smoke ∧ Heat) ⇒ Fire) ⇔ ((Smoke ⇒ Fire) ∨ (Heat ⇒ Fire))

Let S = Smoke, H = Heat, F = Fire. Define L = (S ∧ H) ⇒ F and R = (S ⇒ F) ∨ (H ⇒ F).

| S | H | F | S ∧ H | S ⇒ F | H ⇒ F | L | R | L ⇔ R |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| T | T | T | T | T | T | T | T | T |
| T | T | F | T | F | F | F | F | T |
| T | F | T | F | T | T | T | T | T |
| T | F | F | F | F | T | T | T | T |
| F | T | T | F | T | T | T | T | T |
| F | T | F | F | T | F | T | T | T |
| F | F | T | F | T | T | T | T | T |
| F | F | F | F | T | T | T | T | T |

**Answer: Valid.** Both sides have equal truth values on every row, so the biconditional is true in all eight models.

## Question 3 — Models 

The vocabulary has A, B, C, D, so there are 2⁴ = 16 possible truth assignments.

### 3(a) B ∨ C

| B | C | B ∨ C |
|:--:|:--:|:--:|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

There are three satisfying assignments to B and C. The unused propositions A and D each have two possible values. Therefore the count is **3 × 2² = 12 models**.

### 3(b) (A ⇒ B) ∧ A ∧ ¬B ∧ C ∧ D

To satisfy the conjunction, A = T, ¬B = T (so B = F), C = T and D = T. But then A ⇒ B is T ⇒ F = F. This contradicts the requirement that all conjuncts be true. Thus **0 models** satisfy it; the sentence is unsatisfiable.

## Question 4 — Propositional Logic: Resolution 

Given: **[(Food ⇒ Party) ∨ (Drinks ⇒ Party)] ⇒ [(Food ∧ Drinks) ⇒ Party]**.

Let F = Food, D = Drinks, and P = Party. Define L = (F ⇒ P) ∨ (D ⇒ P), and R = (F ∧ D) ⇒ P. The overall sentence is L ⇒ R.

### 4(a) Enumeration

| F | D | P | F ⇒ P | D ⇒ P | F ∧ D | L | R | L ⇒ R |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| T | T | T | T | T | T | T | T | T |
| T | T | F | F | F | T | F | F | T |
| T | F | T | T | T | F | T | T | T |
| T | F | F | F | T | F | T | T | T |
| F | T | T | T | T | F | T | T | T |
| F | T | F | T | F | F | T | T | T |
| F | F | T | T | T | F | T | T | T |
| F | F | F | T | T | F | T | T | T |

**Answer: Valid.** Every row of the final column is true. In the second row, L and R are both false, and F ⇒ F is true.

### 4(b) Convert the left and right sides into CNF

**Left-hand side:**

1. L = (F ⇒ P) ∨ (D ⇒ P).
2. Replace implications: (¬F ∨ P) ∨ (¬D ∨ P).
3. Associativity: ¬F ∨ P ∨ ¬D ∨ P.
4. Idempotence (P ∨ P = P), and commutativity: **¬F ∨ ¬D ∨ P**.

**Right-hand side:**

1. R = (F ∧ D) ⇒ P.
2. Replace implication: ¬(F ∧ D) ∨ P.
3. De Morgan's law: (¬F ∨ ¬D) ∨ P.
4. Associativity: **¬F ∨ ¬D ∨ P**.

A disjunction of literals is a single CNF clause. Both sides have the identical CNF expression, so L ⇒ R is of the form X ⇒ X, confirming validity in (a).

### 4(c) Resolution refutation

To prove L ⇒ R valid, negate it and show that its negation is unsatisfiable.

1. ¬(L ⇒ R)
2. ¬(¬L ∨ R) — eliminate implication
3. L ∧ ¬R — De Morgan's law and double negation
4. (¬F ∨ ¬D ∨ P) ∧ ¬(¬F ∨ ¬D ∨ P) — substitute from (b)
5. (¬F ∨ ¬D ∨ P) ∧ F ∧ D ∧ ¬P — De Morgan's law

The four initial clauses are:

- C₁ = ¬F ∨ ¬D ∨ P
- C₂ = F
- C₃ = D
- C₄ = ¬P

Resolve C₁ with C₂ on F to obtain **C₅ = ¬D ∨ P**.

Resolve C₅ with C₃ on D to obtain **C₆ = P**.

Resolve C₆ with C₄ on P to obtain **□ (the empty clause)**.

The empty clause means that the negation of the original statement is unsatisfiable. Therefore, the original implication **is valid**.
