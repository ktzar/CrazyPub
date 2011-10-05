import os, pygame, time
import random
from pygame.locals import *
from sprites import *
from stage import *
import utils
import pickle


class Bartending():
    def __init__(self, screen):
        self.screen = screen
        self.initialise()

    def initialise(self):
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
        #Initialize Everything
        pygame.display.flip()

        #Load options
        try:
            self.options = pickle.load(open('options.p', 'rb'))
        except:
            print "No options"
            self.options = []

        self.game_paused = False
        #sounds
        self.sounds = {};
        self.sounds['music'] = utils.load_sound('music.ogg')
        self.sounds['glass'] = utils.load_sound('glass.ogg')
        self.sounds['throw'] = utils.load_sound('throw.ogg')
        if 1 in self.options and self.options[1]['value'] == "On":
            self.sounds['music'].play()
        #Create The Backgound
        self.background, foo = utils.load_image('back.png')

        #game variables
        self.speed = 50 #the lower the faster
        self.score = 0
        self.mugs = 10
        self.clients_served = 0
        self.time = 0 #to check the stage for clients

        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


        self.level = Stage('level_1')
        #The player's ship
        self.bartender = Bartender()
        #The dash indicators

        #group that stores all enemies
        self.beers       = pygame.sprite.Group()
        #group that stores all powerups
        self.clients     = pygame.sprite.Group()
        #group for information sprites in the screen, should be rendered the last one
        self.hud         = pygame.sprite.Group()
        self.font = utils.load_font('saloon.ttf', 20)


        self.game_started = False
        self.game_finished = False
        self.level_finished = False

    def client_gone(self):
        self.game_finished = True

    def return_beer(self, client):
        print "Return beer"
        if 'Difficulty' in self.options and self.options['Difficulty'] == "Hard":
            self.sounds['throw'].play()
            empty_beer = EmptyBeer(self, client.rect, client.cur_lane)
            self.beers.add( empty_beer )
        #client.kill()


    def emptybeer_arrived(self, emptybeer):
        print "emptybeer_arrived"
        #check if the bartender is in the same lane as the beer
        emptybeer.kill()
        if emptybeer.cur_lane != self.bartender.cur_lane :
            self.sounds['glass'].play()
            if self.mugs < 1:
                self.game_finished = True
            else:
                self.mugs -= 1
        else:
            self.score += 500

    def break_beer(self):
        if self.mugs < 1:
            self.game_finished = True
        else:
            self.mugs -= 1

    def handle_keys(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                #exit
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE and self.game_finished == True:
                self.game_finished = True
                
            if event.type == KEYDOWN:
                self.game_started = True
                if event.key == K_ESCAPE:
                    return False   #exit
                elif event.key == K_SPACE:
                    self.beers.add(Beer(self, self.bartender.get_new_beer_position(), self.bartender.cur_lane))
                    self.sounds['throw'].play()
                    pass
                elif event.key == K_UP:
                    self.bartender.move_up()
                elif event.key == K_DOWN:
                    self.bartender.move_down()
                elif event.key == K_p:
                    self.game_paused = not self.game_paused

        return True

    #Main Loop
    def loop(self):
        #handle input events
        esc_pressed = self.handle_keys()
        if self.game_finished:
            return
        if esc_pressed == False:
            return

        if self.game_started == False:
            start_text = self.font.render('Press any key to start', 2, (255,255,255))
            self.screen.blit(start_text, (150, 200))
            pygame.display.flip()
            return

        if self.game_paused == 1:
            start_text = self.font.render('Game paused', 2, (255,255,255))
            self.screen.blit(start_text, (150, 200))
            pygame.display.flip()
            return

        if self.time % self.speed == 0:
            if self.time/self.speed > self.level.get_max_time():
                self.game_finished = True
                return
            clients = self.level.get_clients_in_t(self.time/self.speed) #returns an array with 1 in the lanes with clients
            for i in range(len(clients)):
                if clients[i] == 1:
                    self.clients.add(Client(self, lane=i))

        for beer in self.beers:
            if not isinstance(beer, Beer):
                continue
            clients_drinking  = pygame.sprite.spritecollide(beer, self.clients, False)
            for client_drinking in clients_drinking:
                if client_drinking.state == Client.WAITING:
                    self.score += 100
                    self.clients_served += 1
                    beer.kill()
                    client_drinking.start_drinking()
                    #self.return_beer(client_drinking)
                    break
        try:
            pass
        except:
            self.level_finished = True

        #draw the level
        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.beers.sprites())
        all_sprites.add(self.clients.sprites())
        all_sprites.add(self.bartender)
        all_sprites.update()

        #Move and draw the background
        score_text = "Score: {0} Mugs: {1}".format(self.score, self.mugs)
        text = self.font.render(score_text, 1, (255, 255, 255))
        text_shadow = self.font.render(score_text, 1, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text_shadow, (12, 12))
        self.screen.blit(text, (10, 10))

        if self.game_finished == True:
            gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 200))
            gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 230))
        else:
            all_sprites.draw(self.screen)
        #draw all the groups of sprites
        pygame.display.flip()
        self.time += 1

    #Game Over


