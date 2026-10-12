"""Controlled MCTS parameter experiments; CSV reproducibly generated from code."""
import csv
from pathlib import Path
from mcts import empty_board, drop, mcts

BASE = dict(cycles=120, expansion_nodes=2, max_depth=5, objective_weight=0.25)
VARIANTS = {
    'cycles': [40, 120, 300],
    'expansion_nodes': [1, 2, 4],
    'max_depth': [2, 5, 7],
    'objective_weight': [0.0, 0.25, 0.75],
}

def example_board():
    board = empty_board()
    for col, player in [(3, 1), (2, 2), (3, 1), (2, 2), (4, 1), (4, 2)]:
        board = drop(board, col, player)
    return board

def run(output: Path):
    board = example_board()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['varying_parameter', 'parameter_value', 'cycles', 'expansion_nodes', 'max_depth', 'objective_weight', 'seed', 'move', 'visits', 'mean_reward'])
        writer.writeheader()
        for parameter, values in VARIANTS.items():
            for value in values:
                settings = {**BASE, parameter: value}
                for seed in (0, 1, 2):
                    move, details = mcts(board, 1, seed=seed, **settings)
                    selected = next(d for d in details if d['column'] == move)
                    writer.writerow({'varying_parameter': parameter, 'parameter_value': value, **settings,
                                     'seed': seed, 'move': move, 'visits': selected['visits'], 'mean_reward': selected['mean_reward']})
    print(f'Wrote {output}')

if __name__ == '__main__':
    run(Path(__file__).resolve().parent.parent / 'controlled_results.csv')
