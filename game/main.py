#Import Modules
import os, pygame, time
import random
from pygame.locals import *
from bartending import *
from menus import *


def CrazyPub():
    pygame.init()
    if not pygame.font: print 'Warning, fonts disabled'
    if not pygame.mixer: print 'Warning, sound disabled'
    screen = pygame.display.set_mode((512, 480), pygame.DOUBLEBUF)
    pygame.display.set_caption('Crazy Pub')
    #pygame.display.toggle_fullscreen()
    pygame.mouse.set_visible(0)
#icon
#icon, foo = utils.load_image('icon.png')
#pygame.display.set_icon(icon)

    bartending  = Bartending(screen)
    menu        = Menu(screen)
    options     = Options(screen)
    about       = About(screen)
    clock = pygame.time.Clock()

    if options.values[1]['value'] == "On":
        music = utils.load_sound('level_1.ogg')
        music.play()


    while 1:
        clock.tick(100)
        if menu.selected_option == -1:
            menu.loop()
        elif menu.selected_option == 0:
            bartending.loop()
        elif menu.selected_option == 1:
            options.loop()
            if options.finished == True:
                #recreate menu
                menu    = Menu(screen)
                options = Options(screen)
        elif menu.selected_option == 2:
            about.loop()
            if about.finished == True:
                #recreate menu
                about   = About(screen)
                menu    = Menu(screen)
        elif menu.selected_option == 3:
            pygame.quit()
            quit()
