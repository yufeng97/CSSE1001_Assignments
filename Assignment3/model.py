"""Abstract modelling classes for Lolo puzzle game."""

# To understand recursion, see the bottom of this file
import itertools

from modules import matrix as matrix
from modules.ee import EventEmitter

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"

class AbstractTile:
    """Basic form of a Lolo tile."""

    def __init__(self, type, value=1):
        """Constructor

        Parameters:
             type (*): The tile's type.
             value (int): The tile's value.
        """
        self._type = type
        self._value = value
        self._disabled = False

    def get_type(self):
        """(*) Returns the type of this tile."""
        return self._type

    def get_value(self):
        """(int) Returns the value of this tile."""
        return self._value

    def get_display_value(self):
        """(*) Returns the display value of this tile. None if the tile has no
        value to display."""
        return self.get_value()

    def get_disabled(self):
        """(bool) Returns True iff this tile is disabled. If a tile is disabled,
        it cannot move or be interacted with."""
        return self._disabled

    def join(self, others):
        """
        Joins other tiles to this tile.

        Parameters:
             others (iterable(BasicTile)): The other tiles to join.
        """
        raise NotImplementedError

    def disable(self):
        """Disables this tile."""
        self._disabled = True

    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self._type,
                                       self._value)

    def __str__(self):
        return self.__repr__()


class AbstractTileGenerator:
    """Buffer of tiles."""

    def generate(self, position):
        """(AbstractTile) Abstract method to return a new tile.

        Parameters:
            position (tuple<int, int>) The (row, column) position of the tile.
        """
        raise NotImplementedError


