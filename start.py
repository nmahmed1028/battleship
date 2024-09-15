import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship")

class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0
        self.positions = []

    def is_sunk(self):
        return self.hits == self.size

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []

    def place_ship(self, ship, x, y, horizontal):
        if horizontal:
            if x + ship.size > GRID_SIZE:
                return False
            for i in range(ship.size):
                if self.grid[y][x + i] != 0:
                    return False
            for i in range(ship.size):
                self.grid[y][x + i] = ship
                ship.positions.append((x + i, y))
        else:
            if y + ship.size > GRID_SIZE:
                return False
            for i in range(ship.size):
                if self.grid[y + i][x] != 0:
                    return False
            for i in range(ship.size):
                self.grid[y + i][x] = ship
                ship.positions.append((x, y + i))
        self.ships.append(ship)
        return True

    def receive_attack(self, x, y):
        if self.grid[y][x] == 0:
            self.grid[y][x] = -1  # Miss
            return False
        elif isinstance(self.grid[y][x], Ship):
            ship = self.grid[y][x]
            ship.hits += 1
            self.grid[y][x] = -2  # Hit
            return True
        return False

def draw_board(board, x_offset, hide_ships=False):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x_offset + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if board.grid[y][x] == -1:
                pygame.draw.circle(screen, BLUE, rect.center, CELL_SIZE // 4)
            elif board.grid[y][x] == -2:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
            elif isinstance(board.grid[y][x], Ship) and not hide_ships:
                pygame.draw.rect(screen, GRAY, rect)

def player_place_ships(board, ships):
    font = pygame.font.Font(None, 36)
    
    for ship in ships:
        placing = True
        horizontal = True
        
        while placing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // CELL_SIZE
                    grid_y = (y - MARGIN) // CELL_SIZE
                    
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        if board.place_ship(ship, grid_x, grid_y, horizontal):
                            placing = False
                        else:
                            print(f"Invalid placement at ({grid_x}, {grid_y}), horizontal: {horizontal}")
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        horizontal = not horizontal
            
            screen.fill(BLACK)
            draw_board(board, 0)
            
            # Draw ship preview
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // CELL_SIZE
            grid_y = (mouse_y - MARGIN) // CELL_SIZE
            
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                preview_ship = Ship(ship.size)
                can_place = board.place_ship(preview_ship, grid_x, grid_y, horizontal)
                preview_color = GREEN if can_place else RED
                if horizontal:
                    pygame.draw.rect(screen, preview_color, (grid_x * CELL_SIZE, MARGIN + grid_y * CELL_SIZE, ship.size * CELL_SIZE, CELL_SIZE), 2)
                else:
                    pygame.draw.rect(screen, preview_color, (grid_x * CELL_SIZE, MARGIN + grid_y * CELL_SIZE, CELL_SIZE, ship.size * CELL_SIZE), 2)
                
                # Remove the preview ship from the board
                if can_place:
                    board.ships.pop()
                    for pos in preview_ship.positions:
                        board.grid[pos[1]][pos[0]] = 0
            
            # Draw instructions
            text = font.render(f"Place your ship of size {ship.size}. Press SPACE to rotate.", True, WHITE)
            screen.blit(text, (10, 10))
            
            pygame.display.flip()
    
    return True

def ship_selection_screen():
    font = pygame.font.Font(None, 36)
    num_ships = 3  # Default number of ships
    
    running = True
    while running:
        screen.fill(BLACK)
        
        # Display current number of ships
        text = font.render(f"Number of ships: {num_ships}", True, WHITE)
        screen.blit(text, (300, 200))
        
        # Plus button
        pygame.draw.rect(screen, WHITE, (500, 200, 30, 30), 2)
        plus = font.render("+", True, WHITE)
        screen.blit(plus, (510, 205))
        
        # Minus button
        pygame.draw.rect(screen, WHITE, (550, 200, 30, 30), 2)
        minus = font.render("-", True, WHITE)
        screen.blit(minus, (560, 205))
        
        # Start game button
        pygame.draw.rect(screen, GREEN, (300, 300, 200, 50))
        start_text = font.render("Start Game", True, BLACK)
        screen.blit(start_text, (340, 315))
        
        # Display ship sizes
        ship_sizes_text = font.render(f"Ship sizes: {', '.join(str(i) for i in range(1, num_ships + 1))}", True, WHITE)
        screen.blit(ship_sizes_text, (300, 250))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 < x < 500 and 300 < y < 350:
                    return [Ship(i) for i in range(1, num_ships + 1)]
                elif 500 < x < 530 and 200 < y < 230:
                    num_ships = min(num_ships + 1, 5)
                elif 550 < x < 580 and 200 < y < 230:
                    num_ships = max(num_ships - 1, 1)

def transition_screen(player_number):
    font = pygame.font.Font(None, 48)
    screen.fill(BLACK)
    text = font.render(f"Player {player_number}'s Turn", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(2)  # Display the transition screen for 2 seconds

import pygame
import random
import time

# ... [Previous code remains unchanged up to the main() function]

def display_attack_result(screen, result, x, y):
    font = pygame.font.Font(None, 36)
    if result:
        text = font.render("Hit!", True, RED)
    else:
        text = font.render("Miss!", True, BLUE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1.5)  # Display the result for 1.5 seconds

def main():
    ships = ship_selection_screen()
    if not ships:
        return

    player1_board = Board()
    player2_board = Board()

    # Player 1 ship placement
    transition_screen(1)
    if not player_place_ships(player1_board, ships):
        return

    # Player 2 ship placement
    transition_screen(2)
    if not player_place_ships(player2_board, ships):
        return

    current_player = 1
    game_over = False

    while not game_over:
        transition_screen(current_player)
        attacking_board = player2_board if current_player == 1 else player1_board
        
        screen.fill(BLACK)
        draw_board(attacking_board, 0, hide_ships=True)
        pygame.display.flip()

        waiting_for_move = True
        while waiting_for_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // CELL_SIZE
                    grid_y = (y - MARGIN) // CELL_SIZE
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        hit = attacking_board.receive_attack(grid_x, grid_y)
                        screen.fill(BLACK)
                        draw_board(attacking_board, 0, hide_ships=True)
                        display_attack_result(screen, hit, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                        
                        if hit and all(ship.is_sunk() for ship in attacking_board.ships):
                            font = pygame.font.Font(None, 48)
                            win_text = font.render(f"Player {current_player} wins!", True, GREEN)
                            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                            screen.blit(win_text, win_rect)
                            pygame.display.flip()
                            time.sleep(3)  # Display win message for 3 seconds
                            game_over = True
                        waiting_for_move = False

        if not game_over:
            current_player = 3 - current_player  # Switch players (1 -> 2, 2 -> 1)

    pygame.quit()

if __name__ == "__main__":
    main()