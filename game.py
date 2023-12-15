class Game:
    def __init__(self, id: int):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.game_rules = {'RS': 0, 'SP': 0, 'PR': 0, 'RP': 1, 'PS': 1, 'SR': 1}
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p: int) -> str:
        """
        Returns the move of the specified player.
        :param p: Player number [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player: int, move: str):
        """
        Records the move of the specified player.
        """
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self) -> bool:
        """
        Returns whether the game is ready for both players.
        """
        return self.ready

    def bothWent(self) -> bool:
        """
        Returns whether both players have made their moves.
        """
        return self.p1Went and self.p2Went

    def winner(self) -> int:
        """
        Determines the winner of the game based on the players' moves.
        Returns -1 if there's a tie.
        """
        
        players_moves = self.moves[0].upper()[0] + self.moves[1].upper()[0]
        return self.game_rules.get(players_moves, -1)

    def resetWent(self):
        """
        Resets the moves of both players.
        """
        self.p1Went = False
        self.p2Went = False