import sys
import matplotlib.pyplot as plt
import numpy as np
import math

from scipy import stats
import matplotlib.patches as patches


from .point import Point


class Rectangle():

    def __init__(self, bottomLeft, topRight, color='#4ca3dd', fill=True, alpha=0.2):
        self.p1     = bottomLeft
        self.p3     = topRight
        self.p2     = Point(self.p3.x, self.p1.y)
        self.p4     = Point(self.p1.x, self.p3.y)
        self.color  = color
        self.fill   = fill
        self.alpha  = alpha


    def __str__(self):
        return "Rectangle(%s,%s,%s,%s)" % (self.p1, self.p2, self.p3, self.p4)

    def __repr__(self):
        return "Rectangle(%s,%s,%s,%s)" % (self.p1, self.p2, self.p3, self.p4)

    
    def draw(self, ax):

        self.array = np.array([
            [self.p1[0], self.p1[1]],
            [self.p2[0], self.p2[1]],
            [self.p3[0], self.p3[1]],
            [self.p4[0], self.p4[1]]
        ])

        rectangle = patches.Polygon(
            self.array, 
            color   = self.color, 
            fill    = self.fill, 
            alpha   = self.alpha
        )
        return ax.add_patch(rectangle)


