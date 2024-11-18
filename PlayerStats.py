import pickle


class PlayerStats:
    """
    Holds the base template for the player stats dictionary, which is read in and out of the 'stats' file

    Parameters
    ----------
    player_stats: dict[str, dict[str, float]], default: {}
        The dictionary holding the player's stats for the different gamemodes.
    """

    starting_player_stats = {
        "Minesweeper": {
            # The number of times the player has won on any settings
            "Wins": 0,
            # The number of times the player has lost on any settings
            "Losses": 0,
            # The total number of tiles the player has revealed
            "Tiles Revealed": 0,
            # The number of flags the player has correctly placed on mines
            "Mines Defused": 0,
            # The number of flags the player has incorrectly placed on mines
            "Flag Mistakes": 0,
            # The total number of mines across all maps the player has played
            # Used for calculating average defused mine count in played games
            "Mines Encountered": 0,
            # The total number of seconds the player has spent on attempts where they've won
            # Used for calculating average time to win
            "Total Win Time": 0,
            # The total number of seconds the player has spent on attempts where they've lost
            # Used for calculating general average play time
            "Total Loss Time": 0,
        },
        "Minesweeper V": {
            # The number of times the player has won on any settings
            "Wins": 0,
            # The number of times the player has lost on any settings
            "Losses": 0,
            # The total number of tiles the player has clicked
            "Tiles Revealed": 0,
            # The number of flags the player has correctly placed on mines
            "Mines Defused": 0,
            # The number of flags the player has incorrectly placed on mines
            "Flag Mistakes": 0,
            # The total number of mines across all maps the player has played
            # Used for calculating average mine count in played games
            "Mines Encountered": 0,
            # The total number of seconds the player has spent on attempts where they've won
            # Used for calculating average time to win
            "Total Win Time": 0,
            # The total number of seconds the player has spent on attempts where they've lost
            # Used for calculating general average play time
            "Total Loss Time": 0,
        },
        "Distance Minesweeper": {
            # The number of times the player has won on easy difficulty
            "Easy Wins": 0,
            # The number of times the player has won on medium difficulty
            "Medium Wins": 0,
            # The number of times the player has won on hard difficulty
            "Hard Wins": 0,
            # The number of times the player has lost on easy difficulty
            "Easy Losses": 0,
            # The number of times the player has lost on medium difficulty
            "Medium Losses": 0,
            # The number of times the player has lost on hard difficulty
            "Hard Losses": 0,
            # The total number of tiles the player has clicked
            "Tiles Revealed": 0,
            # The number of flags the player has correctly placed on mines
            "Mines Defused": 0,
            # The number of flags the player has incorrectly placed on mines
            "Flag Mistakes": 0,
            # The total number of mines across all maps the player has played
            # Used for calculating average mine count in played games
            "Mines Encountered": 0,
            # The total number of seconds the player has spent on attempts where they've won on easy difficulty
            # Used for calculating average time to win on easy difficulty
            "Total Win Time Easy": 0,
            # The total number of seconds the player has spent on attempts where they've won on medium difficulty
            # Used for calculating average time to win on medium difficulty
            "Total Win Time Medium": 0,
            # The total number of seconds the player has spent on attempts where they've won on hard difficulty
            # Used for calculating average time to win on hard difficulty
            "Total Win Time Hard": 0,
            # The total number of seconds the player has spent on attempts where they've lost
            # Used for calculating general average play time
            "Total Loss Time": 0,
        },
        "Weighted Minesweeper": {
            # The number of times the player has won on easy difficulty
            "Easy Wins": 0,
            # The number of times the player has won on medium difficulty
            "Medium Wins": 0,
            # The number of times the player has won on hard difficulty
            "Hard Wins": 0,
            # The number of times the player has lost on easy difficulty
            "Easy Losses": 0,
            # The number of times the player has lost on medium difficulty
            "Medium Losses": 0,
            # The number of times the player has lost on hard difficulty
            "Hard Losses": 0,
            # The total number of tiles the player has clicked
            "Tiles Revealed": 0,
            # The number of flags the player has correctly placed on mines
            "Mines Defused": 0,
            # The number of flags the player has incorrectly placed on mines
            "Flag Mistakes": 0,
            # The total number of mines across all maps the player has played
            # Used for calculating average mine count in played games
            "Mines Encountered": 0,
            # The total number of seconds the player has spent on attempts where they've won on easy difficulty
            # Used for calculating average time to win on easy difficulty
            "Total Win Time Easy": 0,
            # The total number of seconds the player has spent on attempts where they've won on medium difficulty
            # Used for calculating average time to win on medium difficulty
            "Total Win Time Medium": 0,
            # The total number of seconds the player has spent on attempts where they've won on hard difficulty
            # Used for calculating average time to win on hard difficulty
            "Total Win Time Hard": 0,
            # The total number of seconds the player has spent on attempts where they've lost
            # Used for calculating general average play time
            "Total Loss Time": 0,
        },
        "Negative Minesweeper": {
            # The number of times the player has won on easy difficulty
            "Easy Wins": 0,
            # The number of times the player has won on medium difficulty
            "Medium Wins": 0,
            # The number of times the player has won on hard difficulty
            "Hard Wins": 0,
            # The number of times the player has lost on easy difficulty
            "Easy Losses": 0,
            # The number of times the player has lost on medium difficulty
            "Medium Losses": 0,
            # The number of times the player has lost on hard difficulty
            "Hard Losses": 0,
            # The total number of tiles the player has clicked
            "Tiles Revealed": 0,
            # The number of flags the player has correctly placed on positive mines
            "Positive Mines Defused": 0,
            # The number of flags the player has correctly placed on negative mines
            "Negative Mines Defused": 0,
            # The number of flags the player has incorrectly placed on positive mines
            "Positive Flag Mistakes": 0,
            # The number of flags the player has incorrectly placed on negative mines
            "Negative Flag Mistakes": 0,
            # The total number of positive mines across all maps the player has played
            # Used for calculating average mine count in played games
            "Positive Mines Encountered": 0,
            # The total number of negative mines across all maps the player has played
            # Used for calculating average mine count in played games
            "Negative Mines Encountered": 0,
            # The total number of seconds the player has spent on attempts where they've won on easy difficulty
            # Used for calculating average time to win on easy difficulty
            "Total Win Time Easy": 0,
            # The total number of seconds the player has spent on attempts where they've won on medium difficulty
            # Used for calculating average time to win on medium difficulty
            "Total Win Time Medium": 0,
            # The total number of seconds the player has spent on attempts where they've won on hard difficulty
            # Used for calculating average time to win on hard difficulty
            "Total Win Time Hard": 0,
            # The total number of seconds the player has spent on attempts where they've lost
            # Used for calculating general average play time
            "Total Loss Time": 0,
        },
    }

    def __init__(self, player_stats=None):
        self.player_stats = player_stats if player_stats is not None else {}

    def load_player_stats(self):
        """
        Load the player's stats, or create a new stats file if there isn't one already.
        """

        try:
            with open("stats", "rb") as stats_file:
                self.player_stats = pickle.load(stats_file)
        except FileNotFoundError:
            self.reset_stats()
            self.player_stats = self.starting_player_stats

    def save_player_stats(self):
        """
        Save the player's stats to an extension-less "stats" file.
        """

        with open("stats", "wb") as stats_file:
            pickle.dump(self.player_stats, stats_file, protocol=pickle.HIGHEST_PROTOCOL)

    def reset_stats(self):
        """
        Reset the stats file to the starting player stats (0s across the board).
        """

        with open("stats", "wb") as stats_file:
            pickle.dump(self.starting_player_stats, stats_file, protocol=pickle.HIGHEST_PROTOCOL)

    def increment_stat(
        self,
        minesweeper_version: str,
        stat_to_increment: str,
        increment_value: float = 1.0,
    ) -> bool:
        """
        Increment a given stat for a given Minesweeper version.
        If the stat or Minesweeper version can't be found, the update fails and return False.

        Parameters
        ----------
        minesweeper_version: str
            The version of Minesweeper to increment the stat for.

        stat_to_increment: str
            The name of the stat to increment.

        increment_value: float, default: 1.0
            The value to increment the stat by.

        Returns
        -------
        bool
            Whether the update was successful or not.
        """

        if minesweeper_version in self.player_stats and stat_to_increment in self.player_stats[minesweeper_version]:
            self.player_stats[minesweeper_version][stat_to_increment] += increment_value
            return True
        return False

    def get_stat(self, minesweeper_version: str, stat: str = None) -> float | dict[str, float]:
        """
        Retrieve a given stat for a given Minesweeper version.
        If no stat is given, retrieve ALL stats for that Minesweeper version as a dictionary.

        Parameters
        ----------
        minesweeper_version: str
            The version of Minesweeper to fetch the stat for.

        stat: str, optional
            The stat to fetch. Fetches ALL stats as a dictionary if left blank.

        Returns
        -------
        float | dict[str, float]
            The value of the stat, or a dictionary of values for ALL stats if stat is left blank. Returns 0.0 if the stat can't be found, or an empty dictionary if stats is None and the minesweeper_version can't be found.
        """

        if stat is not None:
            return self.player_stats.get(minesweeper_version, {}).get(stat, 0.0)
        else:
            return self.player_stats.get(minesweeper_version, {})
