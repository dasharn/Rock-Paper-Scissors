# Online Rock-Paper-Scissors

Online Rock-Paper-Scissors is a multiplayer game created using pygame and sockets, allowing players to enjoy endless rounds of the classic game remotely.

## Running The Game

To play Online Rock-Paper-Scissors, follow these steps:

1. **Server Setup:**
   - Start by running an instance of `server.py` on a machine that will act as the game server.
   - Open `server.py` and change the **server** address to the IPv4 address of your server machine or the specific server IP address you intend to use.

2. **Client Setup:**
   - On other machines, run instances of `client.py` to connect to the game server.
   - Similarly, open `client.py` on each client machine and ensure that the **server** address matches the server's IPv4 address or the chosen server IP address.

3. **Gameplay:**
   - Once clients are connected to the server, they can play Rock-Paper-Scissors games against each other.
   - Enjoy unlimited rounds of the game remotely with your friends or other players connected to the server.

Now you're ready to have fun playing Online Rock-Paper-Scissors with your friends or fellow gamers!

Please ensure that your server machine has the necessary network configuration to allow incoming connections, and make sure that all clients have the correct server address configured in `client.py`. If you encounter any issues, consult the troubleshooting section or seek assistance from the game's documentation.

Happy gaming!
