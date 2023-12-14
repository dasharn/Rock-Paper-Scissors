import socket
from  _thread import start_new_thread
import pickle
import sys
from game import Game
import socket

class Server:
    """
    A class to represent a server.

    ...

    Attributes
    ----------
    server : str
        the server address (default is localhost)
    port : int
        the port number to connect to (default is 5555)
    s : socket
        the socket object
    games : dict
        a dictionary to store games
    id_count : int
        a counter for game ids

    """

    def __init__(self, server="localhost", port=5555):
        """
        Constructs all the necessary attributes for the server object.

        Parameters
        ----------
            server : str, optional
                server address (default is localhost)
            port : int, optional
                port number (default is 5555)
        """
        self.server = server
        self.port = port
        self.s = self.setup_socket()
        self.games = {}
        self.id_count = 0

    def setup_socket(self):
        """
        Sets up the socket connection.

        This method creates a socket object, binds it to the specified server address and port, 
        and starts listening for incoming connections. If binding fails, it prints an error message 
        and exits the program.

        Returns
        -------
        s : socket
            The socket object that's been set up.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.server, self.port))
        except socket.error as e:
            print(f"Socket error: {str(e)}")
            sys.exit(1)

        s.listen(2)
        print("Waiting for a connection, Server Started")
        return s


    def handle_client(self, conn, player, game_id):
        """
        Handles client connection and game data processing.

        This method sends the player data to the client, then enters a loop where it continuously 
        receives data from the client. If the game_id is not in the games dictionary, it breaks 
        the loop. If no data is received, it also breaks the loop. Otherwise, it processes the 
        received data and sends the updated game state back to the client. If any exception occurs, 
        it breaks the loop and closes the connection.

        Parameters
        ----------
        conn : socket
            The client socket object.
        player : object
            The player object.
        game_id : int
            The id of the game.

        """
        conn.send(str.encode(str(player)))

        while True:
            try:
                data = conn.recv(4096).decode()

                if game_id not in self.games:
                    break

                game = self.games[game_id]

                if not data:
                    break
                else:
                    self.process_data(game, data, player)

                conn.sendall(pickle.dumps(game))
            except:
                break

        self.close_connection(conn, game_id)

    def process_data(self, game, data, player):
        """
        Processes the received data from the client.

        This method checks the received data and performs actions based on its value. 
        If the data is "reset", it resets the game. If the data is not "get", it makes a play.

        Parameters
        ----------
        game : object
            The game object.
        data : str
            The received data from the client.
        player : object
            The player object.
        """
        if data == "reset":
            game.resetWent()
        elif data != "get":
            game.play(player, data)

    def close_connection(self, conn, game_id):
        """
        Closes the connection with the client and deletes the game.

        This method prints a message indicating that the connection was lost, 
        attempts to delete the game from the games dictionary, decreases the id_count by 1, 
        and closes the connection.

        Parameters
        ----------
        conn : socket
            The client socket object.
        game_id : int
            The id of the game.
        """
        print("Lost connection")
        try:
            del self.games[game_id]
            print("Closing Game", game_id)
        except:
            pass
        self.id_count -= 1
        conn.close()

    def run(self):
        """
        Runs the server.

        This method enters a loop where it waits for a client to connect. 
        When a client connects, it increments the id_count, determines the player number, 
        and either creates a new game or sets the existing game to ready. 
        It then starts a new thread to handle the client.

        """
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            self.id_count += 1
            p = 0
            game_id = (self.id_count - 1)//2
            if self.id_count % 2 == 1:
                self.games[game_id] = Game(game_id)
                print("Creating a new game...")
            else:
                self.games[game_id].ready = True
                p = 1

            start_new_thread(self.handle_client, (conn, p, game_id))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <server> <port> \n e.g. python server.py localhost 5555")
        sys.exit(1)

    try:
        server = sys.argv[1]
        port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be an integer")
        sys.exit(1)

    s = Server(server, port)
    s.run()