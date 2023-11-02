from pico2d import *
import game_framework

import game_world
from grass import Grass
from boy import Boy
from Bird import Bird
import random

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global grass
    global boy
    global Bird

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    bird_10 = [Bird(random.randint(100, 1500), random.randint(300, 500)) for _ in range (10)]
    for i in range(10):
        game_world.add_object(bird_10[i], 1)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # delay(0.5)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

