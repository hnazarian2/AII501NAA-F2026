"""Connect Four move generator using depth-limited Monte Carlo Tree Search."""
from __future__ import annotations
import argparse
import csv
import math
import random
from dataclasses import dataclass, field
from pathlib import Path

ROWS, COLS = 6, 7
EMPTY = 0
Board = tuple[tuple[int, ...], ...]


def empty_board() -> Board:
    return tuple(tuple(EMPTY for _ in range(COLS)) for _ in range(ROWS))


def legal_moves(board: Board) -> list[int]:
    return [c for c in range(COLS) if board[0][c] == EMPTY]


def drop(board: Board, column: int, player: int) -> Board:
    if player not in (1, 2) or column not in range(COLS) or board[0][column] != EMPTY:
        raise ValueError("Invalid player or full/out-of-range column")
    new = [list(row) for row in board]
    for row in range(ROWS - 1, -1, -1):
        if new[row][column] == EMPTY:
            new[row][column] = player
            return tuple(tuple(r) for r in new)
    raise ValueError("Column full")


def winner(board: Board) -> int:
    for r in range(ROWS):
        for c in range(COLS):
            p = board[r][c]
            if p == EMPTY:
                continue
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                er, ec = r + 3 * dr, c + 3 * dc
                if 0 <= er < ROWS and 0 <= ec < COLS:
                    if all(board[r + k * dr][c + k * dc] == p for k in range(1, 4)):
                        return p
    return 0


def terminal(board: Board) -> bool:
    return winner(board) != 0 or not legal_moves(board)


def opponent(player: int) -> int:
    return 3 - player


