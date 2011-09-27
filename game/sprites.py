import pygame
import random
import utils


class Client(pygame.sprite.Sprite):

    lanes_y     = [105, 200, 295, 393]
    lanes_x_ini = [120, 90, 60, 30]
    lanes_x_end = [300, 338, 370, 407]
    images = ['client_0.png', 'client_1.png', 'client_2.png']

    def __init__(self, bartending, lane):
        pygame.sprite.Sprite.__init__(self)
        pic = random.randint(0,len(Client.images)-1)
        self.image, self.rect = utils.load_image(Client.images[pic])
        self.cur_lane   = lane
        self.rect.top   = Client.lanes_y[lane] -25 
        self.rect.left  = Client.lanes_x_ini[lane]
        self.speed = 1
        self.bartending = bartending

    def update(self):
        self.rect.left  += self.speed
        if self.rect.left > Client.lanes_x_end[self.cur_lane]:
            self.bartending.client_gone()


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
        self.speed = 1

    def update(self):
        self.rect = self.rect.move((-self.speed,0))
        if self.rect.left < Beer.lane_init[self.lane]:
            self.bartending.break_beer()
            self.kill()


