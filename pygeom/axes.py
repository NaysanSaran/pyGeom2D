import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axisartist import SubplotZero


class Axes():

    def __init__(self, xlim=(-5,5), ylim=(-5,5), figsize=(12,5)):
        self.xlim = xlim
        self.ylim = ylim
        self.figsize  = figsize

        self.scale_arrows()
        self.ax = None
        self.drawMajor = False

        # Reference table for each shape
        self.shapes = {
            "Point"     : [],
            "Ellipse"   : [],
            "Polygon"   : [],
            "Rectangle" : [],
            "Segment"   : [],
            "Triangle"  : [],
            "Line"      : [],
            "Vector"    : []
        }


    def __arrow__(self, x, y, dx, dy, width, length):
        plt.arrow(
            x, y, dx, dy,
            color       = 'k',
            clip_on     = False,
            head_width  = self.head_width,
            head_length = self.head_length
        )

    def __drawAxis__(self):
        """
        Draws the 2D cartesian axis
        """
        # A subplot with two additional axis, "xzero" and "yzero"
        # corresponding to the cartesian axis
        self.ax = SubplotZero(self.fig, 1, 1, 1)
        self.fig.add_subplot(self.ax)

        # make xzero axis (horizontal axis line through y=0) visible.
        for axis in ["xzero","yzero"]:
            self.ax.axis[axis].set_visible(True)
        # make the other axis (left, bottom, top, right) invisible
        for n in ["left", "right", "bottom", "top"]:
            self.ax.axis[n].set_visible(False)

        # Plot limits
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)

        # Draw the arrows
        self.__arrow__(self.xlim[1], 0, 0.01, 0, 0.3, 0.2) # x-axis arrow
        self.__arrow__(0, self.ylim[1], 0, 0.01, 0.2, 0.3) # y-axis arrow


    def scale_arrows(self):
        """ Make the arrows look good regardless of the axis limits """
        xrange = self.xlim[1] - self.xlim[0]
        yrange = self.ylim[1] - self.ylim[0]

        self.head_width  = xrange/30
        self.head_length = yrange/30


    def draw(self):

        self.scale_arrows()
        self.fig = plt.figure(figsize=self.figsize)
        # First draw the axis
        self.__drawAxis__()

        # These shapes do not need to be passed the axes as an argument
        for shape in ["Point", "Vector", "Segment"]:
            for s in self.shapes[shape]:
                s.draw()

        # Plot the other shapes
        for shape in ["Line", "Ellipse", "Rectangle", "Triangle", "Polygon"]:
            for s in self.shapes[shape]:
                s.draw(self.ax)

            # Ellipses only: also draw its major and minor axes?
            if shape == "Ellipse" and self.drawMajor:
                ellipse.v_major.draw()
                ellipse.v_minor.draw()
        plt.show()


    #-------------------------------------------------
    # Add any drawable element to the axis
    #-------------------------------------------------
    def addMany(self, shapes):
        for s in shapes:
            self.add(s)

    def add(self, s):
        shape = type(s).__name__
        self.shapes[shape].append(s)


