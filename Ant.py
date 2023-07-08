#!/usr/bin/env python3

"""
Ant sprite class governing ant behaviour.
for ant colony simulation.
"""
import os
import random
import pygame
from numpy import *


UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
#FACINGS = {0: 'UP', (0,1), 
#           }
ANTCOLOUR = (255,0,255)


class Ant(pygame.sprite.Sprite):
    """

    """
    def __init__(self, centroid):
        pygame.sprite.Sprite.__init__(self)
        self.food = False
        self.orientation = random.randint(0,3)
        self.icon = pygame.Surface([9,9])
        self.icon.fill(ANTCOLOUR)
        self.size = [9,9]
        self.centroid = centroid


    def getPosition(self):
        # return the draw position of the ant dependent on orientation
        # do the following for each possible orientation,
        # pygame draws from the top left most pixel -> right and down.
        # want to use a centroid to map the position.
        self.position = [self.centroid[0] - 5, self.centroid[1] - 5]
        return self.position

    def move(self):
        #returns the new position after taking a move
        if self.orientation == UP:
            self.centroid[1] = self.centroid[1] - 1
        elif self.orientation == LEFT:
            self.centroid[0] = self.centroid[0] - 1
        elif self.orientation == DOWN:
            self.centroid[1] = self.centroid[1] + 1
        elif self.orientation == RIGHT:
            self.centroid[0] = self.centroid[0] + 1
    
    def scent(self):
        if self.orientation == UP:
            pass
        elif self.orientation == LEFT:
            pass
        elif self.orientation == DOWN:
            pass
        elif self.orientation == RIGHT:
            pass
        return [0]
    
    def pickup(self):
        #picks up food, gives feedback
        if self.food != True:
            self.food = True
        pass
    

    def sense(self):
        #sense the pixels infrom as a vector
        if self.orientation == UP:
            pass
        elif self.orientation == LEFT:
            pass
        elif self.orientation == DOWN:
            pass
        elif self.orientation == RIGHT:
            pass
        return [0]

    def think(self):
        #
        pass
    
    def act(self):
        #
        pass