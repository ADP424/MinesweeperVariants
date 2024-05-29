"""
The GUI/Controller for Minesweeper
--------------------------------------------------------------------------------
Minesweeper Versions:
0 - Regular Minesweeper
1 - Minesweeper V (tiles see mines in a 5x5 area)
2 - Distance Minesweeper (tiles see mines everywhere, and their values are equal to the sum of the inverse of their distances from all mines)
3 - Weighted Minesweeper (tiles see mines everywhere, and their values are equal to the sum of the inverse of their distances from all mines, where left and down are considered negative, and up and right are considered positive)
4 - Negative Minesweeper (negative mines can appear, which count as -1 mine for surrounding tiles)
"""

from graphics import color_rgb
from graphics import Rectangle, GraphWin, Point, Image
from Minesweeper.MinesweeperBoard import Tile, MinesweeperBoard
from Minesweeper.MinesweeperVBoard import MinesweeperVBoard
from Minesweeper.DistanceMinesweeperBoard import DistanceMinesweeperBoard
from Minesweeper.WeightedMinesweeperBoard import WeightedMinesweeperBoard
from Minesweeper.NegativeMinesweeperBoard import NegativeMinesweeperBoard

# the height and width of the window to draw onto
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# the combined border size around the minesweeper board
# (ex. a border size of 100 means 50px borders above, below, left, and right of the board)
WINDOW_BORDERS = 25

# colors
EVEN_TILE_COLOR = color_rgb(250, 240, 230)
ODD_TILE_COLOR = color_rgb(238, 217, 196)
REVEALED_TILE_COLOR = color_rgb(204, 204, 204)
BACKGROUND_COLOR = color_rgb(100, 100, 100)

# create the chess window and make the background grey
win = GraphWin("Minesweeper", WINDOW_WIDTH, WINDOW_HEIGHT, False)
win.setBackground(BACKGROUND_COLOR)


def create_tile_board(minesweeper_board: MinesweeperBoard) -> list:
    """
    Create a board of square tiles for drawing onto the window based on the given minesweeper board.

    Parameters
    ----------
    minesweeper_board : MinesweeperBoard
        The minesweeper board to draw.

    Returns
    -------
    list
        The 2D array of tiles.
    """

    tile_size = min(
        (WINDOW_HEIGHT - WINDOW_BORDERS) / minesweeper_board.board_height,
        (WINDOW_WIDTH - WINDOW_BORDERS) / minesweeper_board.board_width,
    )

    # create a 2D array of buttons representing tiles on the chess board
    button_board = []
    is_dark_tile = False
    y_coord = (WINDOW_HEIGHT - tile_size * minesweeper_board.board_height) / 2

    for i in range(minesweeper_board.board_height):
        x_coord = (WINDOW_WIDTH - tile_size * minesweeper_board.board_width) / 2
        button_board.append([])

        for j in range(minesweeper_board.board_width):
            button_board[i].append(
                Rectangle(
                    Point(x_coord, y_coord + tile_size),
                    Point(x_coord + tile_size, y_coord),
                )
            )

            if minesweeper_board.board[i][j].revealed:
                button_board[i][j].setFill(REVEALED_TILE_COLOR)
            elif is_dark_tile:
                button_board[i][j].setFill(ODD_TILE_COLOR)
            else:
                button_board[i][j].setFill(EVEN_TILE_COLOR)
            is_dark_tile = not is_dark_tile

            x_coord += tile_size
        y_coord += tile_size
        is_dark_tile = not is_dark_tile

    return button_board


