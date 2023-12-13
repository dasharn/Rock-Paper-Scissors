import pygame
from network import Network
from button import Button

class Client:
    def __init__(self):
        pygame.font.init()
        self.width = 700
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Client")
        self.btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.win.blit(text_surface, (x - text_surface.get_width() / 2, y - text_surface.get_height() / 2))

    def redraw_window(self, game, p):
        self.win.fill((128,128,128))
        font_80 = pygame.font.SysFont("comicsans", 80)
        font_60 = pygame.font.SysFont("comicsans", 60)

        if not game.connected():
            self.draw_waiting_for_player(font_80)
        else:
            self.draw_game_state(game, p, font_60)

        pygame.display.update()

    def draw_waiting_for_player(self, font):
        self.draw_text("Waiting for Player...", font, (255,0,0), self.width/2, self.height/2)

    def draw_game_state(self, game, p, font):
        self.draw_text("Your Move", font, (0, 255,255), 80, 200)
        self.draw_text("Opponents", font, (0, 255,255), 380, 200)

        text1, text2 = self.get_player_texts(game, p)

        self.draw_text(text1, font, (0,0,0), 100, 350)
        self.draw_text(text2, font, (0,0,0), 400, 350)

        for btn in self.btns:
            btn.draw(self.win)

    def get_player_texts(self, game, p):
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for btn in self.btns:
                if btn.click(pos) and game.connected():
                    if player == 0 and not game.p1Went or player == 1 and not game.p2Went:
                        n.send(btn.text)
                        
    def update_game_state(self, n, action):
        try:
            game = n.send(action)
            return game
        except Exception as e:
            print(f"Couldn't get game: {e}")
            return None

    def main(self):
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
