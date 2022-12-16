from __future__ import absolute_import
from game.window import Window
from game.scene import SceneManager

import pygame


def main():
    # makes the screen
    screen = pygame.display.set_mode((Window.win_width, Window.win_height))

    # makes a window title
    pygame.display.set_caption("Pong")

    # general game info
    clock = pygame.time.Clock()
    manager = SceneManager()
    running = True
    pygame.init()

    # runs the game
    while running:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color("darkgreen"))
        manager.scene.render(screen)
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        pygame.display.flip()

    # quit if not running (obviously)
    pygame.quit()


# gotta have it
if __name__ == "__main__":
    main()
