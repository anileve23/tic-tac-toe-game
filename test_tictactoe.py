import unittest
from tic_tac_toe import TicTacToeGame, Player, Move

class TestTicTacToeGame(unittest.TestCase):
    def setUp(self):
        # Set up two players - X and O with respective colors
        self.players = [Player(label="X", color="blue"), Player(label="O", color="green")]
        # Initialize the game with a 3x3 board using the created players
        self.game = TicTacToeGame(self.players, 3)

    def test_game_creation(self):
        # Test whether the game is correctly created with specific initial conditions
        self.assertEqual(self.game.board_size, 3)  # Check the board size
        self.assertEqual(self.game.current_player.label, "X")  # Check starting player
        self.assertFalse(self.game.has_winner())  # Check if there's no initial winner
        self.assertFalse(self.game.is_tied())  # Check if the game isn't tied initially

    def test_valid_move(self):
        # Test if a move is valid on an empty spot on the board
        move = Move(0, 0, "X")
        self.assertTrue(self.game.is_valid_move(move))

    def test_invalid_move(self):
        # Test if a move is invalid on an already taken spot on the board
        move = Move(0, 0, "X")
        self.game.process_move(move)  # Simulate placing a move
        self.assertFalse(self.game.is_valid_move(move))

    def test_toggle_player(self):
        # Test if the player toggles correctly after a move
        initial_player = self.game.current_player
        self.game.toggle_player()
        self.assertNotEqual(initial_player, self.game.current_player)

    def test_win_conditions_3x3(self):
        # Test for winning conditions on a 3x3 board (horizontal win)
        moves_k_horizontal_win = [
            Move(0, 0, "X"), Move(0, 1, "O"),
            Move(1, 0, "X"), Move(1, 1, "O"),
            Move(2, 0, "X")
        ]
        for move in moves_k_horizontal_win:
            self.game.process_move(move)
        self.assertTrue(self.game.has_winner())  # Check if a winner is detected
        self.assertEqual(self.game.winner_combo, [(0, 0), (1, 0), (2, 0)])  # Check the winning combination

    def test_win_conditions_4x4(self):
        # Test for winning conditions on a 4x4 board (vertical win)
        moves_vertical_win = [
            Move(0, 0, "X"), Move(1, 0, "O"),
            Move(0, 1, "X"), Move(1, 1, "O"),
            Move(0, 2, "X")  # Last move completes the vertical win in the first column
        ]
        for move in moves_vertical_win:
            self.game.process_move(move)
        self.assertTrue(self.game.has_winner())  # Check if a winner is detected
        self.assertEqual(self.game.winner_combo, [(0, 0), (0, 1), (0, 2)])  # Check the winning combination

    def test_win_conditions_5x5(self):
        # Test for winning conditions on a 5x5 board (diagonal win)
        moves_diagonal_win = [
            Move(0, 0, "X"), Move(1, 0, "O"),
            Move(1, 1, "X"), Move(0, 1, "O"),
            Move(2, 2, "X")  # Last move completes the diagonal win from top-left to bottom-right
        ]
        for move in moves_diagonal_win:
            self.game.process_move(move)
        self.assertTrue(self.game.has_winner())  # Check if a winner is detected
        self.assertEqual(self.game.winner_combo, [(0, 0), (1, 1), (2, 2)])  # Check the winning combination

if __name__ == "__main__":
    unittest.main()