def get_value_images(
    row: int,
    col: int,
    tile_size: float,
    tile_board: list,
    minesweeper_board: MinesweeperBoard,
):
    """
    Get the image(s) corresponding to the tile value at the given row and column.

    Parameters
    ----------
    row : int
        The row where the value is located.

    col : int
        The column where the value is located.

    tile_size : float
        The size of the tile on the window that the value will be drawn on.

    tile_board : list
        The 2D array of squares representing the tiles on the minesweeper board.

    minesweeper_board : MinesweeperBoard
        The minesweeper board to draw the values from.

    Returns
    -------
    Image
        The value image corresponding to the tile value at the given row and column.
    """

    # if the tile is not revealed, check if there is a flag planted on it
    if not minesweeper_board.board[row][col].revealed:

        # if a positive flag is planted, draw it
        if minesweeper_board.board[row][col].flag_planted == 1:
            return [
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    "images/flag.png",
                    int(tile_size / 2),
                    int(tile_size / 2),
                )
            ]

        elif minesweeper_board.board[row][col].flag_planted == 2:
            return [
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    "images/negative_flag.png",
                    int(tile_size / 2),
                    int(tile_size / 2),
                )
            ]

        # else, draw nothing
        else:
            return [
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    "images/empty.png",
                    int(tile_size / 2),
                    int(tile_size / 2),
                )
            ]

    # if the tile is empty, draw nothing
    if minesweeper_board.board[row][col].type == Tile.EMPTY:
        return [
            Image(
                Point(
                    (
                        tile_board[row][col].getP1().getX()
                        + tile_board[row][col].getP2().getX()
                    )
                    / 2,
                    (
                        tile_board[row][col].getP1().getY()
                        + tile_board[row][col].getP2().getY()
                    )
                    / 2,
                ),
                "images/empty.png",
                int(tile_size / 2),
                int(tile_size / 2),
            )
        ]

    # if the tile is a mine, draw a mine
    if minesweeper_board.board[row][col].type == Tile.MINE:
        return [
            Image(
                Point(
                    (
                        tile_board[row][col].getP1().getX()
                        + tile_board[row][col].getP2().getX()
                    )
                    / 2,
                    (
                        tile_board[row][col].getP1().getY()
                        + tile_board[row][col].getP2().getY()
                    )
                    / 2,
                ),
                "images/bomb.png",
                int(tile_size / 2),
                int(tile_size / 2),
            )
        ]

    # if the tile is a negative mine, draw a negative mine
    if minesweeper_board.board[row][col].type == Tile.NEGATIVE_MINE:
        return [
            Image(
                Point(
                    (
                        tile_board[row][col].getP1().getX()
                        + tile_board[row][col].getP2().getX()
                    )
                    / 2,
                    (
                        tile_board[row][col].getP1().getY()
                        + tile_board[row][col].getP2().getY()
                    )
                    / 2,
                ),
                "images/negative_bomb.png",
                int(tile_size / 2),
                int(tile_size / 2),
            )
        ]

    # if the tile's value is an integer, draw that number
    if isinstance(minesweeper_board.board[row][col].value, int):

        # if it's positive, just draw the number
        if minesweeper_board.board[row][col].value >= 0:
            image_name = (
                "images/" + str(minesweeper_board.board[row][col].value) + ".png"
            )
            return [
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    image_name,
                    int(tile_size / 2),
                    int(tile_size / 2),
                )
            ]

        # if it's negative, draw a minus sign before the number
        else:
            images = []

            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2
                        - tile_size / 4,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    "images/minus.png",
                    int(tile_size / 6),
                    int(tile_size / 3),
                )
            )

            image_name = (
                "images/" + str(abs(minesweeper_board.board[row][col].value)) + ".png"
            )
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2
                        + tile_size / 8,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    image_name,
                    int(tile_size / 3),
                    int(tile_size / 2),
                )
            )

    # else, we can assume the value is a float and draw it to one decimal place
    else:
        images = []

        # if it's positive, just draw the decimal
        if minesweeper_board.board[row][col].value > 0:
            value_string = str(round(minesweeper_board.board[row][col].value, 3)).split(
                "."
            )

            # add the value before the decimal
            image_name = "images/" + str(value_string[0]) + ".png"
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2
                        - tile_size / 4,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    image_name,
                    int(tile_size / 4),
                    int(tile_size / 2),
                )
            )

            # add the decimal point
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2
                        + tile_size / 6,
                    ),
                    "images/dot.png",
                    int(tile_size / 6),
                    int(tile_size / 6),
                )
            )

            # add the value after the decimal
            image_name = "images/" + str(value_string[1][0]) + ".png"
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2
                        + tile_size / 4,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    image_name,
                    int(tile_size / 4),
                    int(tile_size / 2),
                )
            )

        # if it's negative, draw a minus sign before the decimal
        else:
            value_string = str(round(minesweeper_board.board[row][col].value, 3))[
                1:
            ].split(".")

            # add the value before the decimal
            image_name = "images/" + str(value_string[0]) + ".png"
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2
                        - tile_size / 4,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    image_name,
                    int(tile_size / 4),
                    int(tile_size / 2),
                )
            )

            # add the decimal point
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2
                        + tile_size / 6,
                    ),
                    "images/dot.png",
                    int(tile_size / 6),
                    int(tile_size / 6),
                )
            )

            # add the value after the decimal
            image_name = "images/" + str(value_string[1][0]) + ".png"
            images.append(
                Image(
                    Point(
                        (
                            tile_board[row][col].getP1().getX()
                            + tile_board[row][col].getP2().getX()
                        )
                        / 2
                        + tile_size / 4,
                        (
                            tile_board[row][col].getP1().getY()
                            + tile_board[row][col].getP2().getY()
                        )
                        / 2,
                    ),
                    image_name,
                    int(tile_size / 4),
                    int(tile_size / 2),
                )
            )

    return images


def create_value_board(tile_board: list, minesweeper_board: MinesweeperBoard) -> list:
    """
    Create a board of images representing tile values for drawing onto the window based on the given minesweeper board.

    Parameters
    ----------
    tile_board : list
        The 2D array of squares representing the tiles on the minesweeper board.

    minesweeper_board : MinesweeperBoard
        The minesweeper board to draw the values from.

    Returns
    -------
    list
        The 2D array of images.
    """

    tile_size = min(
        (WINDOW_HEIGHT - WINDOW_BORDERS) / minesweeper_board.board_height,
        (WINDOW_WIDTH - WINDOW_BORDERS) / minesweeper_board.board_width,
    )

    # create a 2D array of image lists representing values on the board
    value_board = []
    for i in range(len(minesweeper_board.board)):
        value_board.append([])
        for j in range(len(minesweeper_board.board[i])):
            value_board[i].append(
                get_value_images(i, j, tile_size, tile_board, minesweeper_board)
            )

    return value_board


def draw_tile_board(tile_board: list):
    """
    Draw the given board of rectangular tiles onto the window.

    Parameters
    ----------
    tile_board : list
        The board of tiles to draw onto the window.
    """

    for row in tile_board:
        for button in row:
            button.draw(win)


def draw_value_board(value_board: list):
    """
    Draw the given board of tile values onto the window.

    Parameters
    ----------
    value_board: list
        The board of tile values to draw on top of the tiles.
    """

    for row in value_board:
        for value in row:
            for image in value:
                image.draw(win)


def update_tile_board(tile_board: list, minesweeper_board: MinesweeperBoard):
    """
    Redraw all tiles that changed last move.

    Parameters
    ----------
    tile_board : list
        The board of tiles to redraw.

    minesweeper_board : list
        The minesweeper board to draw from.
    """

    for i in range(minesweeper_board.board_height):
        for j in range(minesweeper_board.board_width):

            # if the tile was updated last move, redraw the tile
            if (
                minesweeper_board.board[i][j].changed_last_move
                and minesweeper_board.board[i][j].revealed
            ):
                tile_board[i][j].undraw()
                tile_board[i][j].setFill(REVEALED_TILE_COLOR)
                tile_board[i][j].draw(win)


def update_value_board(
    value_board: list, tile_board: list, minesweeper_board: MinesweeperBoard
):
    """
    Redraw all tile values on tiles that changed last move.

    Parameters
    ----------
    value_board : list
        The board of tile values to redraw.

    tile_board : list
        The 2D array of squares representing the tiles on the minesweeper board.

    minesweeper_board : list
        The minesweeper board to draw from.
    """

    tile_size = min(
        (WINDOW_HEIGHT - WINDOW_BORDERS) / minesweeper_board.board_height,
        (WINDOW_WIDTH - WINDOW_BORDERS) / minesweeper_board.board_width,
    )

    for i in range(minesweeper_board.board_height):
        for j in range(minesweeper_board.board_width):

            # if the tile was updated last move, redraw the tile value
            if minesweeper_board.board[i][j].changed_last_move:
                for image in value_board[i][j]:
                    image.undraw()

                value_board[i][j] = get_value_images(
                    i, j, tile_size, tile_board, minesweeper_board
                )

                for image in value_board[i][j]:
                    image.draw(win)


def get_clicked_tile_coords(point: Point, minesweeper_board: MinesweeperBoard):
    """
    Find the coordinates of the tile that was clicked, based on the tile size.

    Parameters
    ----------
    point : Point
        The mouse point to check the position of.

    minesweeper_board : MinesweeperBoard
        The game object representation of the board holding the tile information.

    Returns
    -------
    tuple
        The row and column of the tile that was clicked, in the form (row, col).

    Notes
    -----
    The row and column values are calculated by taking the point's x and y coordinates, subtracting the window borders, and dividing by the tile size.
    """

    tile_size = min(
        (WINDOW_HEIGHT - WINDOW_BORDERS) / minesweeper_board.board_height,
        (WINDOW_WIDTH - WINDOW_BORDERS) / minesweeper_board.board_width,
    )
    row = (
        point.getY() - (WINDOW_HEIGHT - tile_size * minesweeper_board.board_height) / 2
    ) // tile_size
    col = (
        point.getX() - (WINDOW_WIDTH - tile_size * minesweeper_board.board_width) / 2
    ) // tile_size

    return (int(row), int(col))


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
        How difficult the game should be (ONLY affects certain gamemods, such as Distance Minesweeper, and not Regular Minesweeper)
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

        # get tile the user clicked
        clicked_point, mouse_button = win.getMouse()
        clicked_tile = get_clicked_tile_coords(clicked_point, minesweeper_board)

        # if the clicked button was left, make a move on the clicked tile (if that tile doesn't have a flag)
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
    WIDTH = 16
    HEIGHT = 16
    NUM_MINES = 40
    VERSION = 4
    DIFFICULTY = "easy"
    run_game(WIDTH, HEIGHT, NUM_MINES, VERSION, DIFFICULTY)
