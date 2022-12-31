import matplotlib.pyplot as plt
import numpy as np

from .point import Point
from .util import get_theta, pprint_float, midpoint, get_text_location


class Segment():
    """
    Segment(p1,p2)
        p1: Point()
        p2: Point()
    """
    def __init__(self, p1, p2, **kwargs):

        self.p1     = p1
        self.p2     = p2
        self.items  = [p1,p2]

        # Rise and run to be used in drawing
        self.dx = self.p2[0] - self.p1[0]
        self.dy = self.p2[1] - self.p1[1]

        # Segment styling
        self.styling_defaults = {
            'color'     : '#696969',
            'zorder'    : 3,
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

       
    def __getitem__(self, index):
        return self.items[index]
    
    def __str__(self):
        return "Segment(%s,%s)" % (self.p1, self.p2)
    
    def __repr__(self):
        return "Segment(%s,%s)" % (self.p1, self.p2)
    
    
    def draw(self, ax, xlim, ylim):

        xv = [self.p1[0], self.p2[0]] # Gather x values
        yv = [self.p1[1], self.p2[1]] # Gatner y values

        ax.plot(xv, yv, color=self.color, linewidth=self.linewidth, linestyle=self.linestyle)

        # Also add the text if needed
        if self.label is not None or self.add_eq == True:
            # angle to rotate the text so it is parallel to the segment
            # also depends on subplot size
            dx = self.dx * ax.bbox.width
            dy = self.dy * ax.bbox.height
            self.theta = get_theta(dx, dy, rad=False)

            # text x,y location
            x, y    = midpoint(self.p1, self.p2)
            tx, ty  = get_text_location(x, y, xlim, ylim, self.loc)

            # add text at midpoint between p1 and p2
            ax.text(
                tx, ty, self.label, 
                color=self.color, rotation=self.theta, fontsize=12, ha='center', va='center'
            )



