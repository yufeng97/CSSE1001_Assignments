"""Modelling classes for Unlimited Lolo game mode."""

import math

import game_regular

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"


class UnlimitedGame(game_regular.RegularGame):
    """Unlimited Lolo game.

    The goal of the game is to form the largest possible tile."""

    GAME_NAME = "Unlimited"

    def __init__(self, size=(8, 8), types=4, min_group=3,
                 animation=True, autofill=True):
        """Constructor

        Parameters:
            size (tuple<int, int>): The number of (rows, columns) in the game.
            types (int): The number of tiles.
            min_group (int): The minimum number of tiles required for a
                             connected group to be joinable.
            animation (bool): If True, animation will be enabled.
            autofill (bool): Automatically fills the grid iff True.
        """

        super().__init__(size=size, types=types, min_group=min_group,
                         animation=animation, autofill=autofill)

    def get_default_score(self):
        """(int) Returns the default score."""
        return max(tile.get_value() for _, tile in self.grid.items())

    def _construct_tile(self, type, position, *args, **kwargs):
        """(RegularTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """
        return game_regular.RegularTile(type, *args, max_value=math.inf, **kwargs)

    def update_score_on_activate(self, current, connections):
        """Updates the score based upon the current tile & connected tiles that
        were joined to it.

        Parameter:
            current (AbstractTile): The tile recently current to.
            connected (tuple<AbstractTiles>): The tiles that were joined to
                                              current.
        """
        if current.get_value() > self._score:
            # Update score
            score = current.get_value()

            self.set_score(score)
