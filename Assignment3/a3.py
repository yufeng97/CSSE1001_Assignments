"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

import random
import sys
import tkinter as tk

from game_regular import RegularGame
from game_make13 import Make13Game
from game_lucky7 import Lucky7Game
from game_unlimited import UnlimitedGame
from tkinter import messagebox
from highscores import HighScoreManager
from base import BaseLoloApp

__author__ = "Yufeng Liu"
__email__ = "yufeng.liu1@uqconnect.edu.au"

__version__ = "1.0.2"


class LoadingScreen:
    """Widget that contains three Frames, one Entry and three Buttons."""

    def __init__(self, master):
        """The loading screen of LoloApp.

        Constructor:
            master (tk.Tk|tk.Frame): The parent widget.
            game (model.AbstractGame): The game displayed as a example.

        """
        self._master = master
        # Title
        self._master.title("Lolo")
        # LoloLogo
        self.lolologo = LoloLogo(master)
        self.lolologo.pack(side=tk.TOP, expand=False)
        # Label Frame
        self.label_frame = tk.Frame(master)
        self.label_frame.pack(side=tk.TOP)
        # Label
        self.entry_label = tk.Label(self.label_frame, text="Your name:")
        self.entry_label.pack(side=tk.LEFT, expand=True)
        # Entry
        self.entry = tk.Entry(self.label_frame, width=30)
        self.entry.pack(side=tk.RIGHT, expand=True)
        # Buttons Frame
        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=30)
        # PlayGame Button
        self.play_game_button = tk.Button(self.buttons_frame, text="Play Game", command=self.start_game)
        self.play_game_button.pack(side=tk.TOP, expand=True, ipadx=50)
        # GameMode Button
        self.game_mode_button = tk.Button(self.buttons_frame, text="Game Mode", command=self.game_mode)
        self.game_mode_button.pack(expand=True, ipadx=50)
        # HighScores Button
        self.high_scores_button = tk.Button(self.buttons_frame, text="High Scores", command=self.high_scores)
        self.high_scores_button.pack(side=tk.TOP, expand=True, ipadx=50)
        # ExitGame Button
        self.exit_game_button = tk.Button(self.buttons_frame, text="Exit Game", command=self.exit_game)
        self.exit_game_button.pack(side=tk.TOP, expand=True, ipadx=50)
        # Game
        AutoPlayingGame(master)
        # Get player's name
        self.player = self.entry.get()

    def start_game(self):
        """Play the game."""
        self._master.withdraw()
        game = GameMode.get_game()
        window = tk.Toplevel()
        app = LoloApp(window, game, self.player, parent=self)

    def exit_game(self):
        """Exits the application."""
        self._master.destroy()
        sys.exit()

    def high_scores(self):
        """Widget that display the highscores."""
        new_window = tk.Toplevel()
        HighScore(new_window)

    def game_mode(self):
        new_window = tk.Toplevel()
        game_mode = GameMode(new_window)


