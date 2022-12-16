from .objects import Player1, Player2, Ball
from .window import Window

import pygame

# a manager for the scene
class SceneManager(object):
    def __init__(self):
        self.go_to(Menu())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


# check for errors
class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class Menu(Scene):
    def __init__(self):
        super().__init__()
        pygame.font.init()

        # sets fonts for the title and subtitle
        self.font = pygame.font.SysFont("Baskerville", 72)
        self.font1 = pygame.font.SysFont("Baskerville", 32)
        self.font2 = pygame.font.SysFont("PT Sans Caption", 36)
        self.font3 = pygame.font.SysFont("Baskerville", 12)

    # makes the main menu
    def render(self, screen):
        screen.fill(pygame.Color("green4"))
        title = self.font.render("Pong", True, (pygame.Color("oldlace")))
        title2 = self.font1.render(
            "A game made with classes", True, (pygame.Color("oldlace"))
        )
        subtitle = self.font2.render(
            'To begin, press "enter"', True, (pygame.Color("oldlace"))
        )
        credits = self.font3.render(
            "Bryan Welton © Dec 2022", True, pygame.Color("lightyellow1")
        )
        screen.blit(title, (40, 115))
        screen.blit(title2, (40, 200))
        screen.blit(subtitle, (40, 425))
        screen.blit(credits, (640, 560))

    def update(self):
        pass

    # handles the events for the screen or it'll crash
    def handle_events(self, events):
        for i in events:
            if i.type == pygame.KEYDOWN and (
                i.key == pygame.K_SPACE or i.key == pygame.K_RETURN
            ):
                self.manager.go_to(GameScene())


class GameScene(Scene):

    # initialize the class
    def __init__(self):
        super().__init__()
        pygame.font.init()
        # calls player classes
        self.player1 = Player1()
        self.player2 = Player2()

        # makes places for the score to be displayed
        self.points = {"player1": 0, "player2": 0}
        self.font = pygame.font.SysFont("Baskerville", 30)
        self.player1_score = self.font.render(
            str(self.points["player1"]), 1, pygame.Color("oldlace")
        )
        self.player2_score = self.font.render(
            str(self.points["player2"]), 1, pygame.Color("oldlace")
        )
        self.ball = Ball()

    # handles the events for the screen or it'll crash
    def handle_events(self, events):
        for i in events:
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                pass

    def render(self, screen):

        # renders the scores
        screen.blit(self.player1_score, (150, 550))
        screen.blit(self.player2_score, (630, 550))
        pygame.draw.rect(screen, pygame.Color("oldlace"), self.player1)
        pygame.draw.rect(screen, pygame.Color("oldlace"), self.player2)
        pygame.draw.rect(screen, pygame.Color("red1"), self.ball)

    def update(self):

        # detects when a key has been pushed
        pressed = pygame.key.get_pressed()

        # player 1 keys = up and down arrow
        up, down = [pressed[key] for key in (pygame.K_UP, pygame.K_DOWN)]

        # player 2 keys = w and s
        key_w, key_s = [pressed[key] for key in (pygame.K_w, pygame.K_s)]
        self.handle_point()
        self.player1.update(key_w, key_s)
        self.player2.update(up, down)
        self.ball.update(self.player1, self.player2)

    # handles the scoring
    def handle_point(self):
        def update_points(key):
            self.points[key] += 1
            self.player1_score = self.font.render(
                str(self.points["player1"]), 1, pygame.Color("oldlace")
            )
            self.player2_score = self.font.render(
                str(self.points["player2"]), 1, pygame.Color("oldlace")
            )

        # detects which side the ball goes into, and then resets the ball
        if self.ball.x <= self.ball.width:
            update_points("player2")
            self.ball.reset()
        if self.ball.x >= (Window.win_width + self.ball.width):
            update_points("player1")
            self.ball.reset()
            self.ball.dir_x *= -1
