import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .point import Point
from .util import distance


class Triangle():

    def __init__(self, p1, p2, p3, color='#4ca3dd', fill=True, alpha=0.2):
        self.p1     = p1
        self.p2     = p2
        self.p3     = p3
        self.color  = color
        self.fill   = fill
        self.alpha  = alpha

        self.get_perimeter()


    def __str__(self):
        return "Triangle(%s,%s,%s)" % (self.p1, self.p2, self.p3)

    def __repr__(self):
        return "Triangle(%s,%s,%s)" % (self.p1, self.p2, self.p3)

    
    def get_perimeter(self):
        """ Triangle perimeter """
        self.perimeter = distance(p1, p2) + distance(p2, p3) + distance(p1, p3)
        return self.perimeter

    
    def get_area(self):
        """ Triangle area """
        pass


    def draw(self, ax):

        self.array = np.array([
            [self.p1[0], self.p1[1]],
            [self.p2[0], self.p2[1]],
            [self.p3[0], self.p3[1]]
        ])

        triangle = patches.Polygon(
            self.array, 
            color   = self.color, 
            fill    = self.fill, 
            alpha   = self.alpha
        )
        return ax.add_patch(triangle)


