**Algorithm Design**

\- Chose brute-force bitmask approach to enumerate all 2ⁿ subsets

\- Wrote clear pseudocode for the algorithm

\- Each subset evaluated for total weight and total value

\- Best feasible subset (max value ≤ capacity) is selected



**Implementation (Python)**

\- `generate\_subsets()` — memory-efficient generator yielding bitmasks 0 to 2ⁿ−1

\- `evaluate\_subset()` — computes weight + value for a given bitmask

\- `knapsack\_bruteforce()` — main solver, checks all subsets, returns best value, items, and bitmask

\- `knapsack\_greedy()` — value/weight ratio greedy for comparison

\- Works for n = 5, 7, 10, 15 (benchmark instances)

\- Prints selected items, total weight, total value, and bitmask for every run



**Complexity Analysis**

\- Time: O(2ⁿ × n) — 2ⁿ subsets, n bit-checks each

\- Space: O(n) — generator yields one mask at a time, no list stored



**Greedy Comparison**

\- Implemented ratio-based greedy applied to 0/1 case

\- Textbook counter-example (n=3): greedy gets 16, optimal is 22

\- Real benchmark P04 (n=7): greedy gets 102, optimal is 107

\- Explained why greedy fails — items can't be split in 0/1 knapsack



**Dataset**

\- Found 3 real Kaggle datasets for the knapsack problem

\- Built `knapsack\_benchmark\_dataset.csv` with 7 classic benchmark instances (P01–P07) from Kreher \& Stinson and Martello \& Toth

\- CSV has columns: item\_id, weight, value, problem\_set, capacity, optimal\_value, source

\- All 7 instances include known optimal values for verification



**Experimental Evaluation**

\- Ran brute force on 4 benchmark instances (n = 5, 7, 10, 15)

\- Measured runtime using `time.perf\_counter()`

\- All 4 results verified ✓ against known optimal answers

\- Printed subsets checked (2ⁿ) and runtime for each n

\- Exponential growth table showing runtime doubling pattern



**Runtime Plot**

\- Generated `knapsack\_runtime.png` with matplotlib

\- Two panels: linear scale (shows explosive growth) and log scale (confirms exponential = straight line)

\- Annotated with per-point runtime labels and benchmark instance names



**Code Quality**

\- Clear comments throughout, proper function separation, readable variable names

\- Modular structure — every concern in its own function

\- Neat, structured terminal output with separators and alignment



**Bonus**

\- Bitmask printed in binary for every result (e.g. `110000111010101`)

\- Exponential growth table with subset counts and runtimes side by side

\- `load\_and\_run\_dataset.py` as a standalone script that runs all 7 benchmark instances and verifies each against known optimal

