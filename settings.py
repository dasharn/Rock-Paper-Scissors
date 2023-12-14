from enum import Enum

class Settings(Enum):
    """
    Enum class for general game settings.

    Attributes
    ----------
    WIDTH : int
        The width of the game window.
    HEIGHT : int
        The height of the game window.
    CAPTION : str
        The caption of the game window.
    """
    WIDTH = 700
    HEIGHT = 700
    CAPTION = "Client"

class ButtonSettings(Enum):
    """
    Enum class for button settings.

    Attributes
    ----------
    ROCK : dict
        The settings for the "Rock" button.
    SCISSORS : dict
        The settings for the "Scissors" button.
    PAPER : dict
        The settings for the "Paper" button.
    FONT : str
        The font of the button text.
    FONT_SIZE : int
        The size of the button text.
    """
    ROCK = {"text": "Rock", "x": 50, "y": 500, "color": (0,0,0)}
    SCISSORS = {"text": "Scissors", "x": 250, "y": 500, "color": (255,0,0)}
    PAPER = {"text": "Paper", "x": 450, "y": 500, "color": (0,255,0)}
    FONT = "comicsans"
    FONT_SIZE = 60