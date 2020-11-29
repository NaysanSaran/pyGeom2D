import sys
import matplotlib.pyplot as plt
import numpy as np

from .point import Point


class Line():
    """
    There are 3 ways to instanciate a line
        Line(p1,p2)
            p1:         Point()
            p2:         Point()
        Line(p, slope)
            p:          Point()
            slope:      float
        Line(slope, intercept)
            slope:      float
            intercept:  float
    """
    def __init__(self, p=None, slope=None, intercept=None, p1=None, p2=None, color='#696969', linewidth=1, linestyle='-'):

        if p1 is not None and p2 is not None:
            self.p1 = p1
            self.p2 = p2
        elif p is not None and slope is not None:
            self.p1 = p
            self.slope = slope
            self.p2 = self.__getp2__()
        elif slope is not None and intercept is not None:
            self.slope = slope
            self.intercept = intercept
            self.__setpoints__()
        else:
            raise Exception("Either Line(p1,p2), Line(p, slope), or Line(p, slope)")

        self.color = color
        self.linewidth = linewidth
        self.linestyle = linestyle

        # Compute the slope and the intercept
        self.set_slope_intercept()
        

    def set_slope_intercept(self):
        """ Set the line's slope and intercept """
        self.slope      = (self.p2[1] - self.p1[1]) / (self.p2[0] - self.p1[0])
        self.intercept  = self.p1[1] - self.slope * self.p1[0]
    
    def y(self, x):
        """ From the line's equation, get y given x """
        y = self.slope*x + self.intercept
        return y

    def __getp2__(self):
        x = 0
        y = self.p1.y - self.slope*self.p1.x
        return Point(x, y)

    def __setpoints__(self):
        self.p1 = Point(0, self.intercept)
        self.p2 = Point(-self.intercept/self.slope, 0)

    def __str__(self):
        return "Line:\ty = %.3f x + %.3f" % (self.slope, self.intercept)
    
    def __repr__(self):
        return "Line:\ty = %.3f x + %.3f" % (self.slope, self.intercept)
    
    def draw(self, ax):
        x_values = list(ax.get_xlim())
        y_values = [self.y(x) for x in x_values]
        plt.plot(
            x_values, 
            y_values, 
            color=self.color, 
            linewidth=self.linewidth,
            linestyle=self.linestyle
        )


