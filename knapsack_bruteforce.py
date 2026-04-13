"""
=============================================================================
  Brute Force 0/1 Knapsack Problem — Bit Masking Approach
=============================================================================
  Algorithm  : Enumerate all 2^n subsets via bitmask, pick best valid one
  Complexity : Time  O(2^n × n)  |  Space O(n)
  Dataset    : knapsack_benchmark_dataset.csv
               (Classic benchmark instances — Kreher & Stinson,
                Martello & Toth — the same data used in research papers
                and mirrored on Kaggle: kaggle.com/datasets/warcoder/knapsack-problem)
=============================================================================

PSEUDOCODE
----------
function knapsack_bruteforce(weights, values, capacity, n):
    best_value  ← 0
    best_mask   ← 0

    for mask in range(0, 2^n):          # iterate every subset
        total_weight ← 0
        total_value  ← 0

        for i in range(0, n):           # check each item bit
            if bit i is set in mask:
                total_weight ← total_weight + weights[i]
                total_value  ← total_value  + values[i]

        if total_weight <= capacity and total_value > best_value:
            best_value ← total_value
            best_mask  ← mask

    selected_items ← [i for i where bit i is set in best_mask]
    return best_value, selected_items, best_mask
"""

import csv
import os
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────────────
# 1. DATASET LOADER
# ─────────────────────────────────────────────────────────────────────────────

DATASET_FILE = "knapsack_benchmark_dataset.csv"