# Define your classes here
class LoloApp(BaseLoloApp):
    """A basic game window design."""

    def __init__(self, master, game, player=None, parent: LoadingScreen = None):
        """Basic game idea, has menubar, LoloLogo, Statusbar, game
        and lightning_button Button.

        Constructor:
            master (tk.Tk|tk.Frame): The parent widget.
            game (model.AbstractGame)
        
        """
        self._master = master
        self._game = game
        self._player = player
        self.parent = parent
        # Title
        self._master.title("Lolo :: {} Game")
        # LoloLogo
        self.lolologo = LoloLogo(master)
        self.lolologo.pack(side=tk.TOP, expand=False)
        # Status bar
        self.statusbar = StatusBar(master)
        self.statusbar.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        # Game
        super().__init__(self._master, self._game)
        # lightning_button Button
        self.lightning_button = tk.Button(master, text="Lightning(1)", command=self.toggle_lightning_button)
        self.lightning_button.pack(side=tk.BOTTOM, expand=True)
        # File menu
        self.setup_menu(self._master)
        # Keyboard Shortcuts
        self._master.bind("<Control-n>", self.new_game_shortcut)
        self._master.bind("<Control-l>", self.toggle_lightning_button_shortcut)
        # Refresh the game and score
        self._master.title("Lolo :: {} Game".format(self._game.get_name()))

        self._master.protocol("WM_DELETE_WINDOW", self.return_to_menu)
        self.statusbar.set_game(self._game.get_name())
        # Holds the current state of the lightning_button Button
        self._lightning_button_on = False
        self._lightning_button_num = 1

    def return_menu(self):
        self.parent._master.deiconify()

    def setup_menu(self, master):
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        # tell master what it's menu is
        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self.new_game, accelerator='Ctrl+N')
        filemenu.add_command(label="High Score", command=self.high_score)
        filemenu.add_command(label="Menu", command=self.return_to_menu)
        filemenu.add_command(label="Exit", command=self.close)

    def new_game(self):
        """Restarts the game."""
        self._game.reset()
        self._grid_view.draw(self._game.grid, self._game.find_connections())
        self._game.set_score(0)
        self._lightning_button_on = False
        self._lightning_button_num = 1

    def new_game_shortcut(self, event):
        """Restarts the game by keyboard shortcut.

        Parameters:
            event: Shortcut key: Ctrl+N
        """
        self.new_game()

    def close(self):
        """Exits the application."""
        self._master.destroy()
        sys.exit()

    def return_to_menu(self):
        self._master.destroy()
        main()

    def toggle_lightning_button(self):
        """Activate the lightning_button button."""
        if not self._lightning_button_on:
            self.lightning_button.config(text="Striking({})".format(self._lightning_button_num))
        else:
            self.lightning_button.config(text="Lightning({})".format(self._lightning_button_num))
        self._lightning_button_on = not self._lightning_button_on

    def toggle_lightning_button_shortcut(self, event):
        """Activate the lightning_button button by keyboard shortcut.

        Parameters:
            event: Shortcut key: Ctrl+L
        """
        self.toggle_lightning_button()

    def score(self, points):
        """Handles increase in score."""
        self.statusbar.set_score(self._game.get_score())

    def game_over(self):
        """Handles the game ending."""
        if self._lightning_button_num == 0 and self._game.game_over():
            messagebox.showinfo(title="Game Over",
                                message="Game over. Your score is {}, better luck next time! ".format(
                                    self._game.get_score()))

    def activate(self, position):
        """Attempts to activate the tile at the given position.

        Parameters:
            position (tuple<int, int>): Row-column position of the tile.
        """
        if not self._lightning_button_on:  # button is off
            if self._game.can_activate(position):
                super().activate(position)
                i = random.randint(1, 100)
                if 50 <= i < 60:
                    self._lightning_button_num += 1
                    self.lightning_button.config(state="normal",
                                                 text="Lightning({})".format(self._lightning_button_num))
            else:
                warning = "Cannot activate position {}".format(position)
                messagebox.showinfo(title="Invalid Activation", message=warning)
        else:  # button is on
            self.remove(position)
            self._lightning_button_num -= 1
            self.toggle_lightning_button()
            if self._lightning_button_num == 0:
                self.lightning_button.config(state=tk.DISABLED, text="Lightning({})".format(self._lightning_button_num))

    def high_score(self):
        new_window = tk.Toplevel()
        HighScore(new_window)


class StatusBar(tk.Frame):
    """Class for status bar"""

    def __init__(self, parent):
        """Display the name of game mode the player is currently playing
        and update latest the player's score.

        :param parent: The parent widget to display status bar
        """
        super().__init__(parent)
        self.game_label = tk.Label(self, text="Game")
        self.game_label.pack(side=tk.LEFT)
        self.score_label = tk.Label(self, text="Score: 0")
        self.score_label.pack(side=tk.RIGHT)

    def set_game(self, game_mode):
        """Change the display of game name. 

        Parameter:
            game_mode(str): The game name
        """
        self.game_label.config(text="{} Game".format(game_mode))

    def set_score(self, score):
        """Change the display of score.

        Parameter:
            score(int)
        """
        self.score_label.config(text="Score: {}".format(score))


class LoloLogo(tk.Canvas):
    """Widget that contains two polygons and four circles."""

    def __init__(self, parent):
        """A canvas display LoloLogo.

        :param parent: The parent widget to display LoloLogo
        """
        super().__init__(parent, width=350, height=100)
        # First character L
        self.create_polygon([(25, 10), (45, 10), (45, 70), (90, 70), (90, 90), (25, 90)], fill="purple")
        centre1 = (135, 55)
        radius_big = 35
        radius_small = 17
        # Second character O
        self.create_oval(centre1[0] - radius_big, centre1[1] - radius_big,
                         centre1[0] + radius_big, centre1[1] + radius_big,
                         fill="purple", outline="purple")
        self.create_oval(centre1[0] - radius_small, centre1[1] - radius_small,
                         centre1[0] + radius_small, centre1[1] + radius_small,
                         fill="white", outline="purple")
        # Third character L
        self.create_polygon([(190, 10), (210, 10), (210, 70), (255, 70), (255, 90), (190, 90)], fill="purple")
        centre2 = (300, 55)
        # Fourth Character O
        self.create_oval(centre2[0] - radius_big, centre2[1] - radius_big,
                         centre2[0] + radius_big, centre2[1] + radius_big,
                         fill="purple", outline="purple")
        self.create_oval(centre2[0] - radius_small, centre2[1] - radius_small,
                         centre2[0] + radius_small, centre2[1] + radius_small,
                         fill="white", outline="purple")


