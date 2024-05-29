from enum import Enum
import random
import sys


class Tile(Enum):
    NULL = -1  # out of bounds
    EMPTY = 0
    MINE = 1
    NUMBERED = 2
    NEGATIVE_MINE = 3 # not used by regular Minesweeper


class MinesweeperTile:
    """
    A single tile on the board, either hidden or unhidden.

    Attributes
    ----------
    type : Tile, default: Tile.EMPTY
        The type of tile the tile is (empty, mine, numbered, etc.).

    value : float, default: 0
        A float or integer representing the number of mines surrounding the tile (if the tile is itself a mine, value is -1).

    revealed : bool, default: False
        Whether the tile's value is visible to the player or not.

    flag_planted : int, default: 0
        Which flag, if any, is planted on the tile.
        0: No Flag
        1: Positive Flag
        2: Negative Flag

    changed_last_move : bool, default: False
        Whether the tile was updated by the last move or not.
    """

    def __init__(
        self,
        type=Tile.EMPTY,
        value=0,
        revealed=False,
        flag_planted=0,
        changed_last_move=False,
    ):
        self.type = type
        self.value = value
        self.revealed = revealed
        self.flag_planted = flag_planted
        self.changed_last_move = changed_last_move

        # set the recursion limit way up for my silly reveal tile function
        sys.setrecursionlimit(100000)


