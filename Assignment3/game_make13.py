"""Modelling classes for Make 13 Lolo game mode."""
import tile_generators

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"

import model
import game_regular
from modules.weighted_selector import WeightedSelector


class LevelTile(model.AbstractTile):
    """Tile whose value & type are equal, incrementing by one when joined."""

    def __init__(self, value=1):
        """Constructor

        Parameters:
             value (int): The tile's value.
        """
        super().__init__(None, value)

    def get_type(self):
        """Returns the type (value) of this tile."""
        return self.get_value()

    def is_max(self):
        return False

    def is_combo_max(self):
        return False

    def join(self, others):
        """
        Joins other tiles to this tile.

        Parameters:
             others (iterable(BasicTile)): The other tiles to join.
        """

        self._value += 1

    def __eq__(self, other):
        return self._value == other._value


class Make13Game(game_regular.RegularGame):
    """Make13 Lolo game.

    Groups of two or more can be combined to increase tile's value by one.

    Game is won when a 13 is made.
    """

    GAME_NAME = "Make 13"

    def __init__(self, size=(6, 6), initial_tiles=4, goal_value=13, min_group=2,
                 animation=True, autofill=True):
        """Constructor

        Parameters:
            size (tuple<int, int>): The number of (rows, columns) in the game.
            initial_tiles (int): The number of tiles.
            goal_value (int): The value of the goal tile.
            min_group (int): The minimum number of tiles required for a
                             connected group to be joinable.
            animation (bool): If True, animation will be enabled.
            autofill (bool): Automatically fills the grid iff True.

        """
        self.goal_value = goal_value

        self.initial_tiles = initial_tiles

        super().__init__(size=size, min_group=min_group, animation=animation,
                         autofill=False)

        self._selector = WeightedSelector({1: 1})
        self.reset()

        generator = tile_generators.WeightedGenerator(self._selector,
                                                      self._construct_tile)

        rows, columns = size
        self.grid = model.LoloGrid(generator, rows=rows, columns=columns,
                                   animation=animation)
        if autofill:
            self.grid.fill()
            self._score = self.get_default_score()

        self.generator = generator

    def get_default_score(self):
        """(int) Returns the default score."""
        return max(tile.get_value() for _, tile in self.grid.items())

    def reset(self):
        """Resets the game."""
        weights = {i: self.get_tile_weight(i) for i in
                   range(1, self.initial_tiles + 1)}
        self._selector.update(weights, clear=True)
        super().reset()

    def get_tile_weight(self, value):
        """(float) Returns the weighting for a tile of given value."""
        return 2 ** (self.goal_value - value)

    def _construct_tile(self, type, position, *args, **kwargs):
        """(LevelTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """

        # TODO: remove when serialize is implemented properly
        args = args[1:]

        return LevelTile(type, *args, **kwargs)

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
            self._score = score

            # Unlock new tile
            self._selector[score] = self.get_tile_weight(score)

            self.set_score(score)

        if current.get_value() == self.goal_value:
            self.emit('game_over')