class HighScore(BaseLoloApp):
    """Widget that contains one grid, one label and three Buttons."""

    def __init__(self, master, grid_view=None):
        self._master = master
        self._master.title("High Scores :: Lolo")
        self._highscore = HighScoreManager()
        # Best Player
        best_player_label = tk.Label(master, text="Best Player: {} with {} points!")
        best_player_label.pack(side=tk.TOP, expand=True)
        best_player_label.config(text="Best Player: {} with {} points!".format(
            self._highscore.get_sorted_data()[0].get("name"),
            self._highscore.get_sorted_data()[0].get("score")))

        # Create High Score gird
        grid_list = self._highscore.get_sorted_data()[0].get("grid")
        game = RegularGame.deserialize(grid_list)
        super().__init__(master, game, grid_view)

        # Text LeaderBoard
        leader_board_label = tk.Label(master, text="LeaderBoard")
        leader_board_label.pack(side=tk.TOP)
        # Players frame
        players_frame = tk.Frame(master)
        players_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
        # Name frame
        name_frame = tk.Frame(players_frame)
        name_frame.pack(side=tk.LEFT)
        # Score frame
        score_frame = tk.Frame(players_frame)
        score_frame.pack(side=tk.RIGHT)
        # Update name and score label
        for i in range(10):
            # Player's name
            name_label = tk.Label(name_frame, text="{}".format(self._highscore.get_sorted_data()[i]["name"]))
            name_label.pack(side=tk.TOP, anchor=tk.W)
            # Player's score
            score_label = tk.Label(score_frame, text="{}".format(self._highscore.get_sorted_data()[i]["score"]))
            score_label.pack(side=tk.TOP, anchor=tk.E)


class AutoPlayingGame(BaseLoloApp):
    def __init__(self, master, game=None):
        super().__init__(master, game)
        self._move_delay = 1500
        self.move()

    def bind_events(self):
        self._game.on('resolve', self.resolve)

    def resolve(self, delay=None):
        if delay is None:
            delay = self._move_delay
        self._master.after(delay, self.move)

    def move(self):
        connections = list(self._game.find_groups())
        if connections:
            cells = []
            for connection in connections:
                for cell in connection:
                    cells.append(cell)
            self.activate(random.choice(cells))
        else:
            self._game.reset()
            self._grid_view.draw(self._game.grid, self._game.find_connections())
            self.resolve()

    def reset(self):
        self._game.reset()
        self._grid_view.draw(self._game.grid)

    def game_over(self):
        self.reset()


class GameMode:
    """Game mode selection window."""
    GAME_MODE = 1

    def __init__(self, master):
        """Constructor.

           Parameters:
              master (tk.Tk|tk.Frame|tk.TopLevel): The parent widget.
        """
        self._master = master
        self._master.title("Game Mode")
        frame = tk.Frame(master)
        frame.pack()
        label = tk.Label(frame, text="Choose a game mode:")
        label.pack()
        self.var = tk.IntVar()
        self.var.set(self.GAME_MODE)
        self.game_modes = [
            (RegularGame, 1),
            (Make13Game, 2),
            (Lucky7Game, 3),
            (UnlimitedGame, 4)
        ]
        self.buttons = []
        for game, val in self.game_modes:
            button = tk.Radiobutton(frame, text=game.get_name(), variable=self.var, value=val)
            self.buttons.append(button)
            button.pack()
        ok_button = tk.Button(frame, text="OK", command=self.confirm)
        ok_button.pack()

    def confirm(self):
        self._master.destroy()
        selection = self.var.get()
        self.var.set(selection)
        self.set_class_var(selection)

    @classmethod
    def set_class_var(cls, game_mode):
        cls.GAME_MODE = game_mode

    @classmethod
    def get_game(cls):
        choice = cls.GAME_MODE
        if choice == 1:
            return RegularGame()
        elif choice == 2:
            return Make13Game()
        elif choice == 3:
            return Lucky7Game()
        else:
            return UnlimitedGame()


def main():
    # Your GUI instantiation code here
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
