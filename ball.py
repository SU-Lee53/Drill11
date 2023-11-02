from pico2d import *
import game_world

# PIXEL_PER_METER = (10.0 / 0.3)
# BALL_SPEED_KMPH = 20.0   # km/h
# BALL_SPEED_MPM = (BALL_SPEED_KMPH * 1000 / 60)    # meter / minit
# BALL_SPEED_MPS = (BALL_SPEED_MPM / 60.0)  # meter / sec
# BALL_SPEED_PPS = (BALL_SPEED_MPS * PIXEL_PER_METER)   # pixel / sec

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

class BigBall:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if BigBall.image == None:
            BigBall.image = load_image('ball41x41.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
