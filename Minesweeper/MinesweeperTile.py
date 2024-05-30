import sys
from enum import Enum


class Tile(Enum):
    NULL = -1  # out of bounds
    EMPTY = 0
    MINE = 1
    NUMBERED = 2
    NEGATIVE_MINE = 3  # not used by regular Minesweeper


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
