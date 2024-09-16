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
from battleship.board import Ship

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MIDDLE = pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

num_ships = None
game_over = False

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

def draw_board(screen, board):
    # TODO
    my_font = pg.font.Font(pg.font.get_default_font(), 36)
    x_offset = 0
    GRID_SIZE = 10
    MARGIN = 50
    CELL_SIZE = 40
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pg.Rect(x_offset + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, (0, 0, 0), rect, 1)
            if board.gameBoard[y][x] == -1: #-1 on the grid indicates a miss
                pg.draw.circle(screen, (0,0,255), rect.center, CELL_SIZE // 4)
            elif board.gameBoard[y][x] == -2: #-2 on the grid indicates a hit
                pg.draw.circle(screen, (255, 0, 0), rect.center, CELL_SIZE // 4)
            #elif isinstance(board.grid[y][x], Ship) and not hide_ships:
                #pg.draw.rect(screen, GRAY, rect)


def start_game(screen, background, clock):
    globals().update(game_over=False)

    running = True
    startBtn = ClickableButton("Start", (250, 100), (MIDDLE.x - 125, MIDDLE.y + 200))

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                return False
        
        background.fill("grey")
        screen.fill("grey")

        img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
        img.convert()
        img_size = img.get_size()
        background.blit(img, (MIDDLE.x - img_size[0]/2, 100))

        if not startBtn.clicked:
            startBtn.draw(background, events)
            startBtn.btn.show()
            startBtn.btn.enable()
        else:
            running = False
            # make start button is disabled
            startBtn.btn.hide()
            startBtn.btn.disable()


        screen.blit(background, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()

        tick = clock.tick(60) # limits FPS to 60

    return True

def choose_gamemode(screen, background, clock):
    running = True
    def txtCb(txt):
        text = ''.join(txt)
        match = re.match("[1-5]", text)
        print(f"num ships: {match[0]}")
        if match:
            globals().update(num_ships=match[0])

    shipTxtbox = TextBox(background, MIDDLE.x - 30, MIDDLE.y + 200, 60, 80, fontSize=50, onSubmit=txtCb)
    shipTxtbox.onSubmitParams = [shipTxtbox.text]

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                return False
        
        background.fill("grey")
        screen.fill("grey")

        if not num_ships:
            img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
            img.convert()
            img_size = img.get_size()
            background.blit(img, (MIDDLE.x - img_size[0]/2, 100))

            my_font = pg.font.Font(pg.font.get_default_font(), 36)
            text_surface = my_font.render('Choose number of ships [1-5]', False, (0, 0, 0))
            background.blit(text_surface, (MIDDLE.x - text_surface.get_width()/2, MIDDLE.y + 150))

            shipTxtbox.draw()
            shipTxtbox.show()
            shipTxtbox.enable()
        else:
            shipTxtbox.hide()
            shipTxtbox.disable()

        screen.blit(background, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()

        tick = clock.tick(60) # limits FPS to 60

def player1_place_ships():
    # TODO
    """
    Outline for the rest of functionality
    Place Ship object
    Confirm placement
    Change screen to a blank screen with a button that says
    'Player two press to start turn'
    Swithces to Player 2 start state when clicked
    """
    pass

def player2_place_ships():
    """
    Copy of Player 1 start
    Except confirmation sends the start to player 1 start
    """
    pass

def transition_between_turns(screen, background, clock):
    """
    Display whose turn it is, then wait until the enter
    button is pushed for confirmation to show that players
    attack/self board
    """
    pass

def player1_turn():
    pass

def player2_turn():
    pass

def run():
    # pygame setup
    pg.init()
    # set screen size
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Battleship")

    screen.fill("grey")
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill("grey")
    screen.blit(background, (0,0))
    pg.display.update()

    clock = pg.time.Clock() # keep to limit framerate
    running = True # track if loop should keep running

    player1_board = Board() # Initializes both players boards
    player2_board = Board()

    if not start_game(screen, background, clock):
        return

    if not choose_gamemode(screen, background, clock):
        return
    
    draw_board(screen,player1_board) #Temporary call, not sure if this is where it should be but it isn't printing anywhere atm

    # placeholder loop until all other states are finished
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        background.fill("grey")
        screen.fill("grey")
        screen.blit(background, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()

        tick = clock.tick(60) # limits FPS to 60
    
    global game_over
    globals().update(game_over=True)
    while not game_over:
        transition_between_turns()
        player1_turn()
        if game_over:
            break

        transition_between_turns()
        player2_turn()
        if game_over:
            break

    # boardGrid = Board()
    # ships = []
    # #these lines draw boxes for testing mouse movement --> either replace w/ ship object or delete
    # for i in range(5):
    #     ship = Ship(i + 1)
    #     #ship = pg.Rect(50 + i*40, 40, 30, 20)
    #     ships.append(ship)
    # active_ship = None

    # while running:
    #     # poll for events
    #     # pg.QUIT event means the user clicked X to close the window
    #     events = pg.event.get()
    #     for event in events:
    #         #mouse movement
    #         '''ROTATION IS STILL WONKY, NEEDS TO BE TWEAKED'''
    #         if event.type == pg.MOUSEBUTTONDOWN: #if mouse clicked
    #             for num, ship in enumerate(ships): #track index # of ships
    #                 if ship.collidepoint(event.pos): #checks for collision w/ mouse coords
    #                     active_ship = num #if collide, update active_ship w/ ship's index val
    #                     '''if keys[pg.K_r]: #if r key pressed while dragging
    #                         ships[active_ship].rotate90() #rotate ship'''
    #                     break

    #         if event.type == pg.MOUSEMOTION and active_ship != None: #if mouse moved and there is active ship
    #             ships[active_ship].move(event.rel) #pick ship from list and move it by same amount as mouse
    #             if keys[pg.K_r]: #if r key pressed while dragging
    #                         print("r pressed") #debugging
    #                         ships[active_ship].rotate90() #rotate ship

    #         if event.type == pg.MOUSEBUTTONUP: #if mouse released
    #             if active_ship is not None: #if ship active
    #                 active_ship = None #releases ship
    #                 break
            
    #     if game_state == State.PLAYER1START:
    #         size = 500
    #         boardGrid.draw(background, middle.x - size/2, middle.y - size/2, size)

    #         my_font = pg.font.Font(pg.font.get_default_font(), 56)
    #         text_surface = my_font.render('PLAYER 1, PLACE SHIPS', False, (0, 0, 0))
    #         background.blit(text_surface, (middle.x - text_surface.get_width()/2, 30))

    #         #draw boxes ----> will have to replace w/ ship object       
    #         for ship in ships:
    #             #pg.draw.rect(background, "purple", ship)
    #             if ships.index(ship) == active_ship:
    #                 pg.draw.rect(background, "red", ship.rect.inflate(10, 10), 2)  # Draw a red outline on the ship player is actively moving
    #             ship.draw(background)
        
    #     if game_state == State.PLAYER1TURN:
    #         pass
    #         '''
    #         Look at hits on their board
    #         Moves to attack phase and confirms hits
    #         Check victory condition
    #         on miss switch to transition screen
    #         switch to player 2 turn
    #         '''

    #     if game_state == State.PLAYER2TURN:
    #         pass
    #         '''
    #         Look at hits on their board
    #         Moves to attack phase and confirms hits
    #         Check victory condition
    #         on miss switch to transition screen
    #         switch to player 1 turn
    #         '''

    pg.quit()

def main():
    # run main loop
    run()

if __name__ == "__main__":
    main()
