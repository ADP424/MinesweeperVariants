import random
from Minesweeper.MinesweeperBoard import Tile, MinesweeperTile, MinesweeperBoard


class MinesweeperVBoard(MinesweeperBoard):
    """
    A board containing many tiles on which a game of Minesweeper V is played.

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
    """

    def __init__(self, width=16, height=16, num_mines=20, board=None):
        super().__init__(width, height, num_mines, board)

    def get_random_board(self, first_click_coords=(-1, -1)) -> list:
        """
        Create and return a random board of size `self.width` and `self.height` with `self.num_mines` hidden in it.
        Tile values are created according to Minesweeper V rules.

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
            (first_click_coords[0] - 2, first_click_coords[1] - 2),
            (first_click_coords[0] - 2, first_click_coords[1] - 1),
            (first_click_coords[0] - 2, first_click_coords[1]),
            (first_click_coords[0] - 2, first_click_coords[1] + 1),
            (first_click_coords[0] - 2, first_click_coords[1] + 2),
            (first_click_coords[0] - 1, first_click_coords[1] - 2),
            (first_click_coords[0] - 1, first_click_coords[1] - 1),
            (first_click_coords[0] - 1, first_click_coords[1]),
            (first_click_coords[0] - 1, first_click_coords[1] + 1),
            (first_click_coords[0] - 1, first_click_coords[1] + 2),
            (first_click_coords[0], first_click_coords[1] - 2),
            (first_click_coords[0], first_click_coords[1] - 1),
            (first_click_coords[0], first_click_coords[1] + 1),
            (first_click_coords[0], first_click_coords[1] + 2),
            (first_click_coords[0] + 1, first_click_coords[1] - 2),
            (first_click_coords[0] + 1, first_click_coords[1] - 1),
            (first_click_coords[0] + 1, first_click_coords[1]),
            (first_click_coords[0] + 1, first_click_coords[1] + 1),
            (first_click_coords[0] + 1, first_click_coords[1] + 2),
            (first_click_coords[0] + 2, first_click_coords[1] - 2),
            (first_click_coords[0] + 2, first_click_coords[1] - 1),
            (first_click_coords[0] + 2, first_click_coords[1]),
            (first_click_coords[0] + 2, first_click_coords[1] + 1),
            (first_click_coords[0] + 2, first_click_coords[1] + 2),
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

            surrounding_tiles = [
                (mine_location[0] - 2, mine_location[1] - 2),
                (mine_location[0] - 2, mine_location[1] - 1),
                (mine_location[0] - 2, mine_location[1]),
                (mine_location[0] - 2, mine_location[1] + 1),
                (mine_location[0] - 2, mine_location[1] + 2),
                (mine_location[0] - 1, mine_location[1] - 2),
                (mine_location[0] - 1, mine_location[1] - 1),
                (mine_location[0] - 1, mine_location[1]),
                (mine_location[0] - 1, mine_location[1] + 1),
                (mine_location[0] - 1, mine_location[1] + 2),
                (mine_location[0], mine_location[1] - 2),
                (mine_location[0], mine_location[1] - 1),
                (mine_location[0], mine_location[1] + 1),
                (mine_location[0], mine_location[1] + 2),
                (mine_location[0] + 1, mine_location[1] - 2),
                (mine_location[0] + 1, mine_location[1] - 1),
                (mine_location[0] + 1, mine_location[1]),
                (mine_location[0] + 1, mine_location[1] + 1),
                (mine_location[0] + 1, mine_location[1] + 2),
                (mine_location[0] + 2, mine_location[1] - 2),
                (mine_location[0] + 2, mine_location[1] - 1),
                (mine_location[0] + 2, mine_location[1]),
                (mine_location[0] + 2, mine_location[1] + 1),
                (mine_location[0] + 2, mine_location[1] + 2),
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
            self.board[row][col].flag_planted = False
            self.board[row][col].changed_last_move = True

            # if the tile is empty, recursively reveal all adjacent, non-mine tiles
            if self.board[row][col].type == Tile.EMPTY:
                surrounding_tiles = [
                    (row - 2, col - 2),
                    (row - 2, col - 1),
                    (row - 2, col),
                    (row - 2, col + 1),
                    (row - 2, col + 2),
                    (row - 1, col - 2),
                    (row - 1, col - 1),
                    (row - 1, col),
                    (row - 1, col + 1),
                    (row - 1, col + 2),
                    (row, col - 2),
                    (row, col - 1),
                    (row, col + 1),
                    (row, col + 2),
                    (row + 1, col - 2),
                    (row + 1, col - 1),
                    (row + 1, col),
                    (row + 1, col + 1),
                    (row + 1, col + 2),
                    (row + 2, col - 2),
                    (row + 2, col - 1),
                    (row + 2, col),
                    (row + 2, col + 1),
                    (row + 2, col + 2),
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
                (row - 2, col - 2),
                (row - 2, col - 1),
                (row - 2, col),
                (row - 2, col + 1),
                (row - 2, col + 2),
                (row - 1, col - 2),
                (row - 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row - 1, col + 2),
                (row, col - 2),
                (row, col - 1),
                (row, col + 1),
                (row, col + 2),
                (row + 1, col - 2),
                (row + 1, col - 1),
                (row + 1, col),
                (row + 1, col + 1),
                (row + 1, col + 2),
                (row + 2, col - 2),
                (row + 2, col - 1),
                (row + 2, col),
                (row + 2, col + 1),
                (row + 2, col + 2),
            ]

            self.board[row][col].flag_planted = not self.board[row][col].flag_planted
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
