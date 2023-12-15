import unittest
from server import Server
from game import Game

class TestServer(unittest.TestCase):
    """
    A test case for the Server class.

    This test case includes test methods to verify the functionality of the Server class.

    Methods
    -------
    setUp():
        Sets up the test environment.
    test_setup_socket():
        Tests the 'setup_socket' method of the Server class.
    test_process_data_reset():
        Tests the 'process_data' method of the Server class with "reset" data.
    test_process_data_play():
        Tests the 'process_data' method of the Server class with a move data.
    test_close_connection():
        Tests the 'close_connection' method of the Server class.
    """

    def setUp(self):
        """
        Sets up the test environment before each test case.
        Creates a new instance of the Server class.
        """
        self.server = Server()

    def test_setup_socket(self):
        """
        Tests the 'setup_socket' method of the Server class.
        Asserts that the method returns a non-None value.
        """
        self.assertIsNotNone(self.server.setup_socket())

    def test_process_data_reset(self):
        """
        Tests the 'process_data' method of the Server class with "reset" data.
        Asserts that the game state is correctly reset.
        """
        game = Game(1)
        player = 0
        data = "reset"
        self.server.process_data(game, data, player)
        self.assertFalse(game.p1_went)
        self.assertFalse(game.p2_went)

    def test_process_data_play(self):
        """
        Tests the 'process_data' method of the Server class with a move data.
        Asserts that the move is correctly recorded.
        """
        game = Game(1)
        player = 0
        data = "ROCK"
        self.server.process_data(game, data, player)
        self.assertEqual(game.get_player_move(player), "ROCK")

    def test_close_connection(self):
        """
        Tests the 'close_connection' method of the Server class.
        Asserts that the game is correctly removed from the server's games and the id_count is reset.
        """
        game_id = 1
        conn = None  # Replace with a mock socket object if available
        self.server.close_connection(conn, game_id)
        self.assertNotIn(game_id, self.server.games)
        self.assertEqual(self.server.id_count, 0)

if __name__ == '__main__':
    unittest.main()