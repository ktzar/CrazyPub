import random
import pygame
import utils


"""Stage"""
class Stage():
    def __init__(self, stage_file='level_1'):
        self.image, self.rect = utils.load_image('{0}.png'.format(stage_file))

        self.level_data = []

        self.colors = { \
            "client":(0,0,0,255)\
        }

        for x in range(0, self.rect.width-1):
            column = [0,0,0,0]
            for y in range(self.rect.height):
                if self.image.get_at((x,y)) == self.colors["client"]:
                    column[y] = 1

            self.level_data.append(column)


    def get_clients_in_t(self, time):
        return self.level_data[time]
        pass

    def get_max_time(self):
        return len(self.level_data)

