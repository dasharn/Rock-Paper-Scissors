import pygame
from network import Network
from button import Button
from settings import Settings, ButtonSettings
class Client:
    """
    A class to represent a client in a game.

    ...

    Attributes
    ----------
    width : int
        the width of the game window
    height : int
        the height of the game window
    win : pygame.Surface
        the game window
    btns : list
        a list of buttons for the game options

    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the client object.

        Initializes the pygame font, sets the width and height of the game window, 
        creates the game window, sets the window caption, and creates the game option buttons.
        """
        pygame.font.init()
        self.width = Settings.WIDTH.value
        self.height = Settings.HEIGHT.value
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(Settings.CAPTION.value)
        self.btns = [Button(btn["text"], btn["x"], btn["y"], btn["color"]) for btn in Settings.BUTTONS.value]

    def draw_text(self, text, font, color, x, y):
        """
        Draws text on the game window.

        This method creates a text surface with the provided text, font, and color, 
        and then blits it to the game window at the provided coordinates.

        Parameters
        ----------
        text : str
            The text to be drawn.
        font : pygame.font.Font
            The font of the text.
        color : tuple
            The color of the text.
        x : int
            The x-coordinate of the text.
        y : int
            The y-coordinate of the text.
        """
        text_surface = font.render(text, True, color)
        self.win.blit(text_surface, (x - text_surface.get_width() / 2, y - text_surface.get_height() / 2))

    def redraw_window(self, game, p):
        """
        Redraws the game window.

        This method fills the game window with a color, creates two fonts, 
        and then either draws a waiting message if the game is not connected, 
        or draws the game state if it is. It then updates the display.

        Parameters
        ----------
        game : Game
            The game object.
        p : int
            The player number.
        """
        self.win.fill((128,128,128))
        font_80 = pygame.font.SysFont("comicsans", 80)
        font_60 = pygame.font.SysFont("comicsans", 60)

        if not game.connected():
            self.draw_waiting_for_player(font_80)
        else:
            self.draw_game_state(game, p, font_60)

        pygame.display.update()

    def draw_waiting_for_player(self, font):
        """
        Draws a "Waiting for Player..." message on the game window.

        This method uses the draw_text method to draw the message 
        "Waiting for Player..." in the middle of the game window.

        Parameters
        ----------
        font : pygame.font.Font
            The font of the text.
        """
        self.draw_text("Waiting for Player...", font, (255,0,0), self.width/2, self.height/2)

    def draw_game_state(self, game, p, font):
        """
        Draws the game state on the game window.

        This method draws the current move of the player and the opponent on the game window.
        It also draws the game option buttons.

        Parameters
        ----------
        game : Game
            The game object.
        p : int
            The player number.
        font : pygame.font.Font
            The font of the text.
        """
        self.draw_text("Your Move", font, (0, 255,255), 80, 200)
        self.draw_text("Opponents", font, (0, 255,255), 380, 200)

        text1, text2 = self.get_player_texts(game, p)

        self.draw_text(text1, font, (0,0,0), 100, 350)
        self.draw_text(text2, font, (0,0,0), 400, 350)

        for btn in self.btns:
            btn.draw(self.win)

    def get_player_texts(self, game, p):
        """
        Gets the texts to be displayed for the players.

        This method gets the current move of each player from the game object, 
        and then determines the text to be displayed for each player based on 
        whether they have made their move.

        Parameters
        ----------
        game : Game
            The game object.
        p : int
            The player number.

        Returns
        -------
        tuple
            The texts to be displayed for the players.
        """
        move1, move2 = game.get_player_move(0), game.get_player_move(1)
        text1, text2 = "Waiting...", "Waiting..."

        if game.bothWent():
            text1, text2 = move1, move2
        else:
            if game.p1Went:
                text1 = move1 if p == 0 else "Locked In"
            if game.p2Went:
                text2 = move2 if p == 1 else "Locked In"

        if p == 1:
            text1, text2 = text2, text1

        return text1, text2

    def handle_game_over(self, game, player, font_90):
        """
        Handles the game over state.

        This method determines the outcome of the game (win, loss, or tie) based on the game's winner 
        and the player number. It then renders a message indicating the outcome, 
        blits it to the game window, updates the display, and delays for 2 seconds.

        Parameters
        ----------
        game : Game
            The game object.
        player : int
            The player number.
        font_90 : pygame.font.Font
            The font of the text.
        """
        if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
            text = font_90.render("You Won!", 1, (255,0,0))
        elif game.winner() == -1:
            text = font_90.render("Tie Game!", 1, (255,0,0))
        else:
            text = font_90.render("You Lost...", 1, (255, 0, 0))

        self.win.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)

    def handle_mouse_event(self, event, game, player, n):
        """
        Handles mouse events.

        This method checks if the event is a mouse button down event. If it is, it gets the current 
        position of the mouse and checks if any of the game option buttons have been clicked. If a button 
        has been clicked and the game is connected, it sends the text of the button to the server if the 
        player has not yet made their move.

        Parameters
        ----------
        event : pygame.event.Event
            The event to be handled.
        game : Game
            The game object.
        player : int
            The player number.
        n : Network
            The network object.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for btn in self.btns:
                if btn.click(pos) and game.connected():
                    if player == 0 and not game.p1Went or player == 1 and not game.p2Went:
                        n.send(btn.text)
                        
    def update_game_state(self, n, action):
        """
        Updates the game state.

        This method sends an action to the server via the network object and receives the updated game state. 
        If an exception occurs during this process, it prints an error message and returns None.

        Parameters
        ----------
        n : Network
            The network object.
        action : str
            The action to be sent to the server.

        Returns
        -------
        Game or None
            The updated game state, or None if an error occurred.
        """
        try:
            game = n.send(action)
            return game
        except Exception as e:
            print(f"Couldn't get game: {e}")
            return None

    def main(self):
        """
        Runs the main game loop.

        This method initializes the game, creates a network object, gets the player number from the server, 
        and then enters a loop that runs at 60 frames per second. In each iteration of the loop, it updates 
        the game state, redraws the game window, and handles any events. If both players have made their move, 
        it delays for half a second, updates the game state again, and then handles the game over state. 
        The loop continues until the game is no longer running.
        """
        run = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP())
        print(f"You are player {player}")

        font_90 = pygame.font.SysFont("comicsans", 90)

        while run:
            clock.tick(60)

            game = self.update_game_state(n)
            if game is None:
                run = False
                break

            if game.bothWent():
                self.redraw_window(game, player)
                pygame.time.delay(500)

                game = self.update_game_state(n)
                if game is None:
                    run = False
                    break
                

                self.handle_game_over(game, player, font_90)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                self.handle_mouse_event(event, game, player, n)

            self.redraw_window(game, player)

    def menu_screen(self):
        """
        Displays the menu screen.

        This method runs a loop that displays the menu screen with the text "Click to Play!". 
        It updates the display at a rate of 60 frames per second. If the user clicks the mouse 
        or closes the window, it stops the loop and calls the main method.

        """
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.win.fill((128, 128, 128))
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, (255,0,0))
            self.win.blit(text, (100,200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        self.main()

if __name__ == "__main__":
    gc = Client()
    while True:
        gc.menu_screen()
