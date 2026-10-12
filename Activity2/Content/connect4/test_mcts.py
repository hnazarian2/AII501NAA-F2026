import unittest
from mcts import empty_board, drop, legal_moves, winner, terminal, mcts, objective

class ConnectFourTests(unittest.TestCase):
    def test_gravity_and_immutable_board(self):
        original = empty_board()
        board = drop(drop(original, 3, 1), 3, 2)
        self.assertEqual((board[5][3], board[4][3]), (1, 2))
        self.assertEqual(original[5][3], 0)

    def test_full_column(self):
        board = empty_board()
        for index in range(6):
            board = drop(board, 0, 1 if index % 2 == 0 else 2)
        self.assertNotIn(0, legal_moves(board))
        with self.assertRaises(ValueError):
            drop(board, 0, 1)

    def test_horizontal_vertical_diagonal(self):
        board = empty_board()
        for col in range(4):
            board = drop(board, col, 1)
        self.assertEqual(winner(board), 1)
        vertical = empty_board()
        for _ in range(4):
            vertical = drop(vertical, 2, 2)
        self.assertEqual(winner(vertical), 2)
        diagonal = empty_board()
        for c in range(4):
            for _ in range(c):
                diagonal = drop(diagonal, c, 2)
            diagonal = drop(diagonal, c, 1)
        self.assertEqual(winner(diagonal), 1)
        self.assertTrue(terminal(diagonal))

    def test_mcts_deterministic_seed_and_legal_move(self):
        board = empty_board()
        a, stats_a = mcts(board, 1, cycles=100, seed=42)
        b, stats_b = mcts(board, 1, cycles=100, seed=42)
        self.assertEqual((a, stats_a), (b, stats_b))
        self.assertIn(a, legal_moves(board))
        self.assertEqual(sum(row['visits'] for row in stats_a), 100)

    def test_objective_bounds(self):
        board = empty_board()
        self.assertTrue(0 <= objective(board, 1) <= 1)

if __name__ == '__main__':
    unittest.main()
