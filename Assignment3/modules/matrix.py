"""
Two-dimensional matrix data structure.
"""
import itertools

__author__ = "Benjamin Martin"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.0.0"

# Change in position for all adjacent cells.
RADIAL_DELTAS = tuple(
    cell for cell in itertools.product(*itertools.repeat((-1, 0, 1), 2)) if
    cell.count(0) <= 1)

# Change in position for all axially adjacent cells.
AXIAL_DELTAS = tuple(cell for cell in RADIAL_DELTAS if cell.count(0) == 1)

# Change in position for all diagonally adjacent cells.
DIAGONAL_DELTAS = tuple(cell for cell in RADIAL_DELTAS if cell.count(0) == 0)


class Matrix:
    """2d grid-like data structure.

    Key Terms:
        position: A (row, column) pair of coordinates.
        valid position: A position that exists in the matrix."""

    def __init__(self, rows=1, columns=1, default=None):
        """
        Constructor

        Parameters:-
            rows (int): The number of rows.
            columns (int): The number of columns.
            default (*): The default value. Defaults to None.

        Preconditions:
            rows & columns are both > 0
        """
        self._cells = [[default for _ in range(columns)] for _ in range(rows)]
        self._default = default
        self._dim = rows, columns

    def reset(self):
        """Resets all elements in this matrix to the default."""
        rows, columns = self._dim
        for i in range(rows):
            for j in range(columns):
                self._cells[i][j] = self._default

    def size(self):
        """(tuple<int, int>) Returns the size of this matrix."""
        return self._dim

    def __contains__(self, position):
        """Returns True iff position represents a valid (row, column) pair.

        Parameters:
            position (tuple<int, int>): A position to test.

        Return: bool"""
        if not all(a <= b < c for a, b, c in
                   zip(itertools.repeat(0, len(self._dim)), position,
                       self._dim)):
            # Coordinates out of range
            return False

        return True

    def __getitem__(self, position):
        """(*) Returns the value corresponding to the key.

        Parameters:
             position (tuple<int, int>): A position."""
        row, column = position
        return self._cells[row][column]

    def __setitem__(self, position, value):
        """Sets the value corresponding to the key.

        Parameters:
             position (tuple<int, int>): A position.
             value (*): The new value."""
        row, column = position
        self._cells[row][column] = value

    def __delitem__(self, key):
        """Deletes the key and corresponding value.

        Parameters:
             key (tuple<int, int>): A position."""
        row, column = key
        self._cells[row][column] = None

    def __iter__(self):
        """Yields (row, column) positions for every cell.

        Yield:
            (tuple<int, int>): (row, column) position"""
        yield from itertools.product(*(range(dim) for dim in self._dim))

    def items(self):
        """Yields (key, value) pairs for every cell, where key is the
        (row, column) position.

        Yield:
            (tuple<int, int>, *): (position, value) pair.
        """
        for cell in self:
            yield cell, self[cell]

    def get_rows(self):
        """Yields rows of values.

        Yield:
            list<*>: Values in each row.
        """
        yield from self._cells

    def get_adjacent_cells(self, position, deltas=AXIAL_DELTAS):
        """Yields adjacent cells from a given position.

        Parameters:
            position (int, int): A position.
            deltas (tuple(tuple<int, int>, ...)):
                Changes in position, each corresponding to an adjacent cell.
                Defaults to AXIAL_DELTAS.

        Yield:
            tuple<int, int>: Position of each adjacent cell.
        """
        for delta in deltas:
            neighbour = tuple(a + b for a, b in zip(position, delta))

            # ensure cell is valid
            if neighbour in self:
                yield neighbour