def objective(board: Board, player: int) -> float:
    """Rule-based utility in [0, 1], for perspective of `player`.

    Evaluates existing 4-cell windows (not a full positional game solver).
    Terminal wins/losses override heuristic scores.
    """
    w = winner(board)
    if w:
        return 1.0 if w == player else 0.0
    if not legal_moves(board):
        return 0.5
    score = 0.0
    weights = (0.0, 0.02, 0.10, 0.45, 1.0)
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if not (0 <= r + 3 * dr < ROWS and 0 <= c + 3 * dc < COLS):
                    continue
                cells = [board[r + k * dr][c + k * dc] for k in range(4)]
                mine, theirs = cells.count(player), cells.count(opponent(player))
                if theirs == 0:
                    score += weights[mine]
                elif mine == 0:
                    score -= weights[theirs]
    score += 0.025 * sum(board[r][COLS // 2] == player for r in range(ROWS))
    score -= 0.025 * sum(board[r][COLS // 2] == opponent(player) for r in range(ROWS))
    # Smoothly normalize to [0, 1]. This evaluates patterns, not certain victories.
    return 0.5 + 0.5 * math.tanh(score / 3.0)


@dataclass
class Node:
    board: Board
    to_move: int
    parent: Node | None = None
    move: int | None = None
    depth: int = 0
    children: list[Node] = field(default_factory=list)
    visits: int = 0
    value_sum: float = 0.0  # from root player's perspective


def select_child(node: Node, root_player: int, exploration: float,
                 objective_weight: float, rng: random.Random) -> Node:
    """UCT + board evaluation; alternating-player selection.

    At opponents' levels, exploitation is from opponent perspective.
    """
    candidates = []
    for child in node.children:
        if child.visits == 0:
            utility = float('inf')
        else:
            learned = child.value_sum / child.visits
            if node.to_move != root_player:
                learned = 1.0 - learned
            heuristic = objective(child.board, node.to_move)
            utility = ((1 - objective_weight) * learned + objective_weight * heuristic
                       + exploration * math.sqrt(math.log(node.visits + 1) / child.visits))
        candidates.append((utility, child))
    best = max(value for value, _ in candidates)
    return rng.choice([child for value, child in candidates if value == best])


def playout(board: Board, player: int, root_player: int, rng: random.Random) -> float:
    """Randomly play until game ends; 1 win, 0 loss, 0.5 draw."""
    while not terminal(board):
        board = drop(board, rng.choice(legal_moves(board)), player)
        player = opponent(player)
    w = winner(board)
    return 0.5 if w == 0 else float(w == root_player)


def mcts(board: Board, player: int, *, cycles: int = 1000, expansion_nodes: int = 2,
         max_depth: int = 5, objective_weight: float = 0.25,
         exploration: float = 1.414, seed: int | None = None) -> tuple[int, list[dict]]:
    """Recommend a column, and return root child stats.

    Expands up to `expansion_nodes` new siblings per visited expandable
    node, then simulates from one new child (or selected existing child).
    This makes expansion width configurable without causing multiple
    playouts per cycle. The tree is limited to `max_depth` edges;
    rollout continues randomly to game end.
    """
    if not 0 <= objective_weight <= 1 or cycles < 1 or expansion_nodes < 1 or max_depth < 1 or exploration < 0:
        raise ValueError("Invalid MCTS parameters")
    if player not in (1, 2) or terminal(board):
        raise ValueError("Board must be nonterminal and player must be 1 or 2")
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(cycles):
        node = root
        while node.depth < max_depth and not terminal(node.board):
            existing = {child.move for child in node.children}
            unexpanded = [m for m in legal_moves(node.board) if m not in existing]
            if unexpanded:
                rng.shuffle(unexpanded)
                for move in unexpanded[:expansion_nodes]:
                    node.children.append(Node(drop(node.board, move, node.to_move),
                                              opponent(node.to_move), node, move, node.depth + 1))
                fresh = [child for child in node.children if child.visits == 0]
                node = rng.choice(fresh)
                break
            node = select_child(node, player, exploration, objective_weight, rng)
        result = playout(node.board, node.to_move, player, rng)
        while node is not None:
            node.visits += 1
            node.value_sum += result
            node = node.parent
    # Robust-child criterion: highest visit count; tied by value, then column centre.
    ranked = sorted(root.children, key=lambda n: (n.visits, n.value_sum / max(1, n.visits),
                                                  -abs(n.move - COLS // 2)), reverse=True)
    details = sorted((dict(column=n.move, visits=n.visits,
                           mean_reward=round(n.value_sum / max(1, n.visits), 4))
                      for n in root.children), key=lambda entry: entry['column'])
    return ranked[0].move, details


def display(board: Board) -> str:
    symbols = {0: '.', 1: 'X', 2: 'O'}
    return '\n'.join(' '.join(symbols[v] for v in row) for row in board) + '\n0 1 2 3 4 5 6'


def experiment(path: Path, board: Board, player: int) -> None:
    """Write raw observations; do not claim meaningful superiority from few runs."""
    configs = [
        (60, 1, 3, 0.0), (60, 2, 3, 0.25), (60, 4, 5, 0.5),
        (200, 1, 3, 0.0), (200, 2, 5, 0.25), (200, 4, 7, 0.5),
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['cycles', 'expansion_nodes', 'max_depth',
                                               'objective_weight', 'seed', 'move', 'visits', 'mean_reward'])
        writer.writeheader()
        for cycles, width, depth, weight in configs:
            for seed in range(3):
                move, stats = mcts(board, player, cycles=cycles, expansion_nodes=width,
                                   max_depth=depth, objective_weight=weight, seed=seed)
                selected = next(x for x in stats if x['column'] == move)
                writer.writerow(dict(cycles=cycles, expansion_nodes=width, max_depth=depth,
                                     objective_weight=weight, seed=seed, move=move,
                                     visits=selected['visits'], mean_reward=selected['mean_reward']))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles', type=int, default=1000)
    parser.add_argument('--expansion-nodes', type=int, default=2)
    parser.add_argument('--max-depth', type=int, default=5)
    parser.add_argument('--objective-weight', type=float, default=0.25)
    parser.add_argument('--exploration', type=float, default=1.414)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--experiment', action='store_true')
    parser.add_argument('--output', type=Path, default=Path('experiment_results.csv'))
    args = parser.parse_args()
    # Example midgame position: both players have taken 3 moves; player 1 next.
    board = empty_board()
    for col, p in [(3, 1), (2, 2), (3, 1), (2, 2), (4, 1), (4, 2)]:
        board = drop(board, col, p)
    print('Board:\n' + display(board))
    if args.experiment:
        experiment(args.output, board, 1)
        print(f'Wrote {args.output}')
    else:
        move, stats = mcts(board, 1, cycles=args.cycles, expansion_nodes=args.expansion_nodes,
                           max_depth=args.max_depth, objective_weight=args.objective_weight,
                           exploration=args.exploration, seed=args.seed)
        print('Recommended column:', move)
        print('Child statistics:', stats)

if __name__ == '__main__':
    main()
