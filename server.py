import socket
from _from _thread import start_new_thread
import pickle
from game import Game
import socket

class Server:
    def __init__(self, server="localhost", port=5555):
        self.server = server
        self.port = port
        self.s = self.setup_socket()
        self.games = {}
        self.idCount = 0

    def setup_socket(self):
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
        if data == "reset":
            game.resetWent()
        elif data != "get":
            game.play(player, data)

    def close_connection(self, conn, game_id):
        print("Lost connection")
        try:
            del self.games[game_id]
            print("Closing Game", game_id)
        except:
            pass
        self.idCount -= 1
        conn.close()

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)

            self.idCount += 1
            p = 0
            game_id = (self.idCount - 1)//2
            if self.idCount % 2 == 1:
                self.games[game_id] = Game(game_id)
                print("Creating a new game...")
            else:
                self.games[game_id].ready = True
                p = 1

            start_new_thread(self.handle_client, (conn, p, game_id))

if __name__ == "__main__":
    s = Server()
    s.run()