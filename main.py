"""
The Controller for Minesweeper
--------------------------------------------------------------------------------
Minesweeper Versions:
- Minesweeper (regular Minesweeper)
- Minesweeper V (tiles see mines in a 5x5 area)
- Distance Minesweeper (tiles see mines everywhere, and their values are equal to the sum of the inverse of their distances from all mines)
- Weighted Minesweeper (tiles see mines everywhere, and their values are equal to the sum of the inverse of their distances from all mines, where left and down are considered negative, and up and right are considered positive)
- Negative Minesweeper (negative mines can appear, which count as -1 mine for surrounding tiles)
"""

import pickle
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
from player_stats_template import starting_player_stats, reset_stats

# game settings
WIDTH = 16
HEIGHT = 16
NUM_MINES = 40
VERSION = "Negative Minesweeper"
DIFFICULTY = "easy"

# dictionary keeping track of player's stats
player_stats = None


def run_game(
    width=16, height=16, num_mines=40, version="Minesweeper", difficulty="medium"
):
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

    version : {"Minesweeper", "Minesweeper V", "Distance Minesweeper", "Weighted Minesweeper", "Negative Minesweeper"}, default: "Minesweeper"
        Which version of Minesweeper to play.

    difficulty : {'easy', 'medium', 'hard'}
        How difficult the game should be (ONLY affects certain gamemodes, such as Distance Minesweeper)
    """

    # create the board object based on which Minesweeper mode was selected
    minesweeper_board = None
    match version:
        case "Minesweeper":
            minesweeper_board = MinesweeperBoard(width, height, num_mines)
        case "Minesweeper V":
            minesweeper_board = MinesweeperVBoard(width, height, num_mines)
        case "Distance Minesweeper":
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
        case "Weighted Minesweeper":
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
        case "Negative Minesweeper":
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

            # if the clicked tile was a mine, the game is lost
            if (
                activated_tile.type == Tile.MINE
                or activated_tile.type == Tile.NEGATIVE_MINE
            ):
                minesweeper_board.reveal_all_tiles()
                game_running = False

            # if the board has been completed, the game is won
            if minesweeper_board.board_finished():
                print(
                    "YOU WON!!!"
                )  # TODO Have a status message in a UI section next to the game board display this
                player_stats[""]

        # if the clicked button was right, plant a flag on the clicked tile
        elif mouse_button == "right":
            minesweeper_board.plant_flag_on_tile(clicked_tile[0], clicked_tile[1])

        # redraw the board
        update_tile_board(tile_board, minesweeper_board)
        update_value_board(value_board, tile_board, minesweeper_board)

    win.getMouse()


if __name__ == "__main__":
    # load the player's stats, or create a new stats file if there isn't one already
    try:
        with open("stats", "rb") as stats_file:
            player_stats = pickle.load(stats_file)
    except FileNotFoundError:
        reset_stats()
        player_stats = starting_player_stats

    while True:
        run_game(WIDTH, HEIGHT, NUM_MINES, VERSION, DIFFICULTY)
