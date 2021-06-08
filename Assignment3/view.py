"""Contains GridView for Lolo tile game."""

"""
                                                 ,  ,
                                               / \/ \
                                              (/ //_ \_
     .-._                                      \||  .  \
      \  '-._                            _,:__.-"/---\_ \
 ______/___  '.    .--------------------'~-'--.)__( , )\ \
`'--.___  _\  /    |             Here        ,'    \)|\ `\|
     /_.-' _\ \ _:,_          Be Dragons           " ||   (
   .'__ _.' \'-/,`-~`                                |/
       '. ___.> /=,|  Abandon hope all ye who enter  |
        / .-'/_ )  '---------------------------------'
        )'  ( /(/
             \\ "
              '=='
"""

import tkinter as tk

from modules.ee import EventEmitter

from colours import VIBRANT_COLOURS

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.2"


def dict_defaults(dictionary, *others):
    """Adds key-value pairs from others to dictionary, unless the key already
    exists in dictionary. A value from others[i] will take precedence over
    a value from others[i+1].

    Parameters:
        dictionary (dict): The dictionary to fill with defaults.
        *others (tuple<dict>): The other dictionaries.
        """

    for other in others:
        for key, value in other.items():
            if key not in dictionary:
                dictionary[key] = other[key]


class GridView(EventEmitter, tk.Canvas):
    """Canvas which displays a grid of tiles representing the Lolo game board"""

    # The colour of each tile type
    COLOURS = {
        'max': VIBRANT_COLOURS['dark_grey'],
        'blank': VIBRANT_COLOURS['cream'],
        1: VIBRANT_COLOURS['red'],
        2: VIBRANT_COLOURS['blue'],
        3: VIBRANT_COLOURS['yellow'],
        4: VIBRANT_COLOURS['blue_purple'],
        5: VIBRANT_COLOURS['pink'],
        6: VIBRANT_COLOURS['orange'],
        7: VIBRANT_COLOURS['dark_grey'],
        8: VIBRANT_COLOURS['green'],
        9: VIBRANT_COLOURS['brown'],
        10: VIBRANT_COLOURS['dark_blue'],
        11: VIBRANT_COLOURS['pale_blue'],
        12: VIBRANT_COLOURS['beige'],
        13: VIBRANT_COLOURS['lime']
    }

    def __init__(self, master, size, cell_size=(70, 70),
                 border=(8, 8), colours=None, **kwargs):
        """
        Constructs a GridView based off a tkinter parent and LoloGrid.

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            game (RegularGame): The game that the view is displaying.
            size (tuple<int, int>): The (row, column) size of the grid.
            cell_size (tuple<int, int>): The size of each cell in pixels.
            border (tuple<int, int>): Size of the gap between cells in pixels.
            colours (dict): Map between the tile type and the colour to display.
                            Extends COLOURS property on class.
            kwargs (dict): Any other keyword arguments for the Frame constructor.
        """
        # Set dimensions
        self.size = size
        self.cell_size = cell_size
        self.border = border
        self.offsets = self._calculate_offsets()

        # Override default colours
        colours = {} if colours is None else colours.copy()
        dict_defaults(colours, self.COLOURS)

        # Super inits.
        EventEmitter.__init__(self)

        width, height = self.calculate_size()
        tk.Canvas.__init__(self, master, width=width, height=height,
                           **kwargs, highlightthickness=0)
        self._master = master

        self._tiles = {}
        self._colours = colours

        # items to be removed from the canvas
        self._connections = []
        self._texts = []

        self.bind("<Button-1>", self._handle_click)

    def calculate_size(self):
        """(tuple<int, int>) Returns the widget's required xy dimensions."""
        rows, columns = self.size
        cell_x, cell_y = self.cell_size
        pad_x, pad_y = self.border
        width = columns * cell_x + (columns + 1) * pad_x
        height = rows * cell_y + (rows + 1) * pad_y

        return width, height

    def _calculate_offsets(self):
        """Calculates the offsets between each cell for showing connections."""
        x, y = self.border

        return (
            ((0, y), (0, 0), (0, -y)),
            ((x, 0), (0, 0), (-x, 0))
        )

    def xy_to_rc(self, xy):
        """(tuple<int, int>) Converts xy position into row-column position."""
        x, y = xy
        cell_x, cell_y = self.cell_size
        pad_x, pad_y = self.border

        column = x // (pad_x + cell_x)
        on_column_padding = x % (pad_x + cell_x) < pad_x
        row = y // (pad_y + cell_y)
        on_row_padding = y % (pad_y + cell_y) < pad_y

        if on_column_padding or on_row_padding:
            return None

        return row, column

    def _handle_click(self, event):
        """Handle a mouse click on the game board by starting a move.

        Parameters:
            event (tk.MouseEvent): The event caused by a mouse click.
        """
        pad_x, pad_y = self.border
        x, y = self.cell_size

        position = self.xy_to_rc((event.x, event.y))

        if position is None:
            return

        self.emit('select', position)

    def reset(self):
        """Removes all tiles."""
        raise NotImplementedError("Soon to be removed.")

    def calculate_bounds(self, position):
        """Calculates the bounds of a tile at the given position in the grid.

        Parameters:
            position (tuple<int, int>): The (row, column) position of the tile.

        Return:
            (tuple<int, int, int>): The top left, middle and bottom right
                                    position of the tile on the GridView.
        """

        row, column = position

        cell_x, cell_y = self.cell_size
        pad_x, pad_y = self.border

        top = row * (pad_y + cell_y) + pad_y
        left = column * (pad_x + cell_x) + pad_x
        bottom = top + cell_y
        right = left + cell_x

        top_left = left, top
        bottom_right = right, bottom

        middle = left + cell_x // 2, top + cell_y // 2

        return top_left, middle, bottom_right

    def _draw_connection(self, tile, type, neighbour):
        """Draws a connection between two tiles in the grid.

        Parameters:
            tile (tuple<int, int>): The position of one tile.
            type (int): The type of the connection to draw.
            neighbour (tuple<int, int>): The position of another tile.
        """
        top_left, middle, bottom_right = self.calculate_bounds(tile)
        colour = self._colours[type]

        x, y = tuple(tile[i] - neighbour[i] for i in (0, 1))
        border = self.border

        offset = [0, 0]
        if y > 0:
            offset[0] = border[0] * -1
        if y < 0:
            offset[0] = border[0]
        if x > 0:
            offset[1] = border[1] * -1
        if x < 0:
            offset[1] = border[1]

        top_left = tuple(x + y for x, y in zip(top_left, offset))
        bottom_right = tuple(x + y for x, y in zip(bottom_right, offset))

        return self.create_rectangle(top_left, bottom_right,
                                     fill=colour, outline=colour)

    def draw_connections(self, connections):
        """
        Draws all the connections between tiles.

        Parameters:
            connections (list<tuple<tuple<int, int>, int, tuple<int, int>>>):
                    A list of all the connections between tiles.
        """
        for connection in connections:
            self._connections.append(self._draw_connection(*connection))

    def get_font_colour(self, position):
        """Based on the colour of the tile at the given position returns either
        black or white depending on which will be easier to see.

        Parameters:
            position (tuple<int, int>): The position of the tile.

        Return:
            (str): The best font colour either black or white.
        """
        colour_name = self.itemconfig(self._tiles[position])['fill'][4]
        colour = self.winfo_rgb(colour_name)
        a = (colour[0] + colour[1] + colour[2]) / (65535 * 3)
        return "white" if a < 0.5 else "black"

    def draw_tile(self, position, cell):
        """Draws a cell at the given position.

        Parameters:
            position (tuple<int, int>): The position of the tile.
            cell (AbstractTile): The tile to draw at the position.
        """
        top_left, middle, bottom_right = self.calculate_bounds(position)

        type = cell.get_type() if cell else 'blank'

        colour = self._colours[type]

        if self._tiles.get(position) is None:
            tile_id = self.create_rectangle(*top_left, *bottom_right,
                                            fill=colour, outline=colour)
            self._tiles[position] = tile_id
        else:
            self.itemconfig(self._tiles[position], fill=colour, outline=colour)

        # label the tiles with their value
        if type != 'blank':
            font_colour = self.get_font_colour(position)
            self._texts.append(self.create_text(*middle,
                                                text=cell.get_display_value(),
                                                fill=font_colour, font=20))

    def draw(self, grid, connections=None):
        """Loop through and draw all the cells contained within the Grid.

        Parameters:
            grid (model.LoloGrid): The LoloGrid to draw.
            connections (list<tuple<tuple<int, int>, int, tuple<int, int>>>):
                    A list of all the connections between tiles.
        """
        # clear all the extra canvas items
        for extra in self._connections + self._texts:
            self.delete(extra)
        # draw all the connections
        if connections is not None:
            self.draw_connections(connections)
        # draw all the tiles
        for position, cell in grid.items():
            self.draw_tile(position, cell)
