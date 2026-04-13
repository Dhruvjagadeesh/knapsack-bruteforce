# 0/1 Knapsack Problem — Brute Force Bitmask

A clean, well-structured Python implementation of the **0/1 Knapsack Problem** using a **brute-force bitmask** approach. Built for educational purposes as part of an algorithms course project.

---

## What This Project Does

Given a set of items (each with a weight and value) and a knapsack with a fixed weight capacity, the goal is to find the subset of items that **maximises total value without exceeding the capacity**.

This project solves it by:
- Enumerating **all 2ⁿ possible subsets** using integer bitmasks
- Evaluating each subset for total weight and value
- Selecting the best feasible one (guaranteed globally optimal)

---

## Files

| File | Description |
|------|-------------|
| `knapsack_benchmark_dataset.csv` | Dataset with 7 classic benchmark instances (55 rows), each with item weights, values, capacity, and known optimal values |
| `knapsack_bruteforce.py` | Main file — full solver, greedy comparison, complexity analysis, experiments, and runtime plot |
| `load_and_run_dataset.py` | Standalone script that runs brute force across all 7 benchmark instances and verifies against known optimal answers |
| `knapsack_runtime.png` | Generated runtime graph (linear + log scale) showing exponential growth |

---

## Run Order

Make sure all files are in the **same folder**, then:

```bash
# Step 1 — install dependency (only matplotlib needed)
pip install matplotlib

# Step 2 — run the main file (reads CSV, runs experiments, saves plot)
python knapsack_bruteforce.py

# Step 3 — optional: run brute force on all 7 benchmark instances
python load_and_run_dataset.py
```

`knapsack_bruteforce.py` is the main deliverable. `load_and_run_dataset.py` is a bonus sweep.

---

## Algorithm

```
for mask in range(0, 2^n):
    compute total_weight and total_value for this subset
    if total_weight <= capacity and total_value > best:
        update best
```

Each integer `mask` from `0` to `2ⁿ − 1` encodes a subset — **bit i set = item i is included**.

### Complexity

| | |
|---|---|
| Time | O(2ⁿ × n) — 2ⁿ subsets, n bit-checks each |
| Space | O(n) — one mask generated at a time, nothing stored |

---

## Benchmark Dataset

The dataset (`knapsack_benchmark_dataset.csv`) contains 7 classic problem instances used in algorithms research and textbooks:

| Problem | Items (n) | Capacity | Known Optimal |
|---------|-----------|----------|---------------|
| P01 | 10 | 165 | 309 |
| P02 | 5 | 26 | 56 |
| P03 | 6 | 190 | 150 |
| P04 | 7 | 50 | 107 |
| P05 | 8 | 104 | 900 |
| P06 | 7 | 170 | 1735 |
| P07 | 15 | 750 | 1458 |

**Source:** Classic benchmark instances from:
- Kreher & Stinson, *Combinatorial Algorithms*, CRC Press, 1998
- Martello & Toth, *Knapsack Problems: Algorithms and Computer Implementations*, Wiley, 1990
- Also mirrored on Kaggle: [kaggle.com/datasets/warcoder/knapsack-problem](https://www.kaggle.com/datasets/warcoder/knapsack-problem)

---

## Sample Output

```
── P01  (n=10, capacity=165)  [Kreher-Stinson]
  Weights  : [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
  Values   : [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

  Selected items (1-indexed) : [1, 2, 3, 4, 6]
  Bitmask                    : 0000101111
  Total weight               : 165  (capacity 165)
  Total value                : 309   ✓ matches known optimal
  Subsets checked            : 1,024  (2^10)
  Runtime                    : 0.000746 s
```

---

## Greedy vs Optimal

The project also implements a **greedy approach** (value/weight ratio) and shows where it fails on 0/1 knapsack:

| | Greedy | Brute Force (Optimal) |
|---|---|---|
| Textbook example (n=3) | Value **16** | Value **22** |
| Benchmark P04 (n=7) | Value **102** | Value **107** |

Greedy fails because items **cannot be split** in 0/1 knapsack — a high-ratio small item can block a more valuable whole-item combination.

---

## Exponential Growth

| n | Problem | Subsets (2ⁿ) | Runtime |
|---|---------|--------------|---------|
| 5 | P02 | 32 | ~0.000016 s |
| 7 | P04 | 128 | ~0.000065 s |
| 10 | P01 | 1,024 | ~0.000746 s |
| 15 | P07 | 32,768 | ~0.036 s |

Each +5 items multiplies the number of subsets by 32 (= 2⁵).

---

## Requirements

- Python 3.7+
- matplotlib

```bash
pip install matplotlib
```

No other dependencies.
