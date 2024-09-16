# import platform
import time
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
MIDDLE = pg.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = pg.Surface(SCREEN.get_size()).convert()
CLOCK = pg.time.Clock() # keep to limit framerate

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

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

def draw_board(board, x_offset, y_offset):
    # TODO
    my_font = pg.font.Font(pg.font.get_default_font(), 36)
    GRID_SIZE = 10
    CELL_SIZE = 60
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pg.Rect(x_offset + x * CELL_SIZE, y_offset + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(BACKGROUND, (0, 0, 0), rect, 1)
            if board.gameBoard[y][x] == -1: #-1 on the grid indicates a miss
                pg.draw.circle(BACKGROUND, (0,0,255), rect.center, CELL_SIZE // 4)
            elif board.gameBoard[y][x] == -2: #-2 on the grid indicates a hit
                pg.draw.circle(BACKGROUND, (255, 0, 0), rect.center, CELL_SIZE // 4)
            #elif isinstance(board.grid[y][x], Ship) and not hide_ships:
                #pg.draw.rect(screen, GRAY, rect)
    SCREEN.blit(BACKGROUND, (0,0))


def start_game():
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
        
        BACKGROUND.fill("grey")
        SCREEN.fill("grey")

        img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
        img.convert()
        img_size = img.get_size()
        BACKGROUND.blit(img, (MIDDLE.x - img_size[0]/2, 100))

        if not startBtn.clicked:
            startBtn.draw(BACKGROUND, events)
            startBtn.btn.show()
            startBtn.btn.enable()
        else:
            running = False
            # make start button is disabled
            startBtn.btn.hide()
            startBtn.btn.disable()


        SCREEN.blit(BACKGROUND, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()

        tick = CLOCK.tick(60) # limits FPS to 60

    return True

def choose_gamemode():
    running = True
    def txtCb(txt):
        text = ''.join(txt)
        match = re.match("[1-5]", text)
        if match:
            print(f"num ships: {match[0]}")
            globals().update(num_ships=int(match[0]))

    shipTxtbox = TextBox(BACKGROUND, MIDDLE.x - 30, MIDDLE.y + 200, 60, 80, fontSize=50, onSubmit=txtCb)
    shipTxtbox.onSubmitParams = [shipTxtbox.text]

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                return False
        
        BACKGROUND.fill("grey")
        SCREEN.fill("grey")

        if not num_ships:
            img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
            img.convert()
            img_size = img.get_size()
            BACKGROUND.blit(img, (MIDDLE.x - img_size[0]/2, 100))

            my_font = pg.font.Font(pg.font.get_default_font(), 36)
            text_surface = my_font.render('Choose number of ships [1-5]', True, (0, 0, 0))
            BACKGROUND.blit(text_surface, (MIDDLE.x - text_surface.get_width()/2, MIDDLE.y + 150))

            shipTxtbox.draw()
            shipTxtbox.show()
            shipTxtbox.enable()
        else:
            running = False
            shipTxtbox.hide()
            shipTxtbox.disable()

        SCREEN.blit(BACKGROUND, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()

        tick = CLOCK.tick(60) # limits FPS to 60
    
    return True

def player_place_ships(screen, board, clock):
    """
    Outline for the rest of functionality
    Place Ship object
    Confirm placement
    Change screen to a blank screen with a button that says
    'Player two press to start turn'
    Swithces to Player 2 start state when clicked
    """
    ships = [Ship(i+1) for i in range(num_ships)]  # Add ship sizes based on your design
    font = pg.font.Font(None, 36)
    MARGIN = 50
    X_OFFSET = 360
    CELL_SIZE = 60
    GRID_SIZE = 10

    for ship in ships:
        placing = True
        horizontal = True

        while placing:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    return False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    print(f"({x}, {y})")
                    grid_x = (x - X_OFFSET) // CELL_SIZE
                    grid_y = (y - MARGIN) // CELL_SIZE
                    
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        print(f"({grid_x}, {grid_y})")
                        # if board.place_ship(ship, grid_x, grid_y, horizontal):
                        #     placing = False
                        # else:
                        #     print(f"Invalid placement at ({grid_x}, {grid_y}), horizontal: {horizontal}")
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        horizontal = not horizontal
            
            screen.fill("grey")
            draw_board(board, X_OFFSET, MARGIN)

            # Draw ship preview
            mouse_x, mouse_y = pg.mouse.get_pos()
            grid_x = (mouse_x) // CELL_SIZE
            grid_y = (mouse_y - MARGIN) // CELL_SIZE

            if 0 <= (mouse_x - X_OFFSET) // CELL_SIZE < GRID_SIZE and 0 <= (mouse_y - MARGIN) // CELL_SIZE < GRID_SIZE:
                can_place = True
                if horizontal:
                    if (mouse_x - X_OFFSET) // CELL_SIZE + ship.size > 10: #10 is the grid size
                        can_place = False
                    try:
                        for i in range(ship.size): 
                            if board.gameBoard[grid_y][grid_x + i] != 0:
                                can_place=False
                    except:
                        can_place = False
                else:
                    if grid_y + ship.size > 10: # 10 is the grid size
                        can_place=False
                    try:
                        for i in range(ship.size):
                            if board.gameBoard[grid_y + i][grid_x] != 0:
                                can_place=False
                    except:
                        can_place = False
                preview_color = "green" if can_place else "red"
                if horizontal:
                    pg.draw.rect(screen, preview_color, (grid_x * CELL_SIZE, MARGIN + grid_y * CELL_SIZE, ship.size * CELL_SIZE, CELL_SIZE), 2)
                else:
                    pg.draw.rect(screen, preview_color, (grid_x * CELL_SIZE, MARGIN + grid_y * CELL_SIZE, CELL_SIZE, ship.size * CELL_SIZE), 2)

            # Draw instructions
            text = font.render(f"Place your ship of size {ship.size}. Press SPACE to rotate.", True, "white")
            screen.blit(text, (10, 10))
            
            pg.display.flip()

def transition_between_turns(pnum):
    """
    Display whose turn it is, then wait until the enter
    button is pushed for confirmation to show that players
    attack/self board
    """
    hold = True
    while hold:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return

        font = pg.font.Font(pg.font.get_default_font(), 48)
        SCREEN.fill("grey")
        BACKGROUND.fill("grey")
        text = font.render(f"Player {pnum}'s Turn Press Enter to continue", True, "white")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        BACKGROUND.blit(text, text_rect)
        SCREEN.blit(BACKGROUND, (0,0))

        events = pg.event.get()
        pw.update(events)  # Call once every loop to allow widgets to render and listen

        pg.display.flip()

def player1_turn():
    '''
    Look at hits on their board
    Moves to attack phase and confirms hits
    Check victory condition
    on miss switch to transition screen
    switch to player 2 turn
    '''
    pass

def player2_turn():
    '''
    Look at hits on their board
    Moves to attack phase and confirms hits
    Check victory condition
    on miss switch to transition screen
    switch to player 1 turn
    '''
    pass

def receive_attack(self, x, y):
    if self.gameBoard[y][x] == 0:
        self.gameBoard[y][x] = -1  # Miss
        return False
    elif isinstance(self.grid[y][x], Ship):
        ship = self.gameBoard[y][x]
        ship.hits += 1
        self.gameBoard[y][x] = -2  # Hit
        return True
    return False

def receive_attack(self, x, y):
    if self.gameBoard[y][x] == 0:
        self.gameBoard[y][x] = -1  # Miss
        return False
    elif isinstance(self.grid[y][x], Ship):
        ship = self.gameBoard[y][x]
        ship.hits += 1
        self.gameBoard[y][x] = -2  # Hit
        return True
    return False

def display_attack_result(attacking_player, hit):
    font = pg.font.Font(None, 36)
    if hit:
        text = font.render("Hit!", True, RED)
    else:
        text = font.render("Miss!", True, BLUE)
    text_rect = text.get_rect(center=(x, y))
    SCREEN.blit(text, text_rect)
    pg.display.flip()
    time.sleep(1.5)  # Display the result for 1.5 seconds

def run():
    # pygame setup
    pg.init()
    # set screen size
    pg.display.set_caption("Battleship")

    SCREEN.fill("grey")
    BACKGROUND.fill("grey")
    SCREEN.blit(BACKGROUND, (0,0))
    pg.display.update()

    running = True # track if loop should keep running

    player1_board = Board() # Initializes both players boards
    player2_board = Board()

    if not start_game():
        return -1

    if not choose_gamemode():
        return -1

    # draw_board(screen,player1_board) #Temporary call, not sure if this is where it should be but it isn't printing anywhere atm
    transition_between_turns(3) #Test Call last number is the player who's turn is next
    player_place_ships(SCREEN, player1_board, CLOCK)

    # placeholder loop until all other states are finished
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()

        tick = CLOCK.tick(60) # limits FPS to 60
        # player1_place_ships(SCREEN,player1_board,CLOCK)

    global game_over
    globals().update(game_over=True)
    while not game_over:
        player_place_ships(SCREEN, player1_board, CLOCK)
        transition_between_turns(1)
        player1_turn()
        #display_attack_result(1)
        if game_over:
            break

        transition_between_turns(2)
        player2_turn()
        #display_attack_result(2)
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
    #         boardGrid.draw(BACKGROUND, middle.x - size/2, middle.y - size/2, size)

    #         my_font = pg.font.Font(pg.font.get_default_font(), 56)
    #         text_surface = my_font.render('PLAYER 1, PLACE SHIPS', False, (0, 0, 0))
    #         BACKGROUND.blit(text_surface, (middle.x - text_surface.get_width()/2, 30))

    #         #draw boxes ----> will have to replace w/ ship object       
    #         for ship in ships:
    #             #pg.draw.rect(BACKGROUND, "purple", ship)
    #             if ships.index(ship) == active_ship:
    #                 pg.draw.rect(BACKGROUND, "red", ship.rect.inflate(10, 10), 2)  # Draw a red outline on the ship player is actively moving
    #             ship.draw(BACKGROUND)

    pg.quit()
    return 0 # returned in good state

def main():
    # run main loop
    exit_state = run()
    print(f"Exited with state {exit_state}")

if __name__ == "__main__":
    main()
