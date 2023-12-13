import pygame

class Button:
    """
    A class to represent a button in a pygame window.

    ...

    Attributes
    ----------
    text : str
        the text to be displayed on the button
    x : int
        the x-coordinate of the button
    y : int
        the y-coordinate of the button
    color : tuple
        the color of the button (R, G, B)
    width : int
        the width of the button
    height : int
        the height of the button
    font : pygame.font.Font
        the font of the text
    rect : pygame.Rect
        the rectangle representing the button

    Methods
    -------
    draw(win):
        Draws the button on the window.
    _draw_text(win):
        Draws the text on the button.
    click(pos):
        Checks if the button is clicked.
    """

    def __init__(self, text, x, y, color, width=150, height=100, font_size=40):
        """
        Constructs all the necessary attributes for the button object.

        Parameters
        ----------
            text : str
                the text to be displayed on the button
            x : int
                the x-coordinate of the button
            y : int
                the y-coordinate of the button
            color : tuple
                the color of the button (R, G, B)
            width : int, optional
                the width of the button (default is 150)
            height : int, optional
                the height of the button (default is 100)
            font_size : int, optional
                the font size of the text (default is 40)
        """

        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", font_size)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, win):
        """
        Draws the button on the window.

        Parameters
        ----------
            win : pygame.Surface
                the window on which to draw the button
        """

        pygame.draw.rect(win, self.color, self.rect)
        self._draw_text(win)

    def _draw_text(self, win):
        """
        Draws the text on the button.

        Parameters
        ----------
            win : pygame.Surface
                the window on which to draw the text
        """

        text = self.font.render(self.text, 1, (255,255,255))
        centered_x = self.x + round(self.width/2) - round(text.get_width()/2)
        centered_y = self.y + round(self.height/2) - round(text.get_height()/2)
        win.blit(text, (centered_x, centered_y))

    def click(self, pos):
        """
        Checks if the button is clicked.

        Parameters
        ----------
            pos : tuple
                the position of the mouse click

        Returns
        -------
            bool
                True if the button is clicked, False otherwise
        """

        return self.rect.collidepoint(pos)
