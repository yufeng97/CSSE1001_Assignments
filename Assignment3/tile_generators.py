"""Tile generator classes for Lolo puzzle game."""

"""
                        /-------------\
                       /               \
                      /                 \
                     /                   \
                     |   XXXX     XXXX   |
                     |   XXXX     XXXX   |
                     |   XXX       XXX   |
                     \         X         /
                      --\     XXX     /--
                       | |    XXX    | |
                       | |           | |
                       | I I I I I I I |
                       |  I I I I I I  |
                        \              /
                          --         --
                            \-------/
                    XXX                    XXX
                  XXXXX                  XXXXX
                  XXXXXXXXX         XXXXXXXXXX
                          XXXXX   XXXXX
                            XXXXXXX
                          XXXXX   XXXXX
                  XXXXXXXXX         XXXXXXXXXX
                  XXXXX                  XXXXX
                    XXX                    XXX
                          **************
                          *  BEWARE!!  *
                          **************
                      All ye who enter here:
                 Most of the code in this module
                     is twisted beyond belief!
                        Tread carefully.
                 If you think you understand it,
                            You Don't,
                          So Look Again.
"""

import game_regular
from model import AbstractTileGenerator

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"


class LoadedGenerator(AbstractTileGenerator):
    """Tile generator based upon the values of a serialized grid."""

    def __init__(self, grid):
        """Constructor

        Parameters:
            grid (list<list<tuple<int, int>>>): The serialized grid.
        """
        print("WARNING: LoadedGenerator is deprecated and should no longer be used.")
        self._grid = grid

    def generate(self, position):
        """(AbstractTile) Generates a new tile."""
        data = self._grid[position[0]][position[1]]
        return game_regular.RegularTile(*data)


class WeightedGenerator(AbstractTileGenerator):
    """Tile generator based upon WeightedSelector value."""

    def __init__(self, selector, constructor):
        """Constructor

        Parameters:
            selector (WeightedSelector): The weighted selector to choose from.
            constructor (function):
                    Callable which returns the tile. Accepts two arguments:
                    constructor(selection, position)
                        - selection: The value returned from selector.choose()
                        - position: The position passed to the generate method.
        """
        self._selector = selector
        self._constructor = constructor

    def generate(self, position):
        """(AbstractTile) Generates a new tile."""
        return self._constructor(self._selector.choose(), position)