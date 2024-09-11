# import platform
import pygame
# import class objects
import battleship

def run():
    # pygame setup
    pygame.init()
    # set screen size
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock() # keep to limit framerate
    running = True # track if loop should keep running
    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        pygame.draw.circle(screen, "red", player_pos, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        # flip() the display to put the work we did on screen
        pygame.display.flip()

        # limits FPS to 60
        tick = clock.tick(60)
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = tick / 1000

    pygame.quit()

def main():
    # run main loop
    run()

if __name__ == "__main__":
    main()
