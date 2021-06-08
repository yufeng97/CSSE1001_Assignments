import json

class HighScoreManager:
    """A HighScoreManager manages the recording of highscores achieved to
    a highscore file.
    """
    _data = None

    def __init__(self, file="highscores.json", gamemode='regular',
                 auto_save=True, top_scores=10):
        """Constructs a HighScoreManager using the provided json file.

        Parameters:
            file (str): The name of the json file which stores the highscore
                        information.
            gamemode (str): The name of the gamemode to load highscores from.
            auto_save (bool): If true the manager saves the scores automatically
                              when a record is added.
            top_scores (int): The number of high scores to store to file.
        """
        self._file = file
        self._top_scores = top_scores
        self._auto_save = auto_save
        self._gamemode = gamemode

        if self._auto_save:
            self.load()

    def _load_json(self):
        """Loads the highscore json file."""
        try:
            with open(self._file) as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    # Failed to decode the json file
                    # Default to empty leaderboard
                    data = {}
        except IOError:
            # Could not locate the json file
            # Default to empty leaderboard
            data = {}

        if self._gamemode not in data:
            data[self._gamemode] = []

        return data

    def load(self):
        """Loads the highscore information from the highscores file into the
        manager.
        """
        data = self._load_json()
        self._data = data[self._gamemode]

    def save(self):
        """Saves the information added to the highscore manager to the file."""
        data = self._load_json()
        with open(self._file, "w") as file:
            data[self._gamemode] = self._data
            file.write(json.dumps(data, indent=2))

    def record(self, score, grid, name=None):
        """Makes a record of a gameplay based on the score, final grid and name.

        Parameters:
            score (int): The top score of the gameplay.
            grid (LoloGrid): A grid to be serialized into the file.
            name (str): The name of the player who played the recorded game.
        """
        scores = self.get_scores()
        data = {"score": score, "name": str(name), "grid": grid.serialize()}

        if len(scores) < self._top_scores:
            self._data.append(data)
        elif score > min(scores):
            self.replace_record(min(scores), data)

        if self._auto_save:
            self.save()

    def replace_record(self, old_score, new_data):
        """Replaces a record based by finding the old score

        Parameters:
            old_score (int): The score of the record to replace.
            new_data (dict<str, *>): The record to replace the old record with.
        """
        min_score_index = self.get_scores().index(old_score)
        self._data[min_score_index] = new_data

    def __iter__(self):
        """Loop through each record in the highscores file.

        Yield:
            record (dict<str, int>): The record being yielded
        """
        for record in self.get_sorted_data():
            yield record

    def __len__(self):
        return len(self.get_data())

    def get_data(self):
        """(list<dict<str, *>>) Returns a list of all the records in the file"""
        return self._data

    def get_sorted_data(self):
        """(list<dict<str, *>>) Returns a sorted list of records in the file."""
        return sorted(self._data, key=lambda x: -x["score"])

    def get_scores(self):
        """(list<int>) Returns a list of all the scores in the file."""
        return [player['score'] for player in self._data]

    def get_names(self):
        """(list<str>) Returns a list of all the scores in the file."""
        return [player['name'] for player in self._data]

    def get_grids(self):
        """(list<list<list<tuple<int, int>>>>) Returns a list of all the scores
                                               in the file."""
        return [player['grid'] for player in self._data]
