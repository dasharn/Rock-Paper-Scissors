import unittest
from game import Game, Move, Outcome

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(1)

    def test_get_player_move(self):
        self.game.play(0, Move.ROCK)
        self.assertEqual(self.game.get_player_move(0), 'ROCK')

    def test_play(self):
        self.game.play(0, Move.PAPER)
        self.assertEqual(self.game.moves[0], 'PAPER')
        self.assertTrue(self.game.p1_went)

    def test_connected(self):
        self.assertFalse(self.game.connected())

    def test_both_went(self):
        self.game.play(0, Move.ROCK)
        self.assertFalse(self.game.both_went())
        self.game.play(1, Move.PAPER)
        self.assertTrue(self.game.both_went())

    def test_winner(self):
        self.game.play(0, Move.ROCK)
        self.game.play(1, Move.SCISSORS)
        self.assertEqual(self.game.winner(), 'PLAYER1')

    def test_reset_went(self):
        self.game.play(0, Move.ROCK)
        self.game.play(1, Move.PAPER)
        self.assertTrue(self.game.p1_went)
        self.assertTrue(self.game.p2_went)
        self.game.reset_went()
        self.assertFalse(self.game.p1_went)
        self.assertFalse(self.game.p2_went)

if __name__ == '__main__':
    unittest.main()