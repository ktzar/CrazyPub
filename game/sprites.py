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
    sounds      = []

    def __init__(self, bartending, lane):
        pygame.sprite.Sprite.__init__(self)
        #Load the sounds if they are not loaded 
        #they will be load with the appeareance of the first client
        if len(Client.sounds) == 0:
            Client.sounds.append(utils.load_sound('shout_0.ogg'))
            Client.sounds.append(utils.load_sound('shout_1.ogg'))
            Client.sounds.append(utils.load_sound('shout_2.ogg'))
        #assign a random sound to the client
        shout = Client.sounds[random.randint(0,len(Client.sounds)-1)]
        shout.play()
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
        self.time_drinking = 0
        self.state = Client.WAITING
        self.drinking_time = 25

    def update(self):
        self.age += 1
        #client is waiting for a beer
        if self.state == Client.WAITING:
            #Advance "step by step"
            if self.age %30 > 10:
                self.rect.left += self.speed
            if self.rect.left > Client.lanes_x_end[self.cur_lane]:
                self.bartending.client_gone()
        #Client is drinking, wait drinking_time updates
        #and go back in the meantime. It the client reaches 
        #the beginning of the bar, kill it
        if self.state == Client.DRINKING:
            self.rect.left -= self.speed
            self.time_drinking += 1
            if self.rect.left < Client.lanes_x_ini[self.cur_lane]:
                self.kill()
            if self.time_drinking > self.drinking_time:
                self.bartending.return_beer(self)
                self.state = Client.WAITING
    #Start counting the time drinking and change the state
    def start_drinking(self):
        self.time_drinking = 0
        self.state = Client.DRINKING
        #every beer takes twice as much to get drank
        self.drinking_time *= 2

class Bartender(pygame.sprite.Sprite):
    #The x,y positions that the bartender can be after moving to a new bar
    positions = [\
        {'x':330,'y':90},\
        {'x':358,'y':190},\
        {'x':400,'y':290},\
        {'x':427,'y':390}\
    ]
    #Constants for animation states
    STILL       = 0
    MOVING      = 1
    MOVING2     = 2
    GOING_LEFT  = 3
    GOING_RIGHT = 4

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_still, self.rect = utils.load_image('tender.png')
        self.image_moving, foo = utils.load_image('tender_moving.png')
        self.cur_lane = 0
        self.num_lanes = 4
        self.state = Bartender.STILL
        #When the player goes left and right, the bartender goes "inside the bar"
        self.inside_bar = 0

    def update(self):
        #If in the middle of the movement, set the sprite in the middle and blurred
        if self.state == Bartender.MOVING:
            self.image = self.image_moving
            self.rect.top   = (self.rect.top + Bartender.positions[self.cur_lane]['y'])/2
            self.rect.left  = (self.rect.left + Bartender.positions[self.cur_lane]['x'])/2 - self.inside_bar
            self.state = Bartender.MOVING2
        elif self.state == Bartender.MOVING2:
            self.image = self.image_moving
            self.state = Bartender.STILL
        elif self.state == Bartender.GOING_RIGHT:
            if self.inside_bar > 0:
                self.inside_bar -= 2
            self.rect.left  = Bartender.positions[self.cur_lane]['x'] - self.inside_bar
        elif self.state == Bartender.GOING_LEFT:
            if self.inside_bar < 200:
                self.inside_bar += 2
            self.rect.left  = Bartender.positions[self.cur_lane]['x'] - self.inside_bar
        else:
            self.image = self.image_still
            self.rect.top   = Bartender.positions[self.cur_lane]['y']
            self.rect.left  = Bartender.positions[self.cur_lane]['x'] - self.inside_bar

    def no_move_left(self):
        self.state = Bartender.STILL

    def no_move_right(self):
        self.state = Bartender.STILL

    def move_left(self):
        self.state = Bartender.GOING_LEFT

    def move_right(self):
        self.state = Bartender.GOING_RIGHT
    
    def move_down(self):
        if self.cur_lane < self.num_lanes-1:
            self.cur_lane += 1
            self.state = Bartender.MOVING
            self.inside_bar = 0

    def move_up(self):
        if self.cur_lane > 0:
            self.cur_lane -= 1
            self.state = Bartender.MOVING
            self.inside_bar = 0
    
    def get_new_beer_position(self):
        rect = self.rect
        rect.left = rect.left #Bartender.positions[self.cur_lane]['x']
        rect.top = Bartender.positions[self.cur_lane]['y']
        return rect

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

