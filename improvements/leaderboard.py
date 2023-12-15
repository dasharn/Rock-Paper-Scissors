# Authors: Dasharn Dennis (solo)
import heapq
from collections import defaultdict

class Leaderboard:
    
    """
    Class for managing the game leaderboard.

    Attributes
    ----------
    scores : defaultdict
        A defaultdict to store player names and their scores.
    heap : list
        A list of tuples to store player names and their scores for the heap.

    Methods
    -------
    add_score(player_name, score):
        Adds a new score for the player.
    get_score(player_name):
        Returns the score of a particular player.
    get_top_scores(n):
        Returns the top n scores.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the leaderboard object.

        Parameters
        ----------
        scores : defaultdict
            A defaultdict to store player names and their scores.
        heap : list
            A list of tuples to store player names and their scores for the heap.
        """
        self.scores = defaultdict(int)
        

    def add_score(self, player_name, score):
        """
        Adds a new score for the player.

        Parameters
        ----------
        player_name : str
            The name of the player.
        score : int
            The score of the player.
        """
        self.scores[player_name] += score
        

    def get_score(self, player_name):
        """
        Returns the score of a particular player.

        Parameters
        ----------
        player_name : str
            The name of the player.

        Returns
        -------
        int
            The score of the player.
        """
        return self.scores[player_name]

    def get_top_scores(self, n):
        """
        Returns the top n scores.

        Parameters
        ----------
        n : int
            The number of top scores to return.

        Returns
        -------
        list
            A list of tuples containing the player names and their scores, sorted in descending order.
        """
        self.heap = [(-score, player_name) for player_name, score in self.scores.items()]
        return heapq.nlargest(n, self.heap)