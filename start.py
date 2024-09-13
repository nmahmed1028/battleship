# import platform
import pygame as pg
import pygame_widgets as pw
from pygame_widgets.textbox import TextBox
# import class objects
from battleship.button import ClickableButton
from battleship.board import Board
from enum import Enum
import os
import re

class State(Enum):
    START = 1
    PICK_SHIPS = 2
    PLAYER1START = 3
    PLAYER2START = 4
    PLAYER1TURN = 5
    PLAYER2TURN = 6

game_state = State.START
num_ships = 1

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")
# functions to create our resources
def load_image(name, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    # size = image.get_size()
    # size = (size[0] * scale, size[1] * scale)
    # image = pg.transform.scale(image, size)

    return image, image.get_rect()

def run():
    # pygame setup
    pg.init()
    # set screen size
    screen = pg.display.set_mode((1280, 720))
    screen.fill("grey")
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill("grey")

    screen.blit(background, (0,0))
    pg.display.update()

    global game_state
    game_state = State.START
    global num_ships
    num_ships = 1

    pg.display.set_caption("Battleship")
    clock = pg.time.Clock() # keep to limit framerate
    running = True # track if loop should keep running

    middle = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    def cb(self):
        print("Start button cb")
        globals().update(game_state=State.PICK_SHIPS)
        del self
    startBtn = ClickableButton("Start", (250, 100), (middle.x - 125, middle.y + 200), cb)

    def txtCb(txt):
        text = ''.join(txt)
        match = re.match("[1-5]", text)
        print(f"num ships: {match[0]}")
        if match:
            globals().update(game_state=State.PLAYER1START)
            globals().update(num_ships=match[0])

    shipTxtbox = TextBox(background, middle.x - 30, middle.y + 200, 60, 80, fontSize=50, onSubmit=txtCb)
    shipTxtbox.onSubmitParams = [shipTxtbox.text]
    boardGrid = Board()
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        background.fill("grey")
        screen.fill("grey")

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            pass
        if keys[pg.K_s]:
            pass
        if keys[pg.K_a]:
            pass
        if keys[pg.K_d]:
            pass

        if game_state == State.START:
            # Put Img On The Background, Centered
            # img, rect = load_image("battleship_fontbolt.png")
            img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
            img.convert()
            img_size = img.get_size()
            background.blit(img, (middle.x - img_size[0]/2, 100))

            startBtn.draw(background, events)
            startBtn.btn.show()
            startBtn.btn.enable()
        else:
            # make start button is disabled
            startBtn.btn.hide()
            startBtn.btn.disable()

        if game_state == State.PICK_SHIPS:
            img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
            img.convert()
            img_size = img.get_size()
            background.blit(img, (middle.x - img_size[0]/2, 100))

            my_font = pg.font.Font(pg.font.get_default_font(), 36)
            text_surface = my_font.render('Choose number of ships [1-5]', False, (0, 0, 0))
            background.blit(text_surface, (middle.x - text_surface.get_width()/2, middle.y + 150))

            shipTxtbox.draw()
            shipTxtbox.show()
            shipTxtbox.enable()
        else:
            shipTxtbox.hide()
            shipTxtbox.disable()

        if game_state == State.PLAYER1START:
            size = 500
            boardGrid.draw(background, middle.x - size/2, middle.y - size/2, size)

            my_font = pg.font.Font(pg.font.get_default_font(), 56)
            text_surface = my_font.render('PLAYER 1, PLACE SHIPS', False, (0, 0, 0))
            background.blit(text_surface, (middle.x - text_surface.get_width()/2, 30))
        else:
            pass

        pw.update(events)  # Call once every loop to allow widgets to render and listen
        screen.blit(background, (0, 0))

        # flip() the display to put the work we did on screen
        pg.display.update()
        # pg.display.flip()

        # limits FPS to 60
        tick = clock.tick(60)

    pg.quit()

def main():
    # run main loop
    run()

if __name__ == "__main__":
    main()
