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

    bartending      = Bartending(screen)
    menu            = Menu(screen)
    options         = Options(screen)
    about           = About(screen)
    highscores      = Highscores(screen)
    newhighscore    = False
    clock = pygame.time.Clock()

    if 'Music' in options.values and options.values['Music'] == "On":
        music = utils.load_sound('level_1.ogg')
        music.play()


    while 1:
        clock.tick(100)
        #Main menu loop
        if menu.selected_option == -1:
            menu.loop()
        #Game loop
        elif menu.selected_option == 0:
            bartending.loop()
            #Game finished, create newhighscore screen
            if bartending.game_finished == True:
                if newhighscore == False:
                    newhighscore = Newhighscore(screen, bartending)
                newhighscore.loop()
                #Name entered
                if newhighscore.finished == True:
                    menu = Menu(screen)
                    bartending = Bartending(screen)
        elif menu.selected_option == 1:
            options.loop()
            if options.finished == True:
                #recreate menu
                if options.values['Music'] == 'Off':
                    music.stop()
                menu    = Menu(screen)
                options = Options(screen)
        elif menu.selected_option == 2:
            highscores.loop()
            if highscores.finished == True:
                #recreate menu
                highscores = Highscores(screen)
                menu    = Menu(screen)
        elif menu.selected_option == 3:
            about.loop()
            if about.finished == True:
                #recreate menu
                about   = About(screen)
                menu    = Menu(screen)
        elif menu.selected_option == 3:
            pygame.quit()
            quit()
