class Game:
    """
    A class to represent a game of Rock, Paper, Scissors.

    ...

    Attributes
    ----------
    id : int
        unique identifier for the game
    p1_went : bool
        whether player 1 has made a move
    p2_went : bool
        whether player 2 has made a move
    ready : bool
        whether the game is ready to start
    moves : list
        the moves made by the players
    wins : list
        the wins by each player
    ties : int
        the number of ties
    winning_combinations : dict
        the winning combinations for the game

    Methods
    -------
    player_move(p):
        Returns the move made by the player.
    play(player, move):
        Records the move made by the player.
    connected():
        Returns whether the game is ready to start.
    both_went():
        Returns whether both players have made a move.
    winner():
        Returns the winner of the game.
    reset_went():
        Resets the moves made by the players.
    """

    def __init__(self, id):
        """
        Constructs all the necessary attributes for the game object.

        Parameters
        ----------
            id : int
                unique identifier for the game
        """

        self.p1_went = False
        self.p2_went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        self.winning_combinations = {'RS': 0, 'SP': 0, 'PR': 0, 'SR': 1, 'PS': 1, 'RP': 1}

    
    def player_move(self, p):
        """
        Returns the move made by the player.

        Parameters
        ----------
            p : int
                player number (0 or 1)

        Returns
        -------
            move : str
                move made by the player
        """

        return self.moves[p]

    def play(self, player, move):
        """
        Records the move made by the player.

        Parameters
        ----------
            player : int
                player number (0 or 1)
            move : str
                move made by the player
        """

        self.moves[player] = move
        if player == 0:
            self.p1_went = True
        else:
            self.p2_went = True

    
    def connected(self):
        """Returns whether the game is ready to start."""
        return self.ready

    
    def both_went(self):
        """Returns whether both players have made a move."""
        return self.p1_went and self.p2_went

    
    def winner(self):
        """
        Returns the winner of the game.

        Returns
        -------
            winner : int
                winner of the game (0 or 1), or None if it's a tie
        """

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        if p1 == p2:  # It's a tie
            return -1

        return self.winning_combinations.get(p1 + p2)

    def reset_went(self):
        """Resets the moves made by the players."""
        self.p1_went = False
        self.p2_went = False