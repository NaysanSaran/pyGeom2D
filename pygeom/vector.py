import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .point import Point
from .util import get_theta, pprint_float, rotate, translate
from .util import midpoint, get_text_location


class Vector():
    """
    Vector(p1, p2)
        p1: Point()
        p2: Point()
    """
    def __init__(self, p1, p2, **kwargs):

        self.p1     = Point(p1[0], p1[1])
        self.p2     = Point(p2[0], p2[1])
        self.items  = [self.p1, self.p2]
        self.x      = self.p2[0] - self.p1[0]
        self.y      = self.p2[1] - self.p1[1]
        self.arr    = np.array([self.x, self.y])

        self.get_norm()

        # Vector styling
        self.styling_defaults = {
            'linewidth' : 1, 
            'linestyle' : '-',
            'color'     : '#6897bb',
            'zorder'    : 5,
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
        return "Vector(%s, %s) from (%s, %s) to (%s, %s)" % (
            pprint_float(self.x), pprint_float(self.y),
            pprint_float(self.p1.x, digits=2), pprint_float(self.p1.y, digits=2),
            pprint_float(self.p2.x, digits=2), pprint_float(self.p2.y, digits=2)
        )
    

    def __repr__(self):
        return self.__str__()

    
    def __len__(self):
        return len(self.items)
    

    def __add__(self, v):
        """ 
        Performs vector addition 
        """
        if type(v).__name__ != 'Vector' or len(v) != 2:
            raise Exception("Can only add vector to another vector of the same size")

        p = translate([self.x + v.x, self.y + v.y], self.p1)
        new_v = Vector(self.p1, p)
        new_v.copy_style(self)
        
        # If both vectors have labels, create a label for the sum
        if self.label is not None and v.label is not None:
            new_v.label = '%s + %s' % (self.label, v.label)
        return new_v
            

    def __sub__(self, v):
        """ 
        Performs vector subtraction
        """
        if type(v).__name__ != 'Vector' or len(v) != 2:
            raise Exception("Can only add vector to another vector of the same size")

        p = translate([self.x - v.x, self.y - v.y], self.p1)
        new_v = Vector(self.p1, p)
        new_v.copy_style(self)

        # If both vectors have labels, create a label for the sum
        if self.label is not None and v.label is not None:
            new_v.label = '%s - %s' % (self.label, v.label)
        return new_v


    def __rmul__(self, value):
        """ 
        Performs scalar * vector right-multiplication
        """
        try: 
            a = float(value)
        except:
            raise Exception("Can only multiply a vector with a scalar")

        p = translate([a*self.x, a*self.y], self.p1)
        new_v = Vector(self.p1, p)
        new_v.copy_style(self)

        # Add a label if the intial vector had a label
        if self.label is not None:
            if '+' in self.label or '-' in self.label:
                new_v.label = '%s * (%s)' % (pprint_float(a), self.label)
            else:
                new_v.label = '%s * %s' % (pprint_float(a), self.label)
        return new_v


    def __mul__(self, value):
        """ 
        Performs vector scalar multiplication
        """
        return self.__rmul__(value)


    def __neg__(self):
        """
        Overrides unary - operator
        """
        p1 = self.p1
        p2 = Point(self.p1.x - self.x, self.p1.y - self.y)
        v = Vector(p1, p2)
        v.copy_style(self)
        if self.label is not None:
            v.label = '- %s' % self.label
        return v 


    def copy_style(self, v):
        """
        Copy the same styling as vector v
        """
        for param in self.styling_defaults.keys():
            setattr(self, param, getattr(v, param))


    def get_norm(self):
        """ Returns the norm of the current vector """
        self.norm = float(np.sqrt(sum(self.arr**2)))
        return self.norm


    def get_unit_vector(self):
        """
        Returns a unit vector associated with this one
        """
        v = (1./self.norm)*self
        return v


    def dot(self, v):
        """
        Dot (scalar) product between this vector the vector v in parameter
        """
        d = self.x * v.x + self.y * v.y
        return d


    def get_midpoint(self, **kwargs):
        """ Returns the midpoint of this vector """
        p = Point(
            0.5*(self.p1.x + self.p2.x), 
            0.5*(self.p1.y + self.p2.y),
            **kwargs
        )
        return p


    def get_angle(self, v, rad=False):
        """
        Returns the angle between this vector and vector v in parameter
        """
        cos_theta = self.dot(v) / (self.norm * v.norm)
        theta = math.acos(cos_theta)
        if rad == False:
            theta = math.degrees(theta)
        return theta


    def is_perpendicular(self, v):
        """
        Returns True if this vector is perpendicular (normal) to the vector v
        """
        if self.dot(v) == 0:
            return True
        return False


    def is_parallel(self, v):
        """
        Returns True if this vector is parallel to the vector v
        """
        if self.get_angle(v) % 180 == 0:
            return True
        return False


    def project_onto(self, v):
        """
        Returns the projection of this vector onto the vector v
        """
        proj = self.norm * math.cos(self.get_angle(v, rad=True))
        proj = proj * v.get_unit_vector()
        proj.needs_square_axes = True
        return proj


    def get_parallel(self, norm=None, start=None, end=None, **kwargs):
        """
        Returns a vector parallel to this vector.
        Start or end points of the new vector can be specified,
        otherwise the vector will start at (0,0)
        """
        # If no norm is speficied, use this vector's norm for the parallel vector
        if norm is None:
            norm = self.norm

        if start is not None and end is not None:
            raise Exception("Either start or end can be specified, but not both")
        elif start is not None:
            p1 = start
            p2 = Point(start.x + self.x, start.y + self.y)
        elif end is not None:
            p1 = Point(end.x - self.x, end.y - self.y)
            p2 = end
        else:
            p1 = Point(0,0)
            p2 = Point(self.x, self.y)
        # build vector
        v = Vector(p1, p2, **kwargs).get_unit_vector()
        v = norm * v
        v.label = kwargs.get('label', None)
        v.needs_square_axes = True
        return v


    def get_perpendicular(self, norm=None, start=None, end=None, **kwargs):
        """
        Returns a vector perpendicular to this vector.
        Start or end points of the new vector can be specified,
        otherwise the vector will start at (0,0)
        """
        # If no norm is speficied, use this vector's norm for the parallel vector
        if norm is None:
            norm = self.norm

        # First we can create a simple vector that we know will be normal to this one
        if self.y == 0:
            v = Vector(Point(0,0), Point(0,1))
        else:
            v = Vector(Point(0,0), Point(-1, self.x/self.y))

        # Next, move the vector according to any speficied start and end points
        if start is not None and end is not None:
            raise Exception("Either start or end can be specified, but not both")
        elif start is not None:
            p1 = start
            p2 = Point(start.x + v.x, start.y + v.y)
        elif end is not None:
            p1 = Point(end.x - v.x, end.y - v.y)
            p2 = end
        else:
            p1 = v.p1
            p2 = v.p2

        # build vector
        v = Vector(p1, p2, **kwargs).get_unit_vector()
        v = norm * v
        v.label = kwargs.get('label', None)
        v.needs_square_axes = True
        return v


    def __get__arrow__head__(self, ax, xlim, ylim):
        """ Vector arrow head as a triangle """
        dx = 0.015*(xlim[1]-xlim[0])
        dy = 0.007*(ylim[1]-ylim[0])
        arrow_head = [[0, 0], [-dx, -dy], [-dx, dy]]
        arrow_head = [rotate(v, math.radians(self.theta)) for v in arrow_head]
        arrow_head = [translate(v, [self.p2.x, self.p2.y]) for v in arrow_head]
        return arrow_head


    def draw(self, ax, xlim, ylim):
        """
        Only supports 2D plotting for now
        """
        # angle to rotate the arrow head so it is aligned with the vector
        # also depends on subplot size
        dx = self.x * ax.bbox.width
        dy = self.y * ax.bbox.height
        self.theta = get_theta(dx, dy, rad=False)

        # Draw the vector first as a segment
        ax.plot(
            [self.p1.x, self.p2.x], 
            [self.p1.y, self.p2.y],
            color       = self.color,
            linewidth   = self.linewidth,
            linestyle   = self.linestyle,
            zorder      = self.zorder
        )

        # Then add the arrow head as a triangle
        arrow_head = self.__get__arrow__head__(ax, xlim, ylim)
        self.arrow_head = patches.Polygon(arrow_head, color=self.color)
        ax.add_patch(self.arrow_head)

        # Also add the text if needed
        if self.label is not None:

            # text x,y location
            if self.x == 0:
                self.loc = 'left'
            x, y = midpoint(self.p1, self.p2)
            tx, ty  = get_text_location(x, y, xlim, ylim, self.loc)

            # add text at midpoint between p1 and p2
            if dx < 0 and dy > 0:
                theta = self.theta - 180
            elif dx > 0 and dy < 0:
                theta = self.theta
            else:
                theta = self.theta % 180

            ax.text(
                tx, ty, self.label, color=self.color, rotation=theta, fontsize=12,
                ha='center', va='center'
            )


