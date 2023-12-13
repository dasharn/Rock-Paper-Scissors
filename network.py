import socket
import pickle

class Network:
    """
    A class to represent a network connection.

    ...

    Attributes
    ----------
    _server : str
        a string representing the server address
    _port : int
        an integer representing the port number
    _p : str
        a string representing the player number received from the server
    _client : socket
        a socket object representing the client

    Methods
    -------
    p():
        Returns the player number.
    _connect():
        Connects to the server and receives the player number.
    send(data):
        Sends data to the server and receives the response.
    """

    def __init__(self, server="localhost", port=5555):
        """
        Constructs all the necessary attributes for the network object.

        Parameters
        ----------
            server : str, optional
                server address (default is "localhost")
            port : int, optional
                port number (default is 5555)
        """

        self._server = server
        self._port = port
        self._p = None
        self._connect()

    @property
    def p(self):
        """Returns the player number."""
        return self._p

    def _connect(self):
        """Connects to the server and receives the player number."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self._client:
                self._client.connect((self._server, self._port))
                self._p = self._client.recv(2048).decode()
        except socket.error as e:
            print(f"Socket error: {e}")

    def send(self, data):
        """
        Sends data to the server and receives the response.

        Parameters
        ----------
            data : str
                data to be sent to the server

        Returns
        -------
            response : object
                response received from the server
        """

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self._client:
                self._client.send(bytes(data, 'utf-8'))
                return pickle.loads(self._client.recv(2048*2))
        except socket.error as e:
            print(f"Socket error: {e}")