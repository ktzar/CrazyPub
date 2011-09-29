import pygame
import random
import utils


class Client(pygame.sprite.Sprite):

    lanes_y     = [103, 198, 296, 391]
    lanes_x_ini = [120, 90, 60, 30]
    lanes_x_end = [300, 338, 370, 407]
    images      = ['client_1.png', 'client_2.png', 'client_3.png',  'client_4.png']
    WAITING     = 0
    DRINKING    = 1
    DRUNK       = 2
    num_clients = 0

    def __init__(self, bartending, lane):
        pygame.sprite.Sprite.__init__(self)
        print "New client in lane {0}".format(lane)
        self.num_client = Client.num_clients
        Client.num_clients += 1
        pic = random.randint(0,len(Client.images)-1)
        self.image, self.rect = utils.load_image(Client.images[pic])
        self.cur_lane   = lane
        self.rect.top   = Client.lanes_y[lane] -25 
        self.rect.left  = Client.lanes_x_ini[lane]
        self.speed = 1
        self.bartending = bartending
        self.age = 0
        self.state = Client.WAITING
        self.DRINKING_TIME = 100

    def update(self):
        if self.state == Client.WAITING:
            self.rect.left += self.speed
            if self.rect.left > Client.lanes_x_end[self.cur_lane]:
                self.bartending.client_gone()
        if self.state == Client.DRINKING:
            self.age += 1
            if self.age > self.DRINKING_TIME:
                self.bartending.return_beer(self)
                #self.state = Client.DRUNK

    def start_drinking(self):
        self.state = Client.DRINKING

class Bartender(pygame.sprite.Sprite):

    positions = [\
        {'x':330,'y':90},\
        {'x':358,'y':190},\
        {'x':400,'y':290},\
        {'x':427,'y':390}\
    ]
    STILL = 0
    MOVING = 1
    MOVING2 = 2

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_still, self.rect = utils.load_image('tender.png')
        self.image_moving, foo = utils.load_image('tender_moving.png')
        self.cur_lane = 0
        self.num_lanes = 4
        self.state = Bartender.STILL

    def update(self):
        if self.state == Bartender.MOVING:
            self.image = self.image_moving
            self.rect.top   = (self.rect.top + Bartender.positions[self.cur_lane]['y'])/2
            self.rect.left  = (self.rect.left + Bartender.positions[self.cur_lane]['x'])/2
            self.state = Bartender.MOVING2
        elif self.state == Bartender.MOVING2:
            self.image = self.image_moving
            self.state = Bartender.STILL
        else:
            self.image = self.image_still
            self.rect.top   = Bartender.positions[self.cur_lane]['y']
            self.rect.left  = Bartender.positions[self.cur_lane]['x']

    def move_down(self):
        if self.cur_lane < self.num_lanes-1:
            self.cur_lane += 1
            self.state = Bartender.MOVING

    def move_up(self):
        if self.cur_lane > 0:
            self.cur_lane -= 1
            self.state = Bartender.MOVING


class Beer(pygame.sprite.Sprite):

    lane_init = [120, 90, 60, 30]

    def __init__(self, bartending, position, lane):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('beer.png')
        self.rect.top = position.top
        self.rect.left = position.left
        self.lane = lane
        self.bartending = bartending
        self.speed = 5

    def update(self):
        self.rect = self.rect.move((-self.speed,0))
        if self.rect.left < Beer.lane_init[self.lane]:
            self.bartending.break_beer()
            self.kill()

class EmptyBeer(pygame.sprite.Sprite):

    lanes_y     = [105, 200, 295, 393]
    lanes_x_end = [300, 338, 370, 407]
    
    def __init__(self, bartending, position, cur_lane):
        pygame.sprite.Sprite.__init__(self)
        self.bartending = bartending
        self.image, self.rect = utils.load_image('beer_empty.png')
        self.cur_lane = cur_lane
        self.rect.left = position.left
        self.rect.top = EmptyBeer.lanes_y[self.cur_lane]
        self.speed = 2
        
    def kill(self):
        pygame.sprite.Sprite.kill(self)
        
    def update(self):
        self.rect = self.rect.move((self.speed,0))
        self.bartending
        if self.rect.left > EmptyBeer.lanes_x_end[self.cur_lane]:
            self.bartending.emptybeer_arrived(self)