def load_dataset(filepath=DATASET_FILE):
    """
    Load knapsack_benchmark_dataset.csv and group rows by problem_set.

    CSV columns: item_id, weight, value, problem_set, capacity,
                 optimal_value, source

    Returns
    -------
    dict  { 'P01': { 'weights': [...], 'values': [...],
                     'capacity': int, 'optimal': int,
                     'source': str }, ... }
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset not found: '{filepath}'\n"
            "Make sure knapsack_benchmark_dataset.csv is in the same folder."
        )

    problems = {}
    with open(filepath, newline="") as f:
        for row in csv.DictReader(f):
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


# ─────────────────────────────────────────────────────────────────────────────
# 2. CORE ALGORITHM FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def generate_subsets(n):
    """
    Generator: yield every bitmask from 0 to 2^n - 1.
    Each integer encodes a subset — bit i set means item i is included.
    Memory-efficient: one mask at a time, nothing stored.
    """
    for mask in range(1 << n):      # 1 << n  ==  2^n
        yield mask


def evaluate_subset(mask, weights, values, n):
    """
    Given a bitmask, compute total weight and total value of that subset.
    Returns (total_weight, total_value).
    """
    total_weight = 0
    total_value  = 0
    for i in range(n):
        if mask & (1 << i):         # is bit i set?
            total_weight += weights[i]
            total_value  += values[i]
    return total_weight, total_value


def knapsack_bruteforce(weights, values, capacity):
    """
    Solve 0/1 Knapsack by evaluating ALL 2^n subsets via bitmask.

    Parameters
    ----------
    weights  : list of item weights
    values   : list of item values
    capacity : knapsack weight limit

    Returns
    -------
    best_value : maximum achievable value (int)
    best_items : list of 0-based item indices in optimal subset
    best_mask  : integer bitmask of the optimal subset
    """
    n          = len(weights)
    best_value = 0
    best_mask  = 0

    for mask in generate_subsets(n):
        total_weight, total_value = evaluate_subset(mask, weights, values, n)

        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_mask  = mask

    best_items = [i for i in range(n) if best_mask & (1 << i)]
    return best_value, best_items, best_mask


# ─────────────────────────────────────────────────────────────────────────────
# 3. GREEDY COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

def knapsack_greedy(weights, values, capacity):
    """
    Greedy 0/1 Knapsack: sort by value/weight ratio (desc), pick greedily.
    NOTE: NOT guaranteed optimal for 0/1 — items cannot be split.
    """
    n     = len(weights)
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)

    tw, tv, selected = 0, 0, []
    for i in order:
        if tw + weights[i] <= capacity:
            selected.append(i)
            tw += weights[i]
            tv += values[i]

    return tv, sorted(selected)


# ─────────────────────────────────────────────────────────────────────────────
# 4. DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def print_separator(char="─", width=62):
    print(char * width)


def print_result(label, value, items, weights, values, mask=None, n=None):
    """Pretty-print one knapsack solution."""
    total_w = sum(weights[i] for i in items)
    print(f"  {label}")
    print(f"    Selected items  : {[i+1 for i in items]}  (1-indexed)")
    print(f"    Total weight    : {total_w}")
    print(f"    Total value     : {value}")
    if mask is not None:
        width = n if n else len(weights)
        print(f"    Bitmask         : {mask:0{width}b}  (bit 0 = item 1)")


# ─────────────────────────────────────────────────────────────────────────────
# 5. GREEDY FAILURE DEMO  (uses P04 from the benchmark dataset)
# ─────────────────────────────────────────────────────────────────────────────

def demo_greedy_failure(problems):
    """
    Show a case from the benchmark where greedy gives a suboptimal answer.
    Uses P04 (n=7, capacity=50) from the real dataset.
    Also includes the classic textbook counter-example for reference.
    """
    print_separator("═")
    print("  GREEDY FAILURE DEMO")
    print_separator("═")

    # ── [A] Classic textbook counter-example ─────────────────────────────────
    print("\n  [A] Textbook Counter-Example (n=3, capacity=5)")
    w_ex, v_ex, cap_ex = [1, 2, 3], [6, 10, 12], 5
    print(f"  Items (weight, value) : {list(zip(w_ex, v_ex))}")
    print(f"  Capacity              : {cap_ex}")
    print(f"  Ratios                : {[round(v/w,2) for v,w in zip(v_ex,w_ex)]}")
    print()
    g_val, g_items = knapsack_greedy(w_ex, v_ex, cap_ex)
    b_val, b_items, b_mask = knapsack_bruteforce(w_ex, v_ex, cap_ex)
    print_result("Greedy  result", g_val, g_items, w_ex, v_ex)
    print()
    print_result("Optimal result", b_val, b_items, w_ex, v_ex, b_mask, n=3)
    if g_val < b_val:
        print(f"\n  ⚠  Greedy value {g_val}  <  Optimal {b_val}  — SUBOPTIMAL!")
        print("     Greedy locked on ratio-6.0 item 1, blocking better pair {2,3}.")

    # ── [B] Benchmark P04 ────────────────────────────────────────────────────
    print()
    print_separator()
    p = problems["P04"]
    weights, values, capacity = p["weights"], p["values"], p["capacity"]
    n = len(weights)
    print(f"\n  [B] Benchmark P04 — {p['source']}  (n={n}, capacity={capacity})")
    print(f"  Weights  : {weights}")
    print(f"  Values   : {values}")
    print(f"  Ratios   : {[round(v/w,2) for v,w in zip(values,weights)]}")
    print()
    g_val2, g_items2 = knapsack_greedy(weights, values, capacity)
    b_val2, b_items2, b_mask2 = knapsack_bruteforce(weights, values, capacity)
    print_result("Greedy  result", g_val2, g_items2, weights, values)
    print()
    print_result("Optimal result", b_val2, b_items2, weights, values, b_mask2, n=n)
    print()
    if g_val2 < b_val2:
        print(f"  ⚠  Greedy value {g_val2}  <  Optimal {b_val2}  — SUBOPTIMAL on real data!")
    else:
        print(f"  ✓  Greedy matched optimal on P04 (value {g_val2}).")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# 6. EXPERIMENTAL EVALUATION  (benchmark dataset, n = 5, 7, 10, 15)
# ─────────────────────────────────────────────────────────────────────────────

# Map each target n to the benchmark problem set with that many items
_N_TO_PS = {5: "P02", 7: "P04", 10: "P01", 15: "P07"}

def run_experiments(problems, n_values=None):
    """
    Run brute-force on real benchmark instances and measure runtime.

        n=5  → P02  (capacity 26,  known optimal 56)
        n=7  → P04  (capacity 50,  known optimal 107)
        n=10 → P01  (capacity 165, known optimal 309)
        n=15 → P07  (capacity 750, known optimal 1458)

    Returns list of (n, runtime_seconds) tuples.
    """
    if n_values is None:
        n_values = [5, 7, 10, 15]

    results = []

    print_separator("═")
    print("  EXPERIMENTAL EVALUATION  (benchmark dataset)")
    print_separator("═")

    for n in n_values:
        ps = _N_TO_PS.get(n)
        if ps is None or ps not in problems:
            print(f"\n  ── n={n}: no matching benchmark instance, skipping.")
            continue

        data     = problems[ps]
        weights  = data["weights"]
        values   = data["values"]
        capacity = data["capacity"]
        known    = data["optimal"]

        print(f"\n  ── {ps}  (n={n}, capacity={capacity})  [{data['source']}]")
        print(f"  Weights  : {weights}")
        print(f"  Values   : {values}")

        start = time.perf_counter()
        best_val, best_items, best_mask = knapsack_bruteforce(weights, values, capacity)
        elapsed = time.perf_counter() - start

        total_w = sum(weights[i] for i in best_items)
        match   = "✓ matches known optimal" if best_val == known else f"✗ differs (known={known})"

        print(f"\n  Selected items (1-indexed) : {[i+1 for i in best_items]}")
        print(f"  Bitmask                    : {best_mask:0{n}b}")
        print(f"  Total weight               : {total_w}  (capacity {capacity})")
        print(f"  Total value                : {best_val}   {match}")
        print(f"  Subsets checked            : {2**n:,}  (2^{n})")
        print(f"  Runtime                    : {elapsed:.6f} s")

        results.append((n, elapsed))

    return results


# ─────────────────────────────────────────────────────────────────────────────
# 7. PLOT RUNTIME
# ─────────────────────────────────────────────────────────────────────────────

def plot_runtime(results, filename="knapsack_runtime.png"):
    """
    Plot measured runtime vs n (linear + log scale). Saves PNG to disk.
    """
    ns    = [r[0] for r in results]
    times = [r[1] for r in results]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#0f0f1a")

    for ax in axes:
        ax.set_facecolor("#1a1a2e")
        ax.tick_params(colors="#ccccdd", labelsize=9)
        ax.spines[:].set_color("#444466")
        ax.xaxis.label.set_color("#ccccdd")
        ax.yaxis.label.set_color("#ccccdd")
        ax.title.set_color("#eeeeff")

    # linear scale
    axes[0].plot(ns, times, "o-", color="#7b7bff", linewidth=2.5,
                 markersize=8, markerfacecolor="#ff7b7b",
                 markeredgecolor="white", markeredgewidth=0.8)
    axes[0].fill_between(ns, times, alpha=0.18, color="#7b7bff")
    axes[0].set_title("Runtime vs n  (linear scale)", fontsize=12, pad=10)
    axes[0].set_xlabel("Number of items  (n)")
    axes[0].set_ylabel("Runtime (seconds)")
    axes[0].set_xticks(ns)
    for x, y in zip(ns, times):
        axes[0].annotate(f"{y:.5f}s", (x, y),
                         textcoords="offset points", xytext=(0, 10),
                         ha="center", color="#ffdd88", fontsize=8)

    # log scale
    axes[1].plot(ns, times, "o-", color="#7bffb0", linewidth=2.5,
                 markersize=8, markerfacecolor="#ffb07b",
                 markeredgecolor="white", markeredgewidth=0.8)
    axes[1].set_yscale("log")
    axes[1].set_title("Runtime vs n  (log scale — exponential = straight line)",
                      fontsize=11, pad=10)
    axes[1].set_xlabel("Number of items  (n)")
    axes[1].set_ylabel("Runtime (seconds, log)")
    axes[1].set_xticks(ns)
    axes[1].grid(True, which="both", linestyle="--", alpha=0.25, color="#666699")

    fig.suptitle(
        "0/1 Knapsack · Brute-Force Bitmask · O(2ⁿ × n) Runtime\n"
        "(benchmark: P02 n=5 · P04 n=7 · P01 n=10 · P07 n=15)",
        fontsize=12, color="#ffffff", y=1.02
    )
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"\n  Runtime plot saved → {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

def print_complexity():
    print_separator("═")
    print("  COMPLEXITY ANALYSIS")
    print_separator("═")
    print("""
  Time Complexity  :  O(2ⁿ × n)
  ─────────────────────────────
  • There are 2ⁿ possible subsets (each item is either IN or OUT).
  • For every subset (bitmask), we scan all n bits to compute weight & value.
  • Total operations ≈ 2ⁿ × n  →  exponential in n.
  • Example:  n=15  →  15 × 32,768  ≈  491,520 operations.

  Space Complexity :  O(n)   (O(1) extra beyond the input)
  ──────────────────────────────────────────────────────
  • Subsets generated one at a time — no list of all masks stored.
  • Only a handful of scalar variables (best_value, best_mask, etc.).
  • Input arrays weights[] and values[] are O(n) — unavoidable.
