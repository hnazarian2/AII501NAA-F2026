# AII501NAA — Activity 2

This folder contains all four questions of Activity 2. The main program is a Python command-line **Connect Four MCTS move generator**, not a graphical game.

## Deliverables

| Path | Purpose |
|---|---|
| `connect4/mcts.py` | Connect Four board mechanics, heuristic selection and MCTS move generator |
| `connect4/test_mcts.py` | Automated game mechanics and MCTS tests |
| `connect4/controlled_experiments.py` | Reproducible one-parameter-at-a-time experiments |
| `controlled_results.csv` | Observed output of 36 experiment runs (four parameters × three values × three seeds) |
| `experiment_results.csv` | Earlier 18-run exploratory data (multiple parameters change together; not used for causal comparison) |
| `report.md` | Part 1 explanation, data summary, analysis and reflection |
| `logic_solutions.md` | Full worked answers to Questions 2, 3 and 4 |

## Requirements and setup

Python 3.10+ is required. No third-party packages are needed. Download/clone this repository and open a terminal in `Activity2/connect4`.

## Execution

Run the move generator on the fixed example position:

```bash
python mcts.py --cycles 1000 --expansion-nodes 2 --max-depth 5 --objective-weight 0.25 --seed 42
```

Options:
- `--cycles`: MCTS iterations, integer >= 1
- `--expansion-nodes`: up to this many new sibling children per expansion, integer >= 1
- `--max-depth`: deepest search tree level, integer >= 1
- `--objective-weight`: fraction of heuristic board utility in exploitation, between 0 and 1
- `--exploration`: UCT exploration coefficient, nonnegative
- `--seed`: RNG seed, optional; setting it reproduces identical outcomes for the same configuration

The program prints the board, the selected zero-indexed column and each explored root move's visits and mean reward.

## Testing

From `Activity2/connect4`:

```bash
python -m unittest -v test_mcts.py
```

Tests cover gravity and board immutability, full columns, three types of four-in-a-row, reproducible seeded MCTS/legal moves, and bounded heuristics. All tests passed in the packaged environment.

## Reproduce experiments

From `Activity2/connect4`:

```bash
python controlled_experiments.py
```

This overwrites `Activity2/controlled_results.csv` with the controlled 36-run experiment. The CSV is summarized and interpreted in `report.md`. The previous exploratory dataset can be regenerated using:

```bash
python mcts.py --experiment --output ../experiment_results.csv
```

## Assumptions and design choices

- Board dimensions: 6 rows × 7 columns. Player 1 = `X`, player 2 = `O`, empty = `.`. Columns are **0 through 6**.
- The starting position is the fixed six-move position specified in `main()`; player 1 is the next player. This assignment is interpreted as requesting a **move generator**, not a GUI or a full player-vs-player application.
- `drop()` creates a new immutable board; the bottommost empty row receives the piece.
- MCTS uses selection, expansion, simulation (random legal moves until terminal), and backpropagation. A configured `max_depth` limits *tree depth*, not random playout length.
- Selection combines visit-based empirical playout reward and a rule-based heuristic (four-cell windows and modest centre control), plus an exploration term. These weights are design choices rather than specified constants in the assignment.
- Expansion adds up to `expansion_nodes` newly available children and simulates one of them per cycle. Thus the number of rollouts per run remains `cycles`.
- Simulation result: root player win = 1, loss = 0, draw = 0.5. A final root child with the most visits is recommended; ties are broken by mean reward and centre proximity.
- Results depend on random decisions. `seed` makes repeated runs reproducible. The experimental conclusions are limited to the tested starting board and three seeds per setting; no claim of best move or playing superiority is made.
- The implementation requires no special hardware or network connection.


