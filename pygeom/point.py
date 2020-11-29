import matplotlib.pyplot as plt
import numpy as np


def midpoint(p1, p2, add_coordinates=True, color='#4ca3dd'):
    """
    Midpoint between two 2D points
        p1: Point()
        p2: Point()
    """
    x = (p1[0]+p2[0])/2
    y = (p1[1]+p2[1])/2
    return Point(x,y, color=color, add_coordinates=add_coordinates)


class Point():

    def __init__(self, x, y, color='#4ca3dd', size=50, add_coordinates=True, zorder=10):
        self.x = x
        self.y = y
        self.color = color
        self.size  = size
        self.zorder= zorder
        self.add_coordinates = add_coordinates
        self.y_offset = 0.2
        self.items = np.array([x,y])
        self.len = 2

    def __getitem__(self, index):
        return self.items[index]

    def __str__(self):
        return "Point(%.2f,%.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%.2f,%.2f)" % (self.x, self.y)

    def __len__(self):
        return self.len

    def draw(self):
        plt.scatter([self.x], [self.y], color=self.color, s=self.size, zorder=self.zorder)

        # Add the coordinates if asked by user
        if self.add_coordinates:
            plt.text(
                self.x, self.y + self.y_offset,
                "(%.1f,%.1f)"%(self.x,self.y),
                horizontalalignment='center',
                verticalalignment='bottom',
                fontsize=12
            )