""")


# ─────────────────────────────────────────────────────────────────────────────
# 9. ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print()
    print_separator("═")
    print("  0/1 KNAPSACK  ·  BRUTE FORCE BITMASK  ·  BENCHMARK DATASET")
    print_separator("═")

    # Step 1 — load the real dataset
    problems = load_dataset(DATASET_FILE)
    print(f"\n  Loaded {len(problems)} benchmark problem sets from '{DATASET_FILE}'")
    for ps, d in problems.items():
        print(f"    {ps}  →  n={len(d['weights'])}, capacity={d['capacity']}, "
              f"known_optimal={d['optimal']}")

    # Step 2 — complexity summary
    print()
    print_complexity()

    # Step 3 — greedy failure demo using real benchmark data
    demo_greedy_failure(problems)

    # Step 4 — timed experiments on benchmark instances
    results = run_experiments(problems, n_values=[5, 7, 10, 15])

    # Step 5 — exponential growth summary table
    print()
    print_separator("═")
    print("  EXPONENTIAL GROWTH TABLE  (benchmark instances)")
    print_separator("═")
    print(f"  {'n':>4}  {'problem':>8}  {'2^n subsets':>14}  {'runtime':>12}")
    print_separator()
    for (n, t) in results:
        ps = _N_TO_PS.get(n, "?")
        print(f"  {n:>4}  {ps:>8}  {2**n:>14,}  {t:>11.6f}s")

    # Step 6 — runtime plot
    plot_runtime(results, filename="knapsack_runtime.png")

    print()
    print_separator("═")
    print("  Done.  All outputs written.")
    print_separator("═")
    print()


if __name__ == "__main__":
    main()
