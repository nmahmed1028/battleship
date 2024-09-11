import pygame_widgets
import pygame as pg

# Should be a widget (draws a board)
# Stores an array
# and has function addShip() that adds to that array
# should also have function to lookup if coordinate has ship on it
# Doesnt need to know gamemode (1-5 ships)

# 0 for empty
# 1 for miss
# x for hit
# Ship class for ship
EMPTY_ROW = [0 for i in range(10)]

class Ship:
    def __init__(self, size) -> None:
        self.x = 1
        self.y = size # number 1-5 s.t. the ship is 1x(size)

    def rotate90(self):
        y = self.y
        self.y = self.x
        self.x = y

# Will have to be able to support a ship board or a attack board
class Board:
    def __init__(self) -> None:
        # always 10x10
        self.gameBoard = [EMPTY_ROW for i in range(10)]

    def draw(self, screen, x, y):
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200)

        # given x is left
        # given y is top
        BOARD_WIDTH = 200
        BOARD_HEIGHT = 200
        blockSize = int(BOARD_WIDTH / 10) # Set the size of the grid block
        x = int(x)
        y = int(y)

        for xDraw in range(x, x + BOARD_WIDTH, blockSize):
            for yDraw in range(y, y + BOARD_HEIGHT, blockSize):
                rect = pg.Rect(xDraw, yDraw, blockSize, blockSize)
                pg.draw.rect(screen, BLACK, rect, 1)

    def addToBoard(self, ship=Ship):
        print("drawing ship")
        pass

    def addToBoard(self, x=int):
        print("drawing int")
        pass

    def addToBoard(self, z=str):
        print("drawing str")
        pass