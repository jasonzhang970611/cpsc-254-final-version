"""Gaming Test"""

from rules import FreeStyle
from settings import BLACK, WHITE
from controller import LocalGame

size = 15
players = {BLACK: "Doge", WHITE: "Meow"}
game = LocalGame(size, 600, players, FreeStyle())
game.start()
