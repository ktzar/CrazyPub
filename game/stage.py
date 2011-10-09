'''This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

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
        if time >= len(self.level_data) :
            return False
        else:
            return self.level_data[time]

    def get_max_time(self):
        return len(self.level_data)

