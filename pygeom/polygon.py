import sys
import matplotlib.pyplot as plt
import numpy as np
import math

from scipy import stats
import matplotlib.patches as patches

from .point import Point


class Polygon():

    def __init__(self, vertices, color='#4ca3dd', fill=True, alpha=0.2):
        self.vertices = vertices
        self.length   = len(self.vertices)

        if self.length < 3:
            raise Exception("Number of vertices (%s) provided is too small for a Polygon" % self.length)

        self.color  = color
        self.fill   = fill
        self.alpha  = alpha


    def __str__(self):
        return "Polygon with %s vertices" % (self.length)

    def __repr__(self):
        return "Polygon with %s vertices" % (self.length)

    
    def draw(self, ax):

        points = [[p[0], p[1]] for p in self.vertices]
        self.array = np.array(points)

        polygon = patches.Polygon(
            self.array, 
            color   = self.color, 
            fill    = self.fill, 
            alpha   = self.alpha
        )
        return ax.add_patch(polygon)


