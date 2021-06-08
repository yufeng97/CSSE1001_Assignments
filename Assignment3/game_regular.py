"""Modelling classes for Regular Lolo game mode."""

import tile_generators
import model
import modules.matrix as matrix
from modules.weighted_selector import WeightedSelector

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"


class RegularTile(model.AbstractTile):
    """Regular Lolo tile.

    When tiles whose values first exceed maximum value, their type & value are
    set to the maximum. Values higher than the maximum can exist when maximum
    tiles are joined (normally only in multiples of the maximum value)."""

    def __init__(self, type, value=1, max_type='max', max_value=50):
        """
        Constructor

        If type == max_type and value < max_value, then value = max_value

        Parameters:
            type (*): The type of this tile.
            value (int): The value of this tile. Defaults to 1.
            max_type (*): The type of a maximum tile.
            max_value (int): The value of a maximum tile.
        """

        super().__init__(type, value)

        self._max_type = max_type
        self._max_value = max_value

        if type == max_type and value < max_value:
            self.maximize()

    def get_display_value(self):
        """(int|None) Returns the display value of this tile."""
        value = self.get_value()
        return None if value == 1 else value

    def join(self, others):
        """
        Joins other tiles to this tile.

        Parameters:
            others (iterable(RegularTile)): The other tiles to join.
        """
        for other in others:
            if isinstance(other.get_value(), int):
                self._value += other.get_value()

        if self._type != self._max_type and self._value >= self._max_value:
            self.maximize()

    def maximize(self):
        """Converts this tile to a max tile."""
        self._value = self._max_value
        self._type = self._max_type

    def is_max(self):
        """(bool) Returns True iff this tile is a maximum tile."""
        return self._type == self._max_type

    def is_combo_max(self):
        """(bool) Returns True iff this tile is a combined maximum tile."""
        return self.is_max() and self._value > self._max_value

    def __eq__(self, other):
        """(bool) Returns True iff this tile's type is equivalent to other's.

        Parameters:
            other (RegularTile): The tile to check for equivalence.
        """
        return self._type == other.get_type()


class RegularGame(model.AbstractGame):
    """Regular game of Lolo.

    Join groups of three or more until max tiles are formed. Join max tiles to
    destroy all surrounding tiles."""

    GAME_NAME = "Regular"

    def __init__(self, size=(6, 6), types=3, min_group=3,
                 max_tile_value=50, max_tile_type='max', normal_weight=20,
                 max_weight=2, animation=True, autofill=True):
        """Constructor

        Parameters:
            size (tuple<int, int>): The number of (rows, columns) in the game.
            types (int): The number of types of basic tiles.
            min_group (int): The minimum number of tiles required for a
                             connected group to be joinable.
            normal_weight (int): The relative weighted probability that a basic
                                 tile will be generated.
            max_weight (int): The relative weighted probability that a maximum
                              tile will be generated.
            animation (bool): If True, animation will be enabled.
            autofill (bool): Automatically fills the grid iff True.
        """

        # Basic properties
        self.max_tile_value = max_tile_value
        self.max_tile_type = max_tile_type
        self.types = types
        self._max_unlocked = False

        # Tile probabilities
        self.normal_likelihood = normal_weight
        self.max_likelihood = max_weight

        weighted_types = {i: normal_weight for i in range(1, types + 1)}
        self._selector = WeightedSelector(weighted_types)

        generator = tile_generators.WeightedGenerator(self._selector,
                                                      self._construct_tile)

        super().__init__(size, generator, min_group, animation=animation,
                         autofill=autofill)

    def get_default_score(self):
        """(int) Returns the default score."""
        return 0

    def reset(self):
        """Resets the game."""
        super().reset()

        self._lock_max()

    def _construct_tile(self, type, position, *args, **kwargs):
        """(RegularTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """
        return RegularTile(type, *args, max_value=self.max_tile_value, **kwargs)

    def _check_unlock_max(self, current):
        """Unlocks the max tile if the current tile is a max tile.

        Parameters:
            current (RegularTile): The current tile.
        """
        if not self._max_unlocked and current.is_max():
            self._selector.update({
                self.max_tile_type: self.max_likelihood
            })
            self._max_unlocked = True

    def _lock_max(self):
        """Locks max tile."""
        del self._selector[self.max_tile_type]
        self._max_unlocked = False

    def update_score_on_activate(self, current, connected):
        """Updates the score based upon the current tile & connected tiles that
        were joined to it.

        Parameter:
            current (RegularTile): The tile recently current to.
            connected (tuple<RegularTiles>): The tiles that were joined to
                                              current.
        """
        factor = 50 if current.is_combo_max() else 1
        points = (len(connected) + 1) * factor
        self.set_score(self.get_score() + points)

    def activate(self, position):
        """Attempts to activate the tile at the given position.

        Parameters:
            position (tuple<int, int>): The position to activate.

        Yield:
            Yields None for each frame of drops and "DONE" when the dropping
            has finished.
        """
        connected_cells = self._attempt_activate_collect(position)
        connected_cells.remove(position)

        self._resolving = True

        current = self.grid[position]
        connected_tiles = [self.grid[cell] for cell in connected_cells]

        # Join tiles
        current.join(connected_tiles)

        self.update_score_on_activate(current, connected_tiles)

        self._check_unlock_max(current)

        for cell in connected_cells:
            del self.grid[cell]

        yield from self.grid.replace_blanks()

        # Find tile, in case it moved.
        # Hack, but it works. Ideally above logic would indicate movement.
        position = self.find_tile_position(current)

        # Perform combo
        yield from self._explode_combo(position)

        # Final step
        yield "DONE"

        self._resolving = False
        self.emit('resolve')

        # Check for game over.
        if self.game_over():
            self.emit('game_over')

    def remove(self, *positions):
        """Attempts to remove the tiles at the given positions.

        Parameters:
            *positions (tuple<int, int>): The position to activate.

        Yield:
            Yields None for each frame of drops and "DONE" when the dropping
            has finished.
        """

        self._resolving = True

        connected_cells = positions
        connected_tiles = [self.grid[cell] for cell in connected_cells]

        for cell in connected_cells:
            del self.grid[cell]

        yield from self.grid.replace_blanks()

        # Final step
        yield "DONE"

        self._resolving = False
        self.emit('resolve')

        # Check for game over.
        if self.game_over():
            self.emit('game_over')

    def find_tile_position(self, tile):
        """(tuple<int, int>) Returns the row, column position of the tile if it
        exists in the game grid, else None."""
        for position, a_tile in self.grid.items():
            if a_tile is tile:
                return position

        return None

    def _explode_combo(self, position):
        """Internal helper method to check if the tile at a position is a
        combination maximum. If so, explodes it, deleting the tile and all
        surrounding tiles.

        Parameters:
            position (tuple<int, int>): Row, column position of the tile.
        """
        current = self.grid[position]

        if current.is_combo_max():
            yield "REMOVE"

            exploded_cells = self.grid.get_adjacent_cells(
                position, deltas=matrix.RADIAL_DELTAS)

            del self.grid[position]

            for cell in exploded_cells:
                tile = self.grid[cell]
                if tile is None or not tile.get_disabled():
                    del self.grid[cell]

            self.set_score(self.get_score() + current.get_value())

            yield from self.grid.replace_blanks()
