#Import Modules
import os, pygame, time
import random
from pygame.locals import *
from sprites import *
import utils

class Background(pygame.Surface):
    def __init__(self, screen):
        pygame.Surface.__init__(self, screen) #call Sprite intializer
        self.convert()
        self.screen = screen
        self.image, self.rect = utils.load_image('back.png');


class Bartending():
    def __init__(self):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        self.initialise()
        self.loop()

    def initialise(self):
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
        #Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((512, 480), pygame.DOUBLEBUF)
        pygame.display.set_caption('Crazy Pub')
        pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(0)
        #icon
        #icon, foo = utils.load_image('icon.png')
        #pygame.display.set_icon(icon)

        self.game_paused = False
        #sounds
        self.sounds = {};
        #self.sounds['powerup'] = utils.load_sound('powerup.wav')
        #self.sounds['music'].play()
        #Create The Backgound
        self.background, foo = utils.load_image('back.png')
        #game variables
        self.score = 0
        self.mugs = 10
        self.clients_served = 0
        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


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

        self.clock = pygame.time.Clock()

        self.game_started = False
        self.game_finished = False
        self.level_finished = False

    def client_gone(self):
        self.game_finished = True

    def return_beer(self, client):
        empty_beer = EmptyBeer(self, client.rect, client.cur_lane)
        self.beers.add( empty_beer )


    def emptybeer_arrived(self, emptybeer):
        #check if the bartender is in the same lane as the beer
        emptybeer.kill()
        if emptybeer.cur_lane != self.bartender.cur_lane :
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
                pygame.quit()
                quit()
                
            if event.type == KEYDOWN:
                self.game_started = True
                if event.key == K_ESCAPE:
                    return False   #exit
                elif event.key == K_SPACE:
                    self.beers.add(Beer(self, self.bartender.rect, self.bartender.cur_lane))
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
        count = 0
        while 1:
            count = (count+1)%50
            self.clock.tick(100)

            #handle input events
            ok = self.handle_keys()
            if ok == False:
                return
            
            chance = 100-self.clients_served
            if chance < 10:
                chance = 10
            if random.randint(0,chance) == 0:
                lane = random.randint(0,3)
                self.clients.add(Client(self, lane))

            for beer in self.beers:
                clients_drinking  = pygame.sprite.spritecollide(beer, self.clients, True)
                for client_drinking in clients_drinking:
                    self.score += 100
                    self.clients_served += 1
                    beer.kill()
                    self.return_beer(client_drinking)
                    break



            if self.game_started == False:
                start_text = self.font.render('Press any key to start', 2, (255,255,255))
                self.screen.blit(start_text, (150, 200))
                pygame.display.flip()
                continue

            if self.game_paused == 1:
                start_text = self.font.render('Game paused', 2, (255,255,255))
                self.screen.blit(start_text, (150, 200))
                pygame.display.flip()
                continue

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

    #Game Over


