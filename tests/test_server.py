import unittest
from server import Server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

    def test_setup_socket(self):
        self.assertIsNotNone(self.server.setup_socket())

    def test_process_data_reset(self):
        game = Game(1)
        player = 0
        data = "reset"
        self.server.process_data(game, data, player)
        self.assertFalse(game.p1_went)
        self.assertFalse(game.p2_went)

    def test_process_data_play(self):
        game = Game(1)
        player = 0
        data = "ROCK"
        self.server.process_data(game, data, player)
        self.assertEqual(game.get_player_move(player), "ROCK")

    def test_close_connection(self):
        game_id = 1
        conn = None  # Replace with a mock socket object if available
        self.server.close_connection(conn, game_id)
        self.assertNotIn(game_id, self.server.games)
        self.assertEqual(self.server.id_count, 0)

if __name__ == '__main__':
    unittest.main()