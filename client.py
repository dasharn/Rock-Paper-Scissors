import pygame
from network import Network  # Assuming you have a Network class defined in a separate module
from button import Button
class Client:
    def __init__(self, width=600, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Rock, Paper, Scissors!")
        self.btns = [
            Button("Rock", 50, 500, (0, 0, 0)),
            Button("Scissors", 250, 500, (255, 0, 0)),
            Button("Paper", 450, 500, (0, 255, 0))
        ]
        self.n = Network()
        self.player = int(self.n.getP())
        print("You are player", self.player)

    def render_text(self, font, text, position, color=(0, 255, 255)):
        rendered_text = font.render(text, 1, color)
        self.win.blit(rendered_text, position)

    def render_moves(self, font, game):
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            self.render_text(font, move1, (100, 350), (0, 0, 0))
            self.render_text(font, move2, (400, 350), (0, 0, 0))
        else:
            text1 = move1 if game.p1Went and self.player == 0 else "Locked In" if game.p1Went else "Waiting..."
            text2 = move2 if game.p2Went and self.player == 1 else "Locked In" if game.p2Went else "Waiting..."
            if self.player == 1:
                self.render_text(font, text2, (100, 350), (0, 0, 0))
                self.render_text(font, text1, (400, 350), (0, 0, 0))
            else:
                self.render_text(font, text1, (100, 350), (0, 0, 0))
                self.render_text(font, text2, (400, 350), (0, 0, 0))

    def redraw_window(self, game):
        self.win.fill((128, 128, 128))

        if not game.connected():
            font = pygame.font.SysFont("comicsans", 80)
            self.render_text(font, "Waiting for Player...", (self.width / 2, self.height / 2), (255, 0, 0))
        else:
            font = pygame.font.SysFont("comicsans", 60)
            self.render_text(font, "Your Move", (80, 200))
            self.render_text(font, "Opponents", (380, 200))
            self.render_moves(font, game)

            for btn in self.btns:
                btn.draw(self.win)

        pygame.display.update()
    def handle_game_result(self, game):
        font = pygame.font.SysFont("comicsans", 90)
        if (game.winner() == 1 and self.player == 1) or (game.winner() == 0 and self.player == 0):
            text = font.render("You Won!", 1, (255, 0, 0))
        elif game.winner() == -1:
            text = font.render("Tie Game!", 1, (255, 0, 0))
        else:
            text = font.render("You Lost...", 1, (255, 0, 0))

        self.win.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(2000)

    def handle_mouse_button_down(self, pos, game):
        for btn in self.btns:
            if btn.click(pos) and game.connected():
                if self.player == 0:
                    if not game.p1Went:
                        self.n.send(btn.text)
                else:
                    if not game.p2Went:
                        self.n.send(btn.text)

    def main(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            try:
                game = self.n.send("get")
            except:
                run = False
                print("Couldn't get game")
                break

            if game.bothWent():
                self.redraw_window(game)
                pygame.time.delay(500)
                try:
                    game = self.n.send("reset")
                except:
                    run = False
                    print("Couldn't get game")
                    break

                self.handle_game_result(game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouse_button_down(pos, game)

            self.redraw_window(game)

    def menu_screen(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.win.fill((128, 128, 128))
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, (255, 0, 0))
            self.win.blit(text, (100, 200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        self.main()

if __name__ == "__main__":
    width, height = 600, 600
    game_client = Client()
    while True:
        game_client.menu_screen()
