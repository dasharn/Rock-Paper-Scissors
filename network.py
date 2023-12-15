import socket
import pickle

class Network:
    """
    A class to represent a network connection to a server.

    ...

    Attributes
    ----------
    client : socket
        a socket object representing the client socket
    server : str
        a string representing the server address, default is "localhost"
    port : int
        an integer representing the port number on which the server is listening, default is 5555
    addr : tuple
        a tuple containing the server address and port number
    p : str
        a string received from the server upon connection

    Methods
    -------
    getP():
        Returns the string received from the server upon connection.
    connect():
        Connects to the server and returns the string received upon connection.
    send(data):
        Sends data to the server and returns the data received in response.
    receive_data():
        Receives data from the server and returns it.
    """

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        """
        Connects to the server and returns the string received upon connection.

        This method attempts to connect to the server using the address stored in the addr attribute.
        If the connection is successful, it receives a string from the server and returns it.
        If a socket error occurs during this process, it prints the error and returns None.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The string received from the server upon connection, or None if there was a connection error.
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Connection error: {e}")
            return None

    def send(self, data):
        """
        Sends data to the server and returns the data received in response.

        This method attempts to send the provided data to the server.
        If the send is successful, it receives data from the server using the receive_data method and returns it.
        If a socket error occurs during this process, it prints the error and returns None.

        Parameters
        ----------
        data : str
            The data to be sent to the server.

        Returns
        -------
        object
            The data received from the server in response, or None if there was a send error.
        """
        try:
            self.client.send(str.encode(data))
            return self.receive_data()
        except socket.error as e:
            print(f"Send error: {e}")
            return None

    def receive_data(self):
        """
        Receives data from the server and returns it.

        This method attempts to receive data from the server and deserialize it using pickle.
        If the receive and deserialization are successful, it returns the deserialized data.
        If an error occurs during this process, it prints the error and returns None.

        Parameters
        ----------
        None

        Returns
        -------
        object
            The data received from the server, or None if there was a receive error.
        """
        try:
            return pickle.loads(self.client.recv(2048*2))
        except (pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError) as e:
            print(f"Receive error: {e}")
            return None