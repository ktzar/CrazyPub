import pygame
import utils


class Bartender(pygame.sprite.Sprite):

    positions = [\
        {'x':330,'y':100},\
        {'x':358,'y':200},\
        {'x':400,'y':300},\
        {'x':427,'y':400}\
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('tender.png')
        self.cur_lane = 0
        self.num_lanes = 4

    def update(self):
        self.rect.top   = Bartender.positions[self.cur_lane]['y']
        self.rect.left  = Bartender.positions[self.cur_lane]['x']

    def move_down(self):
        if self.cur_lane < self.num_lanes-1:
            self.cur_lane += 1

    def move_up(self):
        if self.cur_lane > 0:
            self.cur_lane -= 1


class Beer(pygame.sprite.Sprite):

    lane_init = [120, 90, 60, 30]

    def __init__(self, bartending, position, lane):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('beer.png')
        self.rect.top = position.top
        self.rect.left = position.left
        self.lane = lane
        self.bartending = bartending

    def update(self):
        self.rect = self.rect.move((-2,0))
        if self.rect.left < Beer.lane_init[self.lane]:
            self.bartending.break_beer()
            self.kill()