class LoloGrid(matrix.Matrix):
    """Generic Lolo game."""

    def __init__(self, tile_generator, rows=1, columns=1, default=None,
                 animation=True, connected=None):
        """Constructor

        Parameters:
            tile_generator (AbstractTileGenerator): The tile generator.
            rows (int): The number of rows in the game.
            columns (int): The number of columns in the game.
            default (*): The default value.
            animation (bool): Whether this game animates its resolution steps.
            connected (function): Called with (tile, neighbour). Returns True
                                  iff neighbour is connected to tile.

        Preconditions:
            connected is reflexive (connected(a, b) == connected(b, a))
        """
        super().__init__(rows, columns, default)

        self._animation = animation
        self._generator = tile_generator
        self._connected = lambda tile, neighbour: tile == neighbour

    def fill(self):
        """Fills all empty cells with newly generated tiles."""
        for position in self:
            if self[position] is None:
                tile = self.generate_tile(position)
                self[position] = tile

    # TODO: these should be on game :/
    # Move on and call me an idiot later.
    @classmethod
    def deserialize(cls, grid, *args, **kwargs):
        """Creates a new grid from the a given serialized grid.

        Parameters:
            grid (list<list<tuple<int, int>>>): A serialized grid list to load.
            generator (AbstractTileGenerator): The tile generator to use.

        Return:
            LoloGrid: A grid loaded from the serialized grid list.
        """

        raise NotImplementedError("ERROR: LoloGrid.deserialize is deprecated. See AbstractGame.deserialize instead.")

    def serialize(self):
        """Serializes the grid into a list so it can be saved in a file.

        Return:
            list<list<tuple<int, int>>>: The serialized grid.
        """
        print("WARNING: LoloGrid.serialize is deprecated. See AbstractGame.serialize instead.")
        grid_list = []
        for row in self.get_rows():
            row_list = []
            for tile in row:
                row_list.append((tile.get_type(), tile.get_value()))
            grid_list.append(row_list)
        return grid_list

    def toggle_animation(self):
        """(bool) Toggles animation and returns True iff animation is on."""
        self._animation = not self._animation

    def set_animation(self, animation=True):
        """Sets animation value."""
        self._animation = animation

    def find_connected(self, root, positions=None):
        """Finds all cells connected to the one at given position.

        Parameters:
            root (tuple<int, int>): The (row, column) position of the root cell.
            positions (set<tuple<int, int>>): The set of positions to search.

        Return:
            set<tuple<int, int>>: A set of (row, column) positions for each connected tile, including root.
        """

        # Default to all cells
        if not positions:
            positions = set(self)

        # Perform depth first search on matrix.
        # Treat adjacent cells as having edge iff they share the same type.

        # Initialize data structures
        nodes = []
        visited = set()

        nodes.append(root)

        while len(nodes):
            node = nodes.pop()

            if node not in visited:
                visited.add(node)

                # Iterate over adjacent nodes
                for adjacent in self.get_adjacent_cells(node):

                    if adjacent not in positions:
                        continue

                    # Ensure the type matches
                    if self._connected(self[root], self[adjacent]):
                        nodes.append(adjacent)

        return visited

    def generate_tile(self, position):
        """Uses the provided tile generator to generate a tile for a position."""
        return self._generator.generate(position)

    def find_all_connected(self):
        """Finds and yields all the connections within the grid.

        Yield:
            set<tuple<int, int>>: A set of (row, column) positions for each connected tile, including root.
        """
        positions = set(self)

        while len(positions):
            node = positions.pop()

            connected = self.find_connected(node, positions)

            if not connected:
                continue

            for cell in connected:
                if cell in positions:
                    positions.remove(cell)

            yield connected

    def replace_blanks(self):
        """Replaces any blank tiles in the grid and yields at each frame."""
        replacements = self.calculate_replacements()

        # Perform drops
        max_drops = max(r[0] for r in replacements)
        for i in range(max_drops):
            if self._animation:
                yield

            for empties, column, rows in replacements:
                if i >= empties:
                    continue

                for j in range(len(rows) - 1):
                    row = rows[j]

                    position = row, column
                    above_position = row - 1, column

                    tile = self[position]
                    above_tile = self[above_position]

                    if above_tile and not tile:
                        self[position] = above_tile
                        self[above_position] = None

                new_position = rows[-1], column
                new_tile = self.generate_tile(new_position)
                self[new_position] = new_tile

    def can_position_drop(self, position):
        """(bool) Returns true iff the tile can drop to the next position.

        Parameters:
            position (tuple<int, int>): The position of the tile to check.
        """
        if position not in self:
            return False

        tile = self[position]

        if tile is None:
            return True

        return not tile.get_disabled()

    def calculate_replacements(self):
        """Calculates the drops that need to occur to replace empty tiles.

        Return:
            (list<tuple<int, int, int>>): A list of the drops that need to occur
                                          for a tile to be replaced. Specified
                                          by a tuple (empties, column, rows).
        """
        rows, columns = self._dim

        drops = []
        drop = []

        for column in range(columns):

            empties = 0

            for row in range(rows - 1, -1, -1):
                position = row, column
                tile = self[position]

                if tile is None:
                    if empties == 0:
                        bottom_empty = position
                    empties += 1

                if not self.can_position_drop((row - 1, column)):
                    if empties == 0:
                        # ignore full rows
                        continue

                    drop.append(row)

                    info = (empties, column, drop)

                    empties = 0
                    drop = []

                    drops.append(info)
                elif empties:
                    # print('Can drop {}'.format(position))
                    drop.append(row)

        return drops

    @staticmethod
    def get_replacement_position(position):
        """(tuple<int, int>) Returns (row, column) position of the cell that would
        replace cell at given position.

        Parameters:
            position (tuple<int, int>): The position of the cell to replace.
        """

        row, column = position

        # I am not sure if we need this, but too scared to delete. ;)
        if row == 0:
            row = -row

        return row - 1, column


class AbstractGame(EventEmitter):
    """Abstract base class for a game of Lolo with helpful functionality across
    multiple game modes."""

    GAME_NAME = "Abstract"

    def __init__(self, size, generator, min_group, animation=True,
                 autofill=True):
        """Constructor

        Parameters:
            size (tuple<int, int>): The (row, column) size of the game.
            generator (AbstractTileGenerator): Generates tiles for the grid.
            min_group (int): The minimum number of tiles for a connection to
                             be a group.
            animation (bool): Animation is enabled iff True.
            autofill (bool): Automatically fills the grid iff True.
        """
        super().__init__()
        rows, columns = size
        self.grid = LoloGrid(generator, rows=rows, columns=columns,
                             animation=animation)
        self.generator = generator

        # Basic properties
        self.min_group = min_group
        self._animation = animation
        self._resolving = False

        if autofill:
            self.grid.fill()

            self._score = self.get_default_score()

    def get_default_score(self):
        """(int) Returns the default score."""
        raise NotImplementedError

    def is_resolving(self):
        """(bool) Returns True iff the game is resolving a move."""
        return self._resolving

    def find_groups(self):
        """Yields all the valid groups within the grid. Groups are connected and
        must have at least 'self.min_group' members.

        Yield:
            set<tuple<int, int>>: A set of (row, column) positions for each connected tile, including root.
        """

        for group in self.grid.find_all_connected():
            if len(group) < self.min_group:
                continue

            yield group

    def find_group(self, position):
        """Returns the group containing the tile at position, or None if no such
        group exists. A group must have at least 'self.min_group' members.

        Parameters:
            position (tuple<int, int>): Row, column position of the tile.

        Return:
            None: If tile is not part of a group.
            set<tuple<int, int>>: A set of (row, column) positions for each connected tile, including root.
        """
        group = self.grid.find_connected(position)

        if len(group) < self.min_group:
            return None

        return group

    def find_connections(self):
        """Returns a list of connection information for all grid positions.

        Return:
            list<tuple<tuple<int, int>, *, tuple<int, int>>>:
                Each tuple has form (position, cell_type, neighbour_position).
        """
        connections = []
        for group in self.find_groups():
            for position in group:
                cell = self.grid[position]
                for neighbour in filter(None,
                                        self.grid.get_adjacent_cells(position)):
                    if neighbour in group:
                        connections.append(
                            (position, cell.get_type(), neighbour))
        return connections

    def _attempt_activate_collect(self, position):
        """
        Returns cells connected to tile at position if activation is possible.

        Parameters:
            position (tuple<int, int>): Row, column position of the tile.

        Raises:
            IndexError: If tile could not be activated or game is currently
                        resolving.

        Return:
            (set<tuple<int, int>>): Positions of all cells connected to cell at
                                    position (including the cell itself).
        """
        if self._resolving:
            raise IndexError("Game is resolving.")

        connected_cells = self.grid.find_connected(position)

        if len(connected_cells) < self.min_group:
            raise IndexError("Tile at {} cannot be activated.".format(position))

        return connected_cells

    def activate(self, position):
        """Attempts to activate the tile at the given position.

        Raises:
            IndexError: If position cannot be activated.

        Yield:
            None: On each step of the resolution.
        """
        raise NotImplementedError

    def remove(self, *positions):
        """Removes the tile(s) at the given position(s).

        Yield:
            None: On each step of the resolution.
        """
        raise NotImplementedError

    def can_activate(self, position):
        """(bool) Returns true iff the given position can be activated."""
        try:
            self._attempt_activate_collect(position)
        except IndexError:
            return False

        return True

    def game_over(self):
        """(bool) Returns True iff the game is over."""
        for connected in self.grid.find_all_connected():
            if len(connected) < self.min_group:
                continue
            return False
        return True

    def reset(self):
        """Resets the game."""
        self.grid.reset()
        self.grid.fill()
        self.set_score(self.get_default_score())

    @classmethod
    def get_name(cls):
        """(str) Returns the name of the game."""
        return cls.GAME_NAME

    def get_score(self):
        """(int) Returns the score."""
        return self._score

    def update_score_on_activate(self, current, connected):
        """Updates the score based upon the current tile & connected tiles that
        were joined to it.

        Parameter:
            current (AbstractTile): The tile recently current to.
            connected (tuple<AbstractTiles>): The tiles that were joined to
                                              current.
        """
        raise NotImplementedError

    def set_score(self, score):
        """Sets the score."""
        self._score = score
        self.emit('score', score)

    def _construct_tile(self, type, position, *args, **kwargs):
        """(AbstractTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """
        raise NotImplementedError

    # de/serialize are designed to be backwards compatible with HighScoreManager from <= 1.1.1
    # Ideally, they would consider not just the grid but the entire game (i.e. all of __init__'s parameters).
    # However, this would be a breaking change, so only de/serialization of the grid is supported.
    # This will be changed in 1.2.0 (post-due-date update)
    def serialize(self):
        """
        Serializes this game.
        
        Return: 
            grid (list<list<tuple<int, int>>>): The serialized grid.
        """
        grid_list = []
        for row in self.grid.get_rows():
            row_list = []
            for tile in row:
                row_list.append((tile.get_type(), tile.get_value()))
            grid_list.append(row_list)
        return grid_list

    @classmethod
    def deserialize(cls, grid, *args, **kwargs):
        """
        Deserializes a game grid.
        
        Parameters: 
            grid (list<list<tuple<int, int>>>): A serialized grid list to load.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """

        # TODO: This line should be included, but causes an error with the current design.
        #       Error occurs for games that assume tiles are generated (i.e. unlimited)
        # kwargs['autofill'] = False

        game = cls(*args, **kwargs)

        for row, row_data in enumerate(grid):
            for column, data in enumerate(row_data):
                type, *rest = data
                game.grid[(row, column)] = game._construct_tile(type, (None, None), *rest)

        return game


# To understand recursion, see the top of this file
