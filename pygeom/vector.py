import sys
import matplotlib.pyplot as plt
import numpy as np

from .point import Point


class Vector():
    """
    Vector(p1, p2)
        p1: Point()
        p2: Point()
    """
    def __init__(self, p1, p2,
                 color       = '#6897bb', 
                 linewidth   = 1, 
                 linestyle   = '-',
                 head_width  = 0.25,
                 head_length = 0.3,
                 zorder      = 15
                ):
        self.p1     = p1
        self.p2     = p2
        self.items  = [self.p1, self.p2]
        self.x      = self.p2[0] - self.p1[0]
        self.y      = self.p2[1] - self.p1[1]
        self.arr    = np.array([self.x, self.y])
        self.orig   = (self.p1[0], self.p1[1])
        self.linewidth  = linewidth
        self.linestyle  = linestyle
        self.color      = color
        self.zorder     = zorder
        self.head_width  = head_width
        self.head_length = head_length
        
    def __getitem__(self, index):
        return self.items[index]
    
    def __str__(self):
        return "Vector [(%.1f,%.1f), (%.1f,%.1f)]" % (
            self.p1.x, self.p1.y,
            self.p2.x, self.p2.y
        )
    
    def __repr__(self):
        return "Vector [(%.1f,%.1f), (%.1f,%.1f)]" % (
            self.p1.x, self.p1.y,
            self.p2.x, self.p2.y
        )
    
    def __len__(self):
        return len(self.items)
    

    def norm(self):
        """ Returns the norm of the current vector """
        norm = np.sqrt(sum(self.arr**2))
        return norm

    def project(self, v, color='red'):
        """
        Project this vector onto v, return the projected vector
        https://www.geeksforgeeks.org/vector-projection-using-python/
            input:
                v: Vector()
            output:
                Vector()
        """
        # get the projection
        proj = (np.dot(self.arr, v.arr)/v.norm()**2)*v.arr
        # translate that projection to the origin of v
        p1 = v.p1
        p2 = Point(proj[0]+p1[0], proj[1]+p1[1])
        v_proj = Vector(p1, p2, color=color)
        return v_proj


    def draw(self):
        """
        Only supports 2D plotting for now
        """
        plt.arrow(
            self.orig[0], self.orig[1],
            self.x, self.y, 
            color = self.color,
            head_width = self.head_width, head_length = self.head_length
        )
        
