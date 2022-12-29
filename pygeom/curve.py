import math
import matplotlib.pyplot as plt
import numpy as np

from .point import Point
from .line import Line
from .util import get_theta, pprint_float


class Curve():
    """
    A curve needs a function f(x) that will be plotted
    x_disc: x coordinates of any discontinuities the function has
    """
    def __init__(self, f, x_disc=[], **kwargs):

        if not callable(f):
            raise Exception("f should be a function")

        self.f = f
        self.x_disc = x_disc

        # Curve styling
        self.styling_defaults = {
            'color'     : '#696969',
            'linewidth' : 1,
            'linestyle' : '-',
            'label'     : None,
            'loc'       : 'up'
        }
        for param, default in self.styling_defaults.items():
            if param in kwargs.keys():
                setattr(self, param, kwargs[param])
            else:
                setattr(self, param, default)


    def __str__(self):
        return "Curve:\ty = $s(x)" % (self.f.__name__)
    
    def __repr__(self):
        return "Curve:\ty = %s(x)" % (self.f.__name__)
    

    def __label_xy__(self, xlim, ylim):
        """ 
        Locate where the curve ends to position its label 
        """
        xval = sorted(self.x_plots[-1], reverse=True)
        for i in range(len(xval)-1):
            if xlim[0] < xval[i] < xlim[1] and ylim[0] < self.f(xval[i]) < ylim[1]:
                break

        # last two curve points that are still within the plot limits
        x2 = xval[i]
        x1 = xval[i+1]
        y2 = self.f(x2)
        y1 = self.f(x1)
        # rise and run for the slope
        dy = y2 - y1
        dx = x2 - x1
        # coordinates of where to locate the text
        dt = 0.02*(xlim[1]-xlim[0])
        s2 = math.pow(dx,2)/math.pow(dy,2)
        ux = x1 + math.sqrt((math.pow(dt,2))/(1 + s2))
        uy = y1 + dt * math.sqrt((s2)/(1+s2))
        return ux, uy, dx, dy


    def approximate_tangent(self, point, delta=0.0001, **kwargs):
        """
        Approximate the tangent line to curve at point (x,y)
        """
        if point.y  != self.f(point.x):
            raise Exception("%s is not on the curve" % point)

        p1 = Point(point.x-delta, self.f(point.x-delta))
        p2 = Point(point.x+delta, self.f(point.x+delta))
        tangent = Line(p1=p1, p2=p2, **kwargs)
        tangent.needs_square_axes = True
        return tangent


    def approximate_normal(self, point, delta=0.0001, **kwargs):
        """
        Approximate the normal line to curve at point (x,y)
        """
        if point.y  != self.f(point.x):
            raise Exception("%s is not on the curve" % point)

        # slope around the point of interest
        dx = 2*delta
        dy = self.f(point.x+delta) - self.f(point.x-delta)
        p1 = point
        p2 = Point(point.x + 1, point.y - (dx/dy))
        normal = Line(p1=p1, p2=p2, **kwargs)
        normal.needs_square_axes = True
        return normal


    def draw(self, ax, xlim, ylim):

        # small step to iteratively plot the curve
        step = 0.01*(xlim[1] - xlim[0])
        self.x_plots = []
        self.y_plots = []

        # No discontinuities? Print a single plot
        if len(self.x_disc) == 0:

            xv = list(np.arange(xlim[0], xlim[1], step))
            if not 0 in xv:
                xv = sorted(xv + [0.0])

            yv = [self.f(x) for x in xv]
            self.x_plots.append(xv)
            self.y_plots.append(yv)

        # Otherwise one plot per continuous subset of the function
        else:
            xall = np.arange(xlim[0], xlim[1], step)
            xmin = xlim[0] - 1
            
            values = self.x_disc + [xlim[1] + 1]
            for discont in values:
                xv = [x for x in xall if xmin < x < discont]
                yv = [self.f(x) for x in xv]

                self.x_plots.append(xv)
                self.y_plots.append(yv)
                xmin = discont

        # Draw each continuous curve separately
        for i in range(len(self.x_plots)):
            ax.plot(
                self.x_plots[i], 
                self.y_plots[i], 
                color=self.color, 
                linewidth=self.linewidth, 
                linestyle=self.linestyle
            )

        # Is there a label to add?
        if self.label is not None:
            # Get text anchor
            x, y, dx, dy = self.__label_xy__(xlim, ylim)
            # Find the correct angle for text rotation, also depends on subplot size
            dx = dx * ax.bbox.width
            dy = dy * ax.bbox.height 
            self.theta = get_theta(dx, dy, rad=False)
            # Add label
            ax.text(
                x, y, self.label, color=self.color,
                rotation=self.theta, fontsize=12, ha='center', va='center'
            )




