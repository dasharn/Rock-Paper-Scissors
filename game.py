

from outcome import Outcome

from move import Move

class Game:
    """
    A class to represent a game.

    ...

    Attributes
    ----------
    p1_went : bool
        a flag indicating whether player 1 has made a move
    p2_went : bool
        a flag indicating whether player 2 has made a move
    ready : bool
        a flag indicating whether the game is ready to start
    id : int
        the id of the game
    moves : list
        a list to store the moves of the players
    wins : list
        a list to store the wins of the players
    ties : int
        a counter for the number of ties
    winning_combinations : dict
        a dictionary to store the winning combinations

    """
    def __init__(self, game_id: int):
        self.p1_went = False
        self.p2_went = False
        self.ready = False
        self.id = game_id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.winning_combinations = [('R', 'S'), ('S', 'P'), ('P', 'R')] # for player 1
        self.ties = 0

    def get_player_move(self, player: int) -> Move:
        """Get the move made by a player."""
        return Move(self.moves[player]).value

    def play(self, player: int, move: Move):
        """Record the move made by a player."""
        self.moves[player] = move.value
        if player == 0:
            self.p1_went = True
        else:
            self.p2_went = True

    def connected(self) -> bool:
        """Check if the game is ready to start."""
        return self.ready

    def both_went(self) -> bool:
        """Check if both players have made a move."""
        return self.p1_went and self.p2_went

    def winner(self) -> Outcome:
        """Determine the winner of the game."""
        p1 = self.moves[0]
        p2 = self.moves[1]

        if p1 == p2:
            return Outcome.TIE

        

        if (p1, p2) in self.winning_combinations:
            return Outcome.PLAYER1.value
        else:
            return Outcome.PLAYER2.value

    def reset_went(self):
        """Reset the moves made by the players."""
        self.p1_went = False
        self.p2_went = False

g = Game(0)
g.moves = ['R', 'P']
print(g.get_player_move(0))
print(g.winner())