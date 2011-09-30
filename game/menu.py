import pygame
from pygame.locals import *
import utils
import math

class Menu():
    def __init__(self, screen):
        self.font = utils.load_font('saloon.ttf', 20)
        self.background, foo    = utils.load_image('back.png')
        self.logo, foo          = utils.load_image('logo.png')
        self.screen = screen
        self.chosen_option = 0
        self.options = [ "Start game", "Options", "Quit" ]
        self.age = 0
        self.game_start = False

    def handle_keys(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:                 
                if event.key == K_UP:
                    self.option_up()
                elif event.key == K_DOWN:
                    self.option_down()
                elif event.key == K_ENTER:
                    self.game_start = True

        return True

    def option_down(self):
        if self.chosen_option != len(self.options)-1:
            self.chosen_option += 1

    def option_up(self):
        if self.chosen_option != 0:
            self.chosen_option -= 1

    def loop(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, (10, 50))
        self.age +=1

        esc_pressed = self.handle_keys()
        if esc_pressed == False:
            return False


        y = 200
        i = 0
        for option in self.options:
            if i==self.chosen_option:
                color = (255,100,100)
                angle = math.sin(self.age/10)  * 3
                _y = int(y + angle * angle)
            else:
                color = (255,255,255)    
                angle = 0
                _y = y

            text = self.font.render(option, 2, (0,0,0,0))
            self.screen.blit(text, (152, _y+2))
            text = self.font.render(option, 2, color)
            self.screen.blit(text, (150, _y))
            y += 80
            i += 1

        pygame.display.flip()

