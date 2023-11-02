# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'




# Bird Run Speed
# fill here
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 40.0   # km/h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000 / 60)    # meter / minit
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # meter / sec
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)   # pixel / sec

# Bird Action Speed
# fill here
TIME_PER_ACTION = 0.08 # 초당 80회(벌새의 날갯짓 속도)
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5









class Idle:

    @staticmethod
    def enter(Bird, e):
        if Bird.face_dir == -1:
            Bird.action = 2
        elif Bird.face_dir == 1:
            Bird.action = 3
        Bird.dir = 0
        Bird.frame = 0
        Bird.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(Bird, e):
        if space_down(e):
            Bird.fire_ball()
        pass

    @staticmethod
    def do(Bird):
        Bird.frame = (Bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - Bird.wait_time > 2:
            Bird.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(Bird):
        Bird.image.clip_draw(int(Bird.frame) * 100, Bird.action * 100, 100, 100, Bird.x, Bird.y)



class Run:

    @staticmethod
    def enter(Bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            Bird.dir, Bird.action, Bird.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            Bird.dir, Bird.action, Bird.face_dir = -1, 0, -1

    @staticmethod
    def exit(Bird, e):
        if space_down(e):
            Bird.fire_ball()

        pass

    @staticmethod
    def do(Bird):
        Bird.frame = (Bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        Bird.x += Bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        Bird.x = clamp(25, Bird.x, 1600-25)
        if(Bird.x <= 50 or Bird.y >= 1550):
            Bird.dir = 1 if Bird.dir == -1 else -1


    @staticmethod
    def draw(Bird):
        if Bird.dir == -1:
            Bird.image.clip_composite_draw(int(Bird.frame) * 185, 150, 180, 180, 0, 'v', Bird.x, Bird.y, Bird.size[0], Bird.size[1])
        else:
            Bird.image.clip_draw(int(Bird.frame) * 185, 150, 180, 180, Bird.x, Bird.y, Bird.size[0], Bird.size[1])



class Sleep:

    @staticmethod
    def enter(Bird, e):
        Bird.frame = 0
        pass

    @staticmethod
    def exit(Bird, e):
        pass

    @staticmethod
    def do(Bird):
        Bird.frame = (Bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8




    @staticmethod
    def draw(Bird):
        if Bird.face_dir == -1:
            Bird.image.clip_composite_draw(int(Bird.frame) * 100, 200, 100, 100,
                                          -3.141592 / 2, '', Bird.x + 25, Bird.y - 25, 100, 100)
        else:
            Bird.image.clip_composite_draw(int(Bird.frame) * 100, 300, 100, 100,
                                          3.141592 / 2, '', Bird.x - 25, Bird.y - 25, 100, 100)


class StateMachine:
    def __init__(self, Bird):
        self.Bird = Bird
        self.cur_state = Run
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run}
        }

    def start(self):
        self.cur_state.enter(self.Bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.Bird)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.Bird, e)
                self.cur_state = next_state
                self.cur_state.enter(self.Bird, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.Bird)
        # self.Bird.font.draw(self.Bird.x - 60, self.Bird.y + 50, f'(TIME: {get_time():.2f})', (255, 255, 0))




class Bird:
    def __init__(self, x = 400, y =90):
        self.x, self.y = x, y
        self.frame = random.randint(0, 5)
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.font = load_font('ENCR10B.TTF')
        self.size = (50, 50)


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(25, self.x, 1600 - 25)
        if (self.x <= 50 or self.x >= 1550):
            self.dir = 1 if self.dir == -1 else -1

    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 185, 150, 180, 180, 0, 'h', self.x, self.y, self.size[0], self.size[1])
        else:
            self.image.clip_draw(int(self.frame) * 185, 150, 180, 180, self.x, self.y, self.size[0], self.size[1])


    # Bird는 좌우로 날기만 하니까 상태머신 필요없을듯