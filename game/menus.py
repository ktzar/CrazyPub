import pygame
from pygame.locals import *
import utils
import math
import pickle

class Abstract_Menu():
    def __init__(self, screen):
        self.font = utils.load_font('saloon.ttf', 20)
        self.background, foo    = utils.load_image('back.png')
        self.logo, foo          = utils.load_image('logo.png')
        self.screen = screen
        self.chosen_option = 0
        self.age = 0
        self.selected_option = -1
        self.events = [] #So the subclasses can inspect input events
        self.finished = False
        self.line_height = 60
        self.left_margin = 152

    def handle_keys(self):
        #Handle Input Events
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:                 
                if event.key == K_UP:
                    self.option_up()
                elif event.key == K_DOWN:
                    self.option_down()
                elif event.key == K_RETURN or event.key == K_LEFT or event.key == K_RIGHT:
                    self.selected_option = self.chosen_option
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
        self.age +=0.15

        esc_pressed = self.handle_keys()
        if esc_pressed == False:
            return False


        y = 200
        x = self.left_margin
        i = 0
        for option in self.options:
            if i==self.chosen_option:
                color = (255,100,100)
                angle = math.sin(self.age)  * 3
                _y = (y + angle * angle)
            else:
                color = (255,255,255)    
                angle = 0
                _y = y

            text = self.font.render(option, 2, (0,0,0,0))
            self.screen.blit(text, (x, _y+2))
            text = self.font.render(option, 2, color)
            self.screen.blit(text, (x, _y))
            y += self.line_height
            i += 1

        pygame.display.flip()


class Menu(Abstract_Menu):
    
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.options = [ "Start game", "Options", "Highscores", "About", "Quit" ]

class Options(Abstract_Menu):
    
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.values = { \
            'Difficulty':'Easy',\
            'Music':'On'\
        }
        try:
            self.values = pickle.load(open('options.p', 'rb'))
        except:
            print "Options file not available"
        self.go_back = False

    def handle_keys(self):
        #Handle Input Events
        Abstract_Menu.handle_keys(self)
        for event in self.events:
            if event.type == KEYDOWN:                 
                if event.key == K_LEFT or event.key == K_RIGHT:
                    print "Chosen option "+str(self.chosen_option)
                    self.toggle_option(self.chosen_option)
        return True

    def loop(self):
        #set options
        self.options = []
        for value in self.values:
            print value
            self.options.append('{0}: {1}'.format(value,self.values[value]))
        self.options.append('Back')
        Abstract_Menu.loop(self)
        

    def toggle_option(self, num_option):
        #Difficulty
        if num_option == 0:
            if self.values['Difficulty'] == "Easy":
                self.values['Difficulty'] = "Hard"
            else:
                self.values['Difficulty'] = "Easy"
        #Music
        elif num_option == 1:
            if self.values['Music'] == "On":
                self.values['Music'] = "Off"
            else:
                self.values['Music'] = "On"
        elif num_option == 2:
            self.finished = True
        pickle.dump(self.values, open('options.p', 'wb'))

#Credits, basically
class About(Abstract_Menu):
    
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.font = utils.load_font('saloon.ttf', 16)
        self.line_height = 40
        self.left_margin = 52
        self.options = [\
            'CREDITS',
            'Game design: kTzAR',
            'Game development: kTzAR',
            'Music: ORIGAMI by DANJYON KIMURA',
            'Press ESC to go back',
        ]

    def handle_keys(self):
        #Only listen to ESC, don't execute parent's handle_keys
        #since there are no options to choose from
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:                 
                if event.key == K_ESCAPE:
                    self.finished = True
        return True

class Highscores(Abstract_Menu):
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.font = utils.load_font('saloon.ttf', 16)
        self.line_height = 40
        self.left_margin = 52

        try:
            self.highscores = pickle.load(open('highscores.p', 'rb'))
        except:
            self.highscores = [ {'name':'kTzAR','score':22000} ]
            pickle.dump(self.highscores, open('highscores.p', 'wb'))
            print "Highscores file not available, created new"

        self.options = [ 'HIGH-SCORES' ]
        for highscore in self.highscores :
            self.options.append(highscore['name']+': '+str(highscore['score']))

    def handle_keys(self):
        #Only listen to ESC, don't execute parent's handle_keys
        #since there are no options to choose from
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:                 
                if event.key == K_ESCAPE:
                    self.finished = True
        return True

class Newhighscore(Abstract_Menu):
    def __init__(self, screen, bartending):
        Abstract_Menu.__init__(self, screen)
        self.font = utils.load_font('saloon.ttf', 16)
        self.player_name = 'Blablah'
        self.bartending = bartending
        self.age = 0

        #No options in this menu
        self.options = [ 'New High score', 'You made {0} points'.format(self.bartending.score) ]
    def loop(self):
        self.age+=1
        if self.age % 10 < 5:
            text = self.font.render(self.player_name, 2, (255,255,255))
            self.screen.blit(text, (50, 300))
        Abstract_Menu.loop(self)


    def handle_keys(self):
        #Only listen to ESC, don't execute parent's handle_keys
        #since there are no options to choose from
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:                 
                try:
                    typed_character = chr(event.key)
                except:
                    pass
                self.player_name += typed_character
                if event.key == 13:
                    print "Enter key"
        return True
