import random
import math
from Minesweeper.MinesweeperBoard import Tile, MinesweeperTile, MinesweeperBoard


class DistanceMinesweeperBoard(MinesweeperBoard):
    """
    A board containing many tiles on which a game of Distance Minesweeper is played.

    Attributes
    ----------
    width : int, default: 16
        The number of tiles wide the board is.

    height : int, default: 16
        The number of tiles high the board is.

    num_mines : int, default: 20
        The number of mines hidden in the board.

    board : list, default: None
        A 2D array of tiles representing the current board state.

    distance_weight : int, default: 1
        What the distance is squared by when calculating the inverse (higher means smaller numbers means easier)
    """

    def __init__(
        self, width=16, height=16, num_mines=20, board=None, distance_weight=1
    ):
        super().__init__(width, height, num_mines, board)
        self.distance_weight = distance_weight

    def get_random_board(self, first_click_coords=(-1, -1)) -> list:
        """
        Create and return a random board of size `self.width` and `self.height` with `self.num_mines` hidden in it.
        Tile values are created according to Distance Minesweeper rules.

        Parameters
        ----------
        first_click_coords : tuple, optional
            The coordinates of the first tile clicked to rig the first click to be an empty tile, no rigging if left empty.

        Returns
        -------
        list
            2D array representing the randomly generated board
        """

        # create a base board of size width x height (all tiles that aren't mines are numbered in this version)
        board = [
            [MinesweeperTile(type=Tile.NUMBERED) for _ in range(self.board_width)]
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
        for mine_location in mine_locations:
            board[mine_location[0]][mine_location[1]] = MinesweeperTile(Tile.MINE)

            # increase the value of every tile on the board by the inverse of its distance from the mine
            for row in range(len(board)):
                for col in range(len(board[row])):
                    if (
                        0 <= row < self.board_height
                        and 0 <= col < self.board_width
                        and board[row][col].type != Tile.MINE
                    ):

                        # distance formula
                        board[row][col].value += (
                            1
                            / (
                                math.sqrt(
                                    math.pow(mine_location[0] - row, 2)
                                    + math.pow(mine_location[1] - col, 2)
                                )
                            )
                            ** self.distance_weight
                        )

        return board

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

            # if planting a flag, decrease all tiles by their inverse distance from the flag
            change_factor = -1

            # if removing a flag, increase all tiles by their inverse distance from the flag
            if self.board[row][col].flag_planted:
                change_factor = 1

            self.board[row][col].flag_planted = (
                self.board[row][col].flag_planted + 1
            ) % 2
            self.board[row][col].changed_last_move = True

            # change every numbered tile by the inverse of their distance from the flag
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    if (
                        0 <= r < self.board_height
                        and 0 <= c < self.board_width
                        and self.board[r][c].type == Tile.NUMBERED
                        and not (r == row and c == col)
                    ):
                        self.board[r][c].value += (
                            1
                            / (math.sqrt(math.pow(row - r, 2) + math.pow(col - c, 2)))
                            ** self.distance_weight
                            * change_factor
                        )
                        self.board[r][c].changed_last_move = True
