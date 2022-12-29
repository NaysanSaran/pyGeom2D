import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from mpl_toolkits.axisartist import SubplotZero

import warnings

from .util import get_axes_arrow_shape


class Axes():

    def __init__(self, xlim=(-5,5), ylim=(-5,5), figsize=(12,5), style='arrow'):
        self.xlim       = xlim
        self.ylim       = ylim
        self.figsize    = figsize
        self.ax         = None
        self.drawMajor  = False
        self.style      = style

        # Reference table for each shape
        self.shapes = {
            "Point"     : [],
            "Segment"   : [],
            "Vector"    : [],
            "Line"      : [],
            "Curve"     : [],
            "Circle"    : [],
            "Ellipse"   : [],
            "Polygon"   : [],
            "Rectangle" : [],
            "Triangle"  : []
        }


    def __drawArrows__(self):
        """ Draw the axes x and y arrows """
        
        if self.style == 'arrow':
            self.x_arr, self.y_arr = get_axes_arrow_shape(self.xlim, self.ylim)
            x_arrow = patches.Polygon(self.x_arr, color='#000000')
            y_arrow = patches.Polygon(self.y_arr, color='#000000')

            self.ax.add_patch(x_arrow)
            self.ax.add_patch(y_arrow)
        else:
            try:
                xlabel = self.style[0]
                ylabel = self.style[1]
            except:
                raise Exception("style should be either 'arrow' or [xlabel, ylabel]")

            xlabel_x = self.xlim[1] - 0.02*(self.xlim[1] - self.xlim[0])
            xlabel_y = 0.04*(self.ylim[1] - self.ylim[0])
            ylabel_x = 0.04*(self.xlim[1] - self.xlim[0])
            ylabel_y = self.ylim[1] - 0.02*(self.ylim[1] - self.ylim[0])

            self.ax.text(xlabel_x, xlabel_y, xlabel, ha='right', va='center')
            self.ax.text(ylabel_x, ylabel_y, ylabel, ha='right', va='center', rotation=90)


    def __updateAxisLimits__(self):

        # Small offset values for text positioning
        minrange = min(self.xlim[1] - self.xlim[0], self.ylim[1] - self.ylim[0])
        self.dx = 0.02 * minrange / self.ax.bbox.width
        self.dy = 0.02 * minrange / self.ax.bbox.height

        # Plot limits - add some padding to the axes if arrow style
        if self.style == 'arrow':
            plt.xlim((self.xlim[0], self.x_arr[0, 0]))
            plt.ylim((self.ylim[0], self.y_arr[0, 1]))
        else:
            plt.xlim(self.xlim[0]-self.dx, self.xlim[1]+self.dx)
            plt.ylim(self.ylim[0]-self.dy, self.ylim[1]+self.dy)


    def __drawAxis__(self):
        """
        Draws the 2D cartesian axis
        """
        # A subplot with two additional axis, "xzero" and "yzero"
        # corresponding to the cartesian axis
        plt.rcParams.update({'font.size': 12})
        self.ax = SubplotZero(self.fig, 1, 1, 1)
        self.fig.add_subplot(self.ax)

        # make xzero axis (horizontal axis line through y=0) visible.
        for axis in ["xzero","yzero"]:
            self.ax.axis[axis].set_visible(True)

        # make the other axis (left, bottom, top, right) invisible
        for n in ["left", "right", "bottom", "top"]:
            self.ax.axis[n].set_visible(False)

        # Draw the arrows
        self.__drawArrows__()
        self.__updateAxisLimits__()

 
    def __rescale__if_needed__(self, s):
        """
        Raise a warning and rescale axes if the shape may need square axes
        """
        if hasattr(s, 'needs_square_axes') and s.needs_square_axes == True:
            if self.xlim != self.ylim or self.figsize[0] != self.figsize[1]:

                w = '%s may look distorted if axes are not square. Rescaling to be safe.' % s
                warnings.warn(w)

                minv = min(self.xlim[0], self.ylim[0])
                maxv = max(self.xlim[1], self.ylim[1])
                self.figsize = (max(self.figsize), max(self.figsize))
                self.xlim = (minv, maxv)
                self.ylim = (minv, maxv)
 

    def draw(self, img=None):
        """ Renders the figure """

        # Rescale if needed
        for shape_list in self.shapes.values():
            for s in shape_list:
                self.__rescale__if_needed__(s)
 
        # First draw the axis
        self.fig = plt.figure(figsize=self.figsize)
        self.__drawAxis__()

        # Loop throught each shape and plot it
        for shape_name, shape_list in self.shapes.items():
            for s in shape_list:
                s.draw(self.ax, self.xlim, self.ylim)

        if img is None:
            plt.show()
        else:
            plt.savefig(img)


    def addMany(self, shapes, **kwargs):
        """ Add many shapes at once """
        for s in shapes:
            self.add(s, **kwargs)


    def add(self, s, **kwargs):
        """ Add one shape at the time """
        # style the shape of needed
        for key, value in kwargs.items():
            setattr(s, key, value)

        shape = type(s).__name__
        self.shapes[shape].append(s)




