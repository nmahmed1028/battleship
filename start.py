# import platform
import pygame as pg
import pygame_widgets as pw
# import class objects
from battleship.button import ClickableButton
from enum import Enum
import os

class State(Enum):
    START = 1

game_state = State(1)

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
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill("grey")

    pg.display.set_caption("Battleship")
    clock = pg.time.Clock() # keep to limit framerate
    running = True # track if loop should keep running

    middle = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    startBtn = ClickableButton("Start", (250, 100), (middle.x - 125, middle.y + 200))
    while running:
        # limits FPS to 60
        tick = clock.tick(60)

        # poll for events
        # pygame.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        background.fill("grey")

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
            # Put Text On The Background, Centered
            if pg.font:
                # img, rect = load_image("battleship_fontbolt.png")
                img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
                img.convert()
                img_size = img.get_size()
                background.blit(img, (middle.x - img_size[0]/2, 100))

            startBtn.draw(screen)

        screen.blit(background, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        pg.display.update()

        # flip() the display to put the work we did on screen
        pg.display.flip()

    pg.quit()

def main():
    # run main loop
    run()

if __name__ == "__main__":
    main()
