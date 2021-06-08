"""Modelling classes for Lucky 7 Lolo game mode."""

import game_regular
import game_make13

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"


class LuckyTile(game_make13.LevelTile):
    """Tile whose value & type are equal, incrementing by one when joined."""

    def __init__(self, value=1, lucky=7):
        """Constructor

        Parameters:
             value (int): The tile's value.
             lucky (int): The value of a lucky (exploding) tile.
        """
        super().__init__(value)
        self._lucky = lucky

    def is_max(self):
        return self.get_value() == self._lucky

    def is_combo_max(self):
        return self.is_max()


class Lucky7Game(game_make13.Make13Game):
    """Lucky7 Lolo game.

    Groups of three or more can be combined to increase tile's value by one.

    When lucky 7 tiles are formed, they explode, removing surrounding tiles.
    """

    GAME_NAME = "Lucky 7"

    def __init__(self, size=(6, 6), initial_tiles=4, lucky_value=7, min_group=3,
                 animation=True, autofill=True):
        """Constructor

        Parameters:
            size (tuple<int, int>): The number of (rows, columns) in the game.
            initial_tiles (int): The number of tiles.
            lucky_value (int): The value of the lucky tile.
            min_group (int): The minimum number of tiles required for a
                             connected group to be joinable.
            animation (bool): If True, animation will be enabled.
            autofill (bool): Automatically fills the grid iff True.
        """

        self.lucky_value = lucky_value

        super().__init__(size=size, initial_tiles=initial_tiles,
                         goal_value=lucky_value + 1, min_group=min_group,
                         animation=animation, autofill=autofill)

    def get_default_score(self):
        """(int) Returns the default score."""
        return 0

    def _construct_tile(self, type, position, *args, **kwargs):
        """(LuckyTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """

        if 'lucky' not in kwargs:
            kwargs['lucky'] = self.lucky_value

        # TODO: remove when serialize is implemented properly
        args = args[1:]

        return LuckyTile(type, *args, **kwargs)

    def update_score_on_activate(self, current, connections):
        """Updates the score based upon the current tile & connected tiles that
        were joined to it.

        Parameter:
            current (AbstractTile): The tile recently current to.
            connected (tuple<AbstractTiles>): The tiles that were joined to
                                              current.
        """
        value = current.get_value()

        if value == 1:
            score = 5
        elif value == self.lucky_value:
            score = (value - 2) * 20
        else:
            score = (value - 1) * 10

        self.set_score(self.get_score() + score)

    def activate(self, position):
        """Attempts to activate the tile at the given position.

        Parameters:
            position (tuple<int, int>): The position to activate.

        Yield:
            Yields None for each frame of drops and "DONE" when the dropping
            has finished.
        """
        return game_regular.RegularGame.activate(self, position)

    def _check_unlock_max(self, current):
        """Max tile cannot be unlocked in Lucky 7"""
