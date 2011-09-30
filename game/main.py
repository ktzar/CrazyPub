#Import Modules
import os, pygame, time
import random
from pygame.locals import *
from bartending import *
from menu import *


def CrazyPub():
    pygame.init()
    if not pygame.font: print 'Warning, fonts disabled'
    if not pygame.mixer: print 'Warning, sound disabled'
    screen = pygame.display.set_mode((512, 480), pygame.DOUBLEBUF)
    pygame.display.set_caption('Crazy Pub')
    pygame.display.toggle_fullscreen()
    pygame.mouse.set_visible(0)
#icon
#icon, foo = utils.load_image('icon.png')
#pygame.display.set_icon(icon)

    bartending = Bartending(screen)
    menu = Menu(screen)
    clock = pygame.time.Clock()

    while 1:
        clock.tick(100)
        if menu.game_start == True:
            bartending.loop
        else:
            menu.loop()
