"""
=============================================================================
  Dataset Loader — knapsack_benchmark_dataset.csv
  Works with knapsack_bruteforce.py
=============================================================================
  Source   : Classic benchmark instances (Kreher & Stinson, Martello & Toth)
  CSV cols : item_id, weight, value, problem_set, capacity, optimal_value
=============================================================================
"""

import csv
import time

# ── paste or import from knapsack_bruteforce.py ──────────────────────────────
def generate_subsets(n):
    for mask in range(1 << n):
        yield mask

def knapsack_bruteforce(weights, values, capacity):
    n = len(weights)
    best_value, best_mask = 0, 0
    for mask in generate_subsets(n):
        tw = tv = 0
        for i in range(n):
            if mask & (1 << i):
                tw += weights[i]; tv += values[i]
        if tw <= capacity and tv > best_value:
            best_value = tv; best_mask = mask
    best_items = [i for i in range(n) if best_mask & (1 << i)]
    return best_value, best_items, best_mask

# ─────────────────────────────────────────────────────────────────────────────

def load_dataset(filepath="knapsack_benchmark_dataset.csv"):
    """
    Load the CSV and group rows by problem_set.
    Returns a dict: { 'P01': {'weights':[], 'values':[], 'capacity':int, 'optimal':int}, ... }
    """
    problems = {}
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ps = row["problem_set"]
            if ps not in problems:
                problems[ps] = {
                    "weights":  [],
                    "values":   [],
                    "capacity": int(row["capacity"]),
                    "optimal":  int(row["optimal_value"]),
                    "source":   row["source"],
                }
            problems[ps]["weights"].append(int(row["weight"]))
            problems[ps]["values"].append(int(row["value"]))
    return problems


def run_on_dataset(filepath="knapsack_benchmark_dataset.csv"):
    problems = load_dataset(filepath)

    print("=" * 64)
    print("  0/1 KNAPSACK — BRUTE FORCE ON BENCHMARK DATASET")
    print("=" * 64)

    for ps, data in problems.items():
        weights  = data["weights"]
        values   = data["values"]
        capacity = data["capacity"]
        known_opt= data["optimal"]
        n        = len(weights)

        # Skip large instances for brute force (n > 20 is impractical)
        if n > 20:
            print(f"\n  {ps} (n={n})  →  skipped (n>20, brute force impractical)")
            continue

        start = time.perf_counter()
        best_val, best_items, best_mask = knapsack_bruteforce(weights, values, capacity)
        elapsed = time.perf_counter() - start

        total_w = sum(weights[i] for i in best_items)
        match   = "✓ matches known optimal" if best_val == known_opt else f"✗ differs (known={known_opt})"

        print(f"\n  {ps}  —  {data['source']}  (n={n}, capacity={capacity})")
        print(f"  Weights  : {weights}")
        print(f"  Values   : {values}")
        print(f"  Selected : {[i+1 for i in best_items]}  (1-indexed)")
        print(f"  Bitmask  : {best_mask:0{n}b}")
        print(f"  Weight   : {total_w}  /  {capacity}")
        print(f"  Value    : {best_val}   {match}")
        print(f"  Subsets  : {2**n:,}   Runtime: {elapsed:.6f} s")

    print("\n" + "=" * 64)


if __name__ == "__main__":
    run_on_dataset("knapsack_benchmark_dataset.csv")
