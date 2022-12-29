import math
import numpy as np

from .util import get_text_location


class Point():

    def __init__(self, x, y, **kwargs):
        self.x      = x
        self.y      = y
        self.items  = np.array([x,y])
        self.len    = 2

        # Point styling
        self.styling_defaults = {
            'color' : '#4ca3dd',
            'size'  : 50,
            'zorder': 10,
            'coords': False,
            'label' : None,
            'loc'   : 'up'
        }
        for param, default in self.styling_defaults.items():
            if param in kwargs.keys():
                setattr(self, param, kwargs[param])
            else:
                setattr(self, param, default)


    def __getitem__(self, index):
        return self.items[index]

    def __str__(self):
        return "Point(%.2f,%.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%.2f,%.2f)" % (self.x, self.y)

    def __len__(self):
        return self.len

    def draw(self, ax, xlim, ylim):
        
        # Plot the point
        ax.scatter(
            [self.x], 
            [self.y], 
            color=self.color, 
            s=self.size, 
            zorder=self.zorder
        )

        # Compute a relatively small offset to add any text
        diagonal = math.sqrt(math.pow(xlim[1]-xlim[0], 2) + math.pow(ylim[1]-ylim[0], 2))
        offset   = diagonal / 50.

        # Add the text if needed
        if self.label is not None or self.coords == True:

            # label
            if self.label is not None and self.coords is True:
                label = "%s(%.1f,%.1f)" % (self.label, self.x, self.y)
            elif self.label is not None:
                label = self.label
            else:
                label = "(%.1f,%.1f)" % (self.x, self.y)

            # text location
            tx, ty = get_text_location(self.x, self.y, xlim, ylim, self.loc)
            ax.text(tx, ty, label, color=self.color, ha='center', va='center', fontsize=12)


