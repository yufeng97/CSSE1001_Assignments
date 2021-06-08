"""Plays a game of Lolo."""

import tkinter as tk

import a3
import game_lucky7
import game_make13
import game_regular
import game_unlimited

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"


def main():
    """Plays a game."""

    game = game_regular.RegularGame()
    # game = game_make13.Make13Game()
    # game = game_lucky7.Lucky7Game()
    # game = game_unlimited.UnlimitedGame()

    root = tk.Tk()
    app = a3.LoloApp(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()


