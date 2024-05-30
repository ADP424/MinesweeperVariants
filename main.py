"""
The Controller for Minesweeper
--------------------------------------------------------------------------------
Minesweeper Versions:
0 - Regular Minesweeper
1 - Minesweeper V (tiles see mines in a 5x5 area)
2 - Distance Minesweeper (tiles see mines everywhere, and their values are equal to the sum of the inverse of their distances from all mines)
3 - Weighted Minesweeper (tiles see mines everywhere, and their values are equal to the sum of the inverse of their distances from all mines, where left and down are considered negative, and up and right are considered positive)
4 - Negative Minesweeper (negative mines can appear, which count as -1 mine for surrounding tiles)
"""

from Minesweeper.MinesweeperBoard import Tile, MinesweeperBoard
from Minesweeper.MinesweeperVBoard import MinesweeperVBoard
from Minesweeper.DistanceMinesweeperBoard import DistanceMinesweeperBoard
from Minesweeper.WeightedMinesweeperBoard import WeightedMinesweeperBoard
from Minesweeper.NegativeMinesweeperBoard import NegativeMinesweeperBoard
from GUI import (
    win,
    create_tile_board,
    create_value_board,
    draw_tile_board,
    draw_value_board,
    get_clicked_tile_coords,
    update_tile_board,
    update_value_board,
)

# game settings
WIDTH = 16
HEIGHT = 16
NUM_MINES = 40
VERSION = 4
DIFFICULTY = "easy"


def run_game(width=16, height=16, num_mines=40, version=0, difficulty="medium"):
    """
    Create and run a minesweeper game with the specified settings.

    Parameters
    ----------
    width : int, default: 16
        The number of tiles wide the minesweeper board is.

    height : int, default: 16
        The number of tiles high the minesweeper board is.

    num_mines : int, default: 40
        The number of mines to hide in the board.

    version : int, default: 0
        Which set of rules to play with.

    difficulty : {'easy', 'medium', 'hard'}
        How difficult the game should be (ONLY affects certain gamemodes, such as Distance Minesweeper)
    """

    # create the board object based on which Minesweeper mode was selected
    minesweeper_board = None
    match version:
        case 0:
            minesweeper_board = MinesweeperBoard(width, height, num_mines)
        case 1:
            minesweeper_board = MinesweeperVBoard(width, height, num_mines)
        case 2:
            match difficulty:
                case "easy":
                    minesweeper_board = DistanceMinesweeperBoard(
                        width, height, num_mines, distance_weight=3
                    )
                case "medium":
                    minesweeper_board = DistanceMinesweeperBoard(
                        width, height, num_mines, distance_weight=2
                    )
                case "hard":
                    minesweeper_board = DistanceMinesweeperBoard(
                        width, height, num_mines, distance_weight=1
                    )
                case _:
                    raise Exception("Invalid difficulty setting")
        case 3:
            match difficulty:
                case "easy":
                    minesweeper_board = WeightedMinesweeperBoard(
                        width, height, num_mines, distance_weight=3
                    )
                case "medium":
                    minesweeper_board = WeightedMinesweeperBoard(
                        width, height, num_mines, distance_weight=2
                    )
                case "hard":
                    minesweeper_board = WeightedMinesweeperBoard(
                        width, height, num_mines, distance_weight=1
                    )
                case _:
                    raise Exception("Invalid difficulty setting")
        case 4:
            match difficulty:
                case "easy":
                    minesweeper_board = NegativeMinesweeperBoard(
                        width, height, num_mines - (num_mines // 4), num_mines // 4
                    )
                case "medium":
                    minesweeper_board = NegativeMinesweeperBoard(
                        width, height, num_mines - (num_mines // 3), num_mines // 3
                    )
                case "hard":
                    minesweeper_board = NegativeMinesweeperBoard(
                        width, height, num_mines - (num_mines // 2), num_mines // 2
                    )
                case _:
                    raise Exception("Invalid difficulty setting")
        case _:
            raise Exception("Invalid Minesweeper Version")

    # create the initial boardstate and draw it into the window
    tile_board = create_tile_board(minesweeper_board)
    value_board = create_value_board(tile_board, minesweeper_board)
    draw_tile_board(tile_board)
    draw_value_board(value_board)

    # get the first left click the user makes in order to rig the first tile to always be empty
    mouse_button = ""
    while mouse_button != "left":

        # get tile the user clicked
        clicked_point, mouse_button = win.getMouse()
        clicked_tile = get_clicked_tile_coords(clicked_point, minesweeper_board)

        # if the clicked button was left, make a move on the clicked tile (if that tile doesn't have a flag)
        if mouse_button == "left":

            # create a random board where the first clicked tile is guaranteed to be empty
            minesweeper_board.board = minesweeper_board.get_random_board(clicked_tile)
            minesweeper_board.make_move(clicked_tile[0], clicked_tile[1])

        # if the clicked button was right, plant a flag on the clicked tile
        elif mouse_button == "right":
            minesweeper_board.plant_flag_on_tile(clicked_tile[0], clicked_tile[1])

        # redraw the board
        update_tile_board(tile_board, minesweeper_board)
        update_value_board(value_board, tile_board, minesweeper_board)

    # loop until the game is over
    game_running = True
    while game_running:

        # get the tile the user clicked
        clicked_point, mouse_button = win.getMouse()
        clicked_tile = get_clicked_tile_coords(clicked_point, minesweeper_board)

        # if the clicked button was left, make a move on the clicked tile
        if mouse_button == "left":
            activated_tile = minesweeper_board.make_move(
                clicked_tile[0], clicked_tile[1]
            )

            # if the clicked tile was a mine, end the game
            if (
                activated_tile.type == Tile.MINE
                or activated_tile.type == Tile.NEGATIVE_MINE
            ):
                minesweeper_board.reveal_all_tiles()
                game_running = False

        # if the clicked button was right, plant a flag on the clicked tile
        elif mouse_button == "right":
            minesweeper_board.plant_flag_on_tile(clicked_tile[0], clicked_tile[1])

        # redraw the board
        update_tile_board(tile_board, minesweeper_board)
        update_value_board(value_board, tile_board, minesweeper_board)

    win.getMouse()


while True:
    run_game(WIDTH, HEIGHT, NUM_MINES, VERSION, DIFFICULTY)
