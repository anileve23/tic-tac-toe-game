import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""  # Default value for the label attribute

class TicTacToeGame:
    def __init__(self, players, board_size):
        # Initialize the game with players, board size, and necessary attributes
        self._players = cycle(players)  # Use cycle to alternate players' turns
        self.board_size = board_size
        self.current_player = next(self._players)  # Set the current player
        self.winner_combo = []  # Initialize an empty list for winner's combination
        self._current_moves = [[Move(row, col) for col in range(board_size)] for row in range(board_size)]
        # Create a 2D array of Move objects representing the board
        self._has_winner = False  # Initialize the winner status
        self._winning_combos = self._get_winning_combos()  # Calculate all possible winning combinations

    def _get_winning_combos(self):
        # Method to generate all possible winning combinations on the board
        # It includes rows, columns, and diagonal combinations
        # Each combination is represented as a list of tuples (row, column)
        # The function returns a list containing all winning combinations
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        diagonals = [[row[i] for i, row in enumerate(rows)], [col[j] for j, col in enumerate(reversed(columns))]]
        winning_combos = rows + columns + diagonals

        for i in range(self.board_size):
            for j in range(self.board_size):
                if j + 2 < self.board_size:
                    winning_combos.extend([[(i, j), (i, j + 1), (i, j + 2)]])
                if i + 2 < self.board_size:
                    winning_combos.extend([[(i, j), (i + 1, j), (i + 2, j)]])
                if i + 2 < self.board_size and j + 2 < self.board_size:
                    winning_combos.extend([[(i, j), (i + 1, j + 1), (i + 2, j + 2)]])
                if i - 2 >= 0 and j + 2 < self.board_size:
                    winning_combos.extend([[(i, j), (i - 1, j + 1), (i - 2, j + 2)]])
        
        return winning_combos

    def toggle_player(self):
        # Method to switch the current player for the next turn
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        # Method to check if a move is valid
        # It verifies if the move is within the board's bounds and the cell is empty
        return not self._has_winner and self._current_moves[move.row][move.col].label == ""

    def process_move(self, move):
        # Method to process the player's move
        # Updates the board with the player's move and checks for a win or tie
        # If a win is detected, sets the has_winner flag and stores the winning combination
        row, col = move.row, move.col
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self._current_moves[row][col].label == "":
                self._current_moves[row][col] = move
            for combo in self._winning_combos:
                results = set(self._current_moves[n][m].label for n, m in combo)
                is_win = (len(results) == 1) and ("" not in results)
                if is_win:
                    self._has_winner = True
                    self.winner_combo = combo
                    break

    def has_winner(self):
        # Method to check if the game has a winner
        return self._has_winner

    def is_tied(self):
        # Method to check if the game ended in a tie
        # It counts the number of played moves and compares it with the total possible moves
        played_moves = sum(1 for row in self._current_moves for move in row if move.label)
        return not self._has_winner and played_moves == self.board_size * self.board_size

    def reset_game(self):
        # Method to reset the game
        # Resets the board, winner status, and winning combination
        self._current_moves = [[Move(row, col) for col in range(self.board_size)] for row in range(self.board_size)]
        self._has_winner = False
        self.winner_combo = []

class TicTacToeBoard(tk.Tk):
    # Class representing the graphical interface of the Tic-Tac-Toe game
    # Inherits from tkinter.Tk
    def __init__(self, game):
        # Initialize the GUI for the game
        super().__init__()  # Call the constructor of the superclass
        self.title("Tic-Tac-Toe Game")  # Set the window title
        self._cells = {}  # Dictionary to store button positions
        self._game = game  # Keep a reference to the game logic
        self._create_menu()  # Create the menu bar
        self._create_board_display()  # Create the display for messages
        self._create_board_grid()  # Create the grid for the game board

    def _create_menu(self):
        # Method to create the menu bar for the game window
        # It includes options for playing again and exiting the game
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        # Method to create the display area for game messages
        # Uses a label widget to show messages (e.g., player's turn, winner, etc.)
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        # Method to create the grid of buttons for the game board
        # Initializes buttons and binds them to the 'play' method
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        # Method to handle a player's move when a button is clicked
        # Determines the clicked cell, updates the game, and updates the display
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label, fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue", text="", fg="black")

def choose_players():
    player_choice = input("Player 1, choose 'x' or 'o': ").lower()
    while player_choice not in ['x', 'o']:
        player_choice = input("Invalid choice. Please choose 'x' or 'o': ").lower()

    return [Player(label="x", color="purple"), Player(label="o", color="orange")] if player_choice == 'x' else [
        Player(label="o", color="orange"), Player(label="x", color="purple")]

def choose_board_size():
    size = input("Enter board size (3, 4, or 5): ")
    while size not in ['3', '4', '5']:
        size = input("Invalid size. Please choose between 3, 4, or 5: ")
    return int(size)

def main():
    players = choose_players()  # Get the player choices
    board_size = choose_board_size()  # Get the board size
    game = TicTacToeGame(players, board_size)  # Initialize the game logic
    board = TicTacToeBoard(game)  # Create the GUI with the game logic
    board.mainloop()  # Start the GUI main loop

if __name__ == "__main__":
    main() # Run the game when the script is executed directly
