import math
import matplotlib.pyplot as plt
import numpy as np

from .point import Point
from .util import get_theta, pprint_float, midpoint, get_text_location


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
    def __init__(self, p=None, slope=None, intercept=None, p1=None, p2=None, **kwargs):

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

        # Compute the slope and the intercept
        self.__set_slope_intercept__()
        self.__set_equation__()
 
        # Point styling
        self.styling_defaults = {
            'color'     : '#696969',
            'zorder'    : 1,
            'linewidth' : 1,
            'linestyle' : '-',
            'add_eq'    : False,
            'label'     : None,
            'loc'       : 'up'
        }
        for param, default in self.styling_defaults.items():
            if param in kwargs.keys():
                setattr(self, param, kwargs[param])
            else:
                setattr(self, param, default)

       

    def __set_slope_intercept__(self):
        """ Set the line's slope and intercept """
        self.dx = self.p2[0] - self.p1[0]
        self.dy = self.p2[1] - self.p1[1]

        # vertical line
        if self.dx == 0:
            self.slope      = float('inf')
            self.intercept  = np.nan
        # horizontal line
        elif self.dy == 0:
            self.slope      = 0
            self.intercept  = self.p1[1]
        # other
        else:
            self.slope      = self.dy/self.dx
            self.intercept  = self.p1[1] - self.slope * self.p1[0]
    

    def __set_equation__(self):
        """
        Line equation: y = ax + b
        """
        if self.slope == 0: 
            self.equation = "y = %s" % pprint_float(self.intercept)

        elif np.isinf(self.slope):
            self.equation = "x = %s" % pprint_float(self.p1.x)

        elif self.intercept == 0:
            self.equation = "y = %s x" % pprint_float(self.slope)

        elif self.intercept < 0: 
            self.equation = "y = %s x - %s" % (
                pprint_float(self.slope),
                pprint_float(abs(self.intercept))
            )
        else:
            self.equation = "y = %s x + %s" % (
                pprint_float(self.slope),
                pprint_float(self.intercept)
            )

        
    def y(self, x):
        """ From the line's equation, get y given x """
        y = self.slope*x + self.intercept
        return y

    def __getp2__(self):
        x = 0
        y = self.p1.y - self.slope*self.p1.x
        return Point(x, y)

    def __setpoints__(self):
        # horizontal line
        if self.slope == 0:
            self.p1 = Point(0, self.intercept)
            self.p2 = Point(1, self.intercept)
        else:
            self.p1 = Point(0, self.intercept)
            self.p2 = Point(-self.intercept/self.slope, 0)

    def __str__(self):
        return "Line:\ty = %.3f x + %.3f" % (self.slope, self.intercept)
    
    def __repr__(self):
        return "Line:\ty = %.3f x + %.3f" % (self.slope, self.intercept)
    
    def draw(self, ax, xlim, ylim):

        # Take care of vertical lines
        if np.isinf(self.slope):
            xv = [self.p1.x for v in ylim]
            yv = ylim
        else:
            xv = xlim
            yv = [self.y(x) for x in xlim]

        # Draw the line first
        ax.plot(xv, yv, color=self.color, linewidth=self.linewidth, linestyle=self.linestyle)
        
        # Also add the text if needed
        if self.label is not None or self.add_eq == True:
            # angle to rotate the text so it is parallel to the line
            # also depends on subplot size
            dx = self.dx * ax.bbox.width
            dy = self.dy * ax.bbox.height
            self.theta = get_theta(dx, dy, rad=False)

            # text x,y location
            x, y    = midpoint(self.p1, self.p2)
            tx, ty  = get_text_location(x, y, xlim, ylim, self.loc)

            # label
            if self.label is not None and self.add_eq == True:
                label = "%s  %s" % (self.label, self.equation)
            elif self.label is not None:
                label = self.label
            else:
                label = self.equation

            # add text at midpoint between p1 and p2
            ax.text(
                tx, ty, label, 
                color=self.color, rotation=self.theta, fontsize=12, ha='center', va='center'
            )