class MinesweeperBoard:
    """
    A board containing many tiles on which a regular game of Minesweeper is played.

    Attributes
    ----------
    width : int, default: 16
        The number of tiles wide the board is.

    height : int, default: 16
        The number of tiles high the board is.

    num_mines : int, default: 40
        The number of mines hidden in the board.

    board : list, default: 2D array of blank tiles of size height x width
        A 2D array of tiles representing the current board state.
    """

    def __init__(self, width=16, height=16, num_mines=40, board=None):
        self.board_width = width
        self.board_height = height
        self.num_mines = num_mines
        self.board = [
            [MinesweeperTile() for _ in range(self.board_width)]
            for _ in range(self.board_height)
        ]

    def get_random_board(self, first_click_coords=(-1, -1)) -> list:
        """
        Create and return a random board of size `self.width` and `self.height` with `self.num_mines` hidden in it.
        Tile values are created according to regular Minesweeper rules.

        Parameters
        ----------
        first_click_coords : tuple, optional
            The coordinates of the first tile clicked to rig the first click to be an empty tile, no rigging if left empty.

        Returns
        -------
        list
            2D array representing the randomly generated board
        """

        # create a base board of size width x height
        board = [
            [MinesweeperTile() for _ in range(self.board_width)]
            for _ in range(self.board_height)
        ]

        # create a list of tiles surrounding and including the first click
        first_click_tiles = [
            first_click_coords,
            (first_click_coords[0] - 1, first_click_coords[1] - 1),
            (first_click_coords[0] - 1, first_click_coords[1]),
            (first_click_coords[0] - 1, first_click_coords[1] + 1),
            (first_click_coords[0], first_click_coords[1] - 1),
            (first_click_coords[0], first_click_coords[1] + 1),
            (first_click_coords[0] + 1, first_click_coords[1] - 1),
            (first_click_coords[0] + 1, first_click_coords[1]),
            (first_click_coords[0] + 1, first_click_coords[1] + 1),
        ]

        # create a list of tuples representing every possible (row, col) pair
        tile_locations = []
        for row in range(self.board_height):
            for col in range(self.board_width):

                # if the coordinate pair is the first click or next to the first click, don't let it get a mine
                if first_click_coords[0] < 0 or (row, col) not in first_click_tiles:
                    tile_locations.append((row, col))

        # take a random sample of locations to put mines on
        mine_locations = random.sample(tile_locations, self.num_mines)

        # hide the mines in the board
        count = 0
        for mine_location in mine_locations:
            board[mine_location[0]][mine_location[1]] = MinesweeperTile(Tile.MINE)

            surrounding_tiles = [
                (mine_location[0] - 1, mine_location[1] - 1),
                (mine_location[0] - 1, mine_location[1]),
                (mine_location[0] - 1, mine_location[1] + 1),
                (mine_location[0], mine_location[1] - 1),
                (mine_location[0], mine_location[1] + 1),
                (mine_location[0] + 1, mine_location[1] - 1),
                (mine_location[0] + 1, mine_location[1]),
                (mine_location[0] + 1, mine_location[1] + 1),
            ]

            # increase the value of each surrounding non-mine tile by 1
            for tile in surrounding_tiles:
                if (
                    0 <= tile[0] < self.board_height
                    and 0 <= tile[1] < self.board_width
                    and board[tile[0]][tile[1]].type != Tile.MINE
                ):
                    board[tile[0]][tile[1]].value += 1

                    # change the tile's type to 'numbered' now that it has been assigned a number
                    board[tile[0]][tile[1]].type = Tile.NUMBERED

        return board

    def make_move(self, row, col) -> MinesweeperTile:
        """
        Make a move on the board at the given row and column, if there isn't a flag planted there.

        Parameters
        ----------
        row : int
            The row of the tile to move on.
        col : int
            The column of the tile to move on.

        Returns
        -------
        MinesweeperTile
            The MinesweeperTile that was moved on
        """

        if (
            0 <= row < self.board_height
            and 0 <= col < self.board_width
            and not self.board[row][col].flag_planted
        ):
            self.reset_changed_last_move_board()
            self._reveal_tile(row, col)
            return self.board[row][col]
        return MinesweeperTile(Tile.NULL)

    def _reveal_tile(self, row, col):
        """
        Reveal the tile at the given row and column.

        Parameters
        ----------
        row : int
            The row of the tile to reveal.
        col : int
            The column of the tile to reveal.
        """

        if not self.board[row][col].revealed:
            self.board[row][col].revealed = True
            self.board[row][col].flag_planted = 0
            self.board[row][col].changed_last_move = True

            # if the tile is empty, recursively reveal all adjacent, non-mine tiles
            if self.board[row][col].type == Tile.EMPTY:
                surrounding_tiles = [
                    (row - 1, col - 1),
                    (row - 1, col),
                    (row - 1, col + 1),
                    (row, col - 1),
                    (row, col + 1),
                    (row + 1, col - 1),
                    (row + 1, col),
                    (row + 1, col + 1),
                ]

                for tile in surrounding_tiles:
                    if (
                        0 <= tile[0] < self.board_height
                        and 0 <= tile[1] < self.board_width
                        and self.board[tile[0]][tile[1]].type != Tile.MINE
                    ):
                        self._reveal_tile(tile[0], tile[1])

    def plant_flag_on_tile(self, row, col):
        """
        Plant or unplant a flag on the tile at the given row and column if it is not revealed.

        Parameters
        ----------
        row : int
            The row of the tile to plant on.
        col : int
            The column of the tile to plant on.
        """

        self.reset_changed_last_move_board()
        if not self.board[row][col].revealed:

            # if planting a flag, decrease all surrounding tiles by 1
            change_value = -1

            # if removing a flag, increase all surrounding tiles by 1
            if self.board[row][col].flag_planted:
                change_value = 1

            surrounding_tiles = [
                (row - 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row, col - 1),
                (row, col + 1),
                (row + 1, col - 1),
                (row + 1, col),
                (row + 1, col + 1),
            ]

            self.board[row][col].flag_planted = (self.board[row][col].flag_planted + 1) % 2
            self.board[row][col].changed_last_move = True

            # change every numbered surrounding tile by the change value
            for tile in surrounding_tiles:
                if (
                    0 <= tile[0] < self.board_height
                    and 0 <= tile[1] < self.board_width
                    and self.board[tile[0]][tile[1]].type == Tile.NUMBERED
                ):
                    self.board[tile[0]][tile[1]].value += change_value
                    self.board[tile[0]][tile[1]].changed_last_move = True

    def reset_changed_last_move_board(self):
        """
        Reset every tile's `changed_last_move` indicator to False in `self.board`.
        """

        for row in self.board:
            for tile in row:
                tile.changed_last_move = False

    def reveal_all_tiles(self):
        """
        Set every tile to revealed.
        """

        for row in self.board:
            for tile in row:
                if not tile.revealed:
                    tile.changed_last_move = True
                tile.revealed = True

    def print_board(self):
        """
        Print a string representation of the board to the terminal.
        """

        for row in self.board:
            for tile in row:
                if not tile.revealed:
                    print("#", end=" ")
                else:
                    if tile.value == 0:
                        print(".", end=" ")
                    elif tile.value == -1:
                        print("B", end=" ")
                    else:
                        print(tile.value, end=" ")
            print()
        print()

    def print_board_revealed(self):
        """
        Print a string representation of the board with all tiles revealed to the terminal.
        """

        for row in self.board:
            for tile in row:
                if tile.value == 0:
                    print(".", end=" ")
                elif tile.value == -1:
                    print("B", end=" ")
                else:
                    print(tile.value, end=" ")
            print()
        print()

    def print_board_changed_last_move(self):
        """
        Print a grid representing whether each tile was updated last move or not to the terminal.
        """

        for row in self.board:
            for tile in row:
                if tile.changed_last_move:
                    print("T", end=" ")
                else:
                    print("F", end=" ")
            print()
        print()
