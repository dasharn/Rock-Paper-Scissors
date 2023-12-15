import socket
from _thread import *
import pickle
from game import Game

class Server:
    """
    A class to represent a server for managing multiple games and their respective clients.

    ...

    Attributes
    ----------
    server : str
        a string representing the server address, default is "localhost"
    port : int
        an integer representing the port number on which the server is listening, default is 5555
    s : socket
        a socket object representing the server socket
    connected : set
        a set to keep track of all connected clients
    games : dict
        a dictionary to keep track of all active games, with the game ID as the key and the game object as the value
    idCount : int
        an integer counter used to assign a unique ID to each game
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the server object.

        Parameters
        ----------
            None
        """
        self.server = "localhost"
        self.port = 5555
        self.s = self.setup_socket()
        self.connected = set()
        self.games = {}
        self.idCount = 0

    def setup_socket(self):
        """
        Sets up the server socket and starts listening for connections.

        This method creates a new socket using the AF_INET address family and the SOCK_STREAM socket type.
        It then binds the server and port to the socket and starts listening for connections.

        Parameters
        ----------
        None

        Returns
        -------
        s : socket
            The server socket object that is set up and listening for connections.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.server, self.port))
        s.listen(2)
        print("Waiting for a connection, Server Started")
        return s
    
    def handle_game_data(self, game, data, p):
        """
        Handles the game data received from the client.

        This method processes the data received from the client. If the data is "reset", it resets the game.
        If the data is anything other than "get", it makes a move in the game. The method then returns the game.

        Parameters
        ----------
        game : Game
            The game object that the data is related to.
        data : str
            The data received from the client.
        p : int
            The player number (0 or 1).

        Returns
        -------
        game : Game
            The updated game object after handling the received data.
        """
        if data == "reset":
            game.resetWent()
        elif data != "get":
            game.play(p, data)
        return game

    def threaded_client(self, conn, p, game_id):
        """
        Handles a client connection in a separate thread.

        This method sends the player number to the client, then enters a loop where it continuously receives data from the client.
        If the game ID is not in the games dictionary, or if no data is received, it breaks the loop.
        Otherwise, it handles the received data and sends the updated game object back to the client.
        If an exception occurs during this process, it prints the error and breaks the loop.
        After breaking the loop, it cleans up the game and connection.

        Parameters
        ----------
        conn : socket
        The socket connection object for the client.
        p : int
        The player number (0 or 1).
        game_id : int
        The unique ID of the game.

        Returns
        -------
        None
        """
        conn.send(str.encode(str(p)))

        while True:
            try:
                data = conn.recv(4096).decode()

                if game_id not in self.games:
                    break

                game = self.games[game_id]

                if not data:
                    break

                game = self.handle_game_data(game, data, p)
                conn.sendall(pickle.dumps(game))

            except Exception as e:
                print(f"Error occurred: {e}")
                break

        self.cleanup_game(conn, game_id)

    def cleanup_game(self, conn, game_id):
        print("Lost connection")
        try:
            del self.games[game_id]
            print("Closing Game", game_id)
        except Exception as e:
            print(f"Error while closing game: {e}")
        self.idCount -= 1
        conn.close()

    def run_server(self):
        """
        Runs the server, accepting new connections and starting new games.

        This method enters a loop where it continuously accepts new connections.
        For each new connection, it increments the idCount and calculates the game_id.
        If the idCount is odd, it creates a new game. If the idCount is even, it marks the game as ready and sets the player number to 1.
        It then starts a new thread to handle the client connection.

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            self.idCount += 1
            p = 0
            game_id = (self.idCount - 1) // 2
            if self.idCount % 2 == 1:
                self.games[game_id] = Game(game_id)
                print("Creating a new game...")
            else:
                self.games[game_id].ready = True
                p = 1

            start_new_thread(self.threaded_client, (conn, p, game_id))

if __name__ == "__main__":
    server = Server()
    server.run_server()

