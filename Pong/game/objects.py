from .window import Window
from math import cos, sin, radians

import pygame

# player 1 info
class Player1(pygame.Rect):
    def __init__(self):
        super().__init__(20, 225, 20, 150)
        self.velocity = 3.5

    # updates paddle and ball positions
    def update(self, up, down):
        if up and self.y >= 10:
            self.y -= self.velocity
        if down and self.y <= Window.win_height - (self.height + 10):
            self.y += self.velocity


# player 2 info
class Player2(pygame.Rect):
    def __init__(self):
        super().__init__(760, 225, 20, 150)
        self.velocity = 3.5

    # updates paddle and ball positions
    def update(self, up, down):
        if up and self.y >= 10:
            self.y -= self.velocity
        if down and self.y <= Window.win_height - (self.height + 10):
            self.y += self.velocity


class Ball(pygame.Rect):
    # default info, lots of math
    def __init__(self):
        super().__init__(400, 300, 20, 20)
        self.velocity = 3.5
        self.angle = radians(0)
        self.dir_x = cos(self.angle)
        self.dir_y = -sin(self.angle)

    # this is for when the ball resets after scoring
    def reset(self):
        # middle of screen
        self.x = Window.win_width / 2
        self.y = Window.win_height / 2

        # resets the angle so it goes horizontal
        self.angle = radians(0)
        self.dir_x = cos(self.angle)
        self.dir_y = -sin(self.angle)

    # this handles the ball moving
    def update(self, player1, player2):
        self.x += self.dir_x * self.velocity
        self.y += self.dir_y * self.velocity

        # checks for if the ball hits boundaries or paddles
        self.handle_bound_collision()
        self.handle_paddle_collision(player1, player2)

    # checks if the ball collides with the edges of the screen (with some padding)
    def handle_bound_collision(self):
        if self.y <= 0 or self.y >= Window.win_height - 10:
            self.dir_y *= -1.05

    # checks if the ball hits a paddle and bounces the ball at an angle relative to which half it bounces on
    def handle_paddle_collision(self, player1, player2):
        intersect_y = self.y

        if self.colliderect(player1):
            relative_intersect_y = (player1.y + (player1.height / 2)) - intersect_y
            normalized_relative_intersect_y = relative_intersect_y / (
                player1.height / 2
            )
            self.angle = radians(normalized_relative_intersect_y * 60)
            self.dir_x = cos(self.angle)
            self.dir_y = -sin(self.angle)

        if self.colliderect(player2):
            relative_intersect_y = (player2.y + (player2.height / 2)) - intersect_y
            normalized_relative_intersect_y = relative_intersect_y / (
                player2.height / 2
            )
            self.angle = radians(normalized_relative_intersect_y * 60)
            self.dir_x = -cos(self.angle)
            self.dir_y = sin(self.angle)
