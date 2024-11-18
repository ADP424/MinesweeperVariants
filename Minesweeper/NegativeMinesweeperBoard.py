import random
from Minesweeper.MinesweeperBoard import Tile, MinesweeperTile, MinesweeperBoard
from PlayerStats import PlayerStats


class NegativeMinesweeperBoard(MinesweeperBoard):
    """
    A board containing many tiles on which a game of Negative Minesweeper is played.

    Attributes
    ----------
    minesweeper_version: str, default: "Negative Minesweeper"
        The name of the Minesweeper version being played on this board.

    width : int, default: 16
        The number of tiles wide the board is.

    height : int, default: 16
        The number of tiles high the board is.

    num_positive_mines : int, default: 20
        The number of regular mines hidden in the board.

    num_negative_mines : int, default: 20
        The number of negative mines hidden in the board.

    board : list, default: 2D array of blank tiles of size height x width
        A 2D array of tiles representing the current board state.

    stats : PlayerStats, optional
        Stats to update throughout the game whenever a relevant action happens.
    """

    def __init__(
        self,
        minesweeper_version="Negative Minesweeper",
        width=16,
        height=16,
        num_positive_mines=20,
        num_negative_mines=20,
        board: list[list[MinesweeperTile]] = None,
        stats: PlayerStats = None,
    ):
        super().__init__(minesweeper_version, width, height, num_positive_mines + num_negative_mines, board, stats)
        self.num_positive_mines = num_positive_mines
        self.num_negative_mines = num_negative_mines

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
        board = [[MinesweeperTile() for _ in range(self.board_width)] for _ in range(self.board_height)]

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
        positive_count = 0
        for mine_location in mine_locations:
            if positive_count < self.num_positive_mines:
                board[mine_location[0]][mine_location[1]] = MinesweeperTile(Tile.MINE)
                positive_count += 1
            else:
                board[mine_location[0]][mine_location[1]] = MinesweeperTile(Tile.NEGATIVE_MINE)

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

            # increase (or decrease if mine is negative) the value of each surrounding non-mine tile by 1
            for tile in surrounding_tiles:
                if (
                    0 <= tile[0] < self.board_height
                    and 0 <= tile[1] < self.board_width
                    and board[tile[0]][tile[1]].type != Tile.MINE
                    and board[tile[0]][tile[1]].type != Tile.NEGATIVE_MINE
                ):
                    if positive_count < self.num_positive_mines:
                        board[tile[0]][tile[1]].value += 1
                    else:
                        board[tile[0]][tile[1]].value -= 1

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
            self.stats.increment_stat(self.minesweeper_version, "Tiles Revealed")
            self.board[row][col].revealed = True
            self.board[row][col].flag_planted = False
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
                        and self.board[tile[0]][tile[1]].type != Tile.NEGATIVE_MINE
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

            # if planting a flag or removing a negative flag, decrease all surrounding tiles by 1
            if self.board[row][col].flag_planted != 1:
                change_value = -1

            # if replacing a positive flag with a negative one, increase all surrounding tiles by 2
            else:
                change_value = 2

            # TODO: this is ridiculous lol
            if self.board[row][col].type == Tile.MINE:
                if self.board[row][col].flag_planted == 0:
                    self.stats.increment_stat(self.minesweeper_version, "Positive Mines Defused")
                elif self.board[row][col].flag_planted == 1:
                    self.stats.increment_stat(self.minesweeper_version, "Positive Mines Defused", -1)
                    self.stats.increment_stat(self.minesweeper_version, "Flag Mistakes")
                else:
                    self.stats.increment_stat(self.minesweeper_version, "Flag Mistakes", -1)
            elif self.board[row][col].type == Tile.NEGATIVE_MINE:
                if self.board[row][col].flag_planted == 0:
                    self.stats.increment_stat(self.minesweeper_version, "Flag Mistakes", -1)
                elif self.board[row][col].flag_planted == 1:
                    self.stats.increment_stat(self.minesweeper_version, "Negative Mines Defused")
                else:
                    self.stats.increment_stat(self.minesweeper_version, "Negative Mines Defused", -1)
                    self.stats.increment_stat(self.minesweeper_version, "Flag Mistakes")
            else:
                if self.board[row][col].flag_planted == 0:
                    self.stats.increment_stat(self.minesweeper_version, "Flag Mistakes")
                elif self.board[row][col].flag_planted == 2:
                    self.stats.increment_stat(self.minesweeper_version, "Flag Mistakes", -1)

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

            self.board[row][col].flag_planted = (self.board[row][col].flag_planted + 1) % 3
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

    def board_finished(self) -> bool:
        """
        Check if the board has been fully revealed/flagged correctly

        Returns
        -------
        bool
            Whether the board has been completed or not
        """

        for row in self.board:
            for tile in row:

                # if the tile hasn't been revealed and isn't a correctly flagged mine, the board isn't complete
                if not tile.revealed and (
                    tile.flag_planted == 0
                    or (tile.flag_planted == 1 and tile.type != Tile.MINE)
                    or (tile.flag_planted == 2 and tile.type != Tile.NEGATIVE_MINE)
                ):
                    return False
        return True
