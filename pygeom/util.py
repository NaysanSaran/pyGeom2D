import math
import numpy as np

from fractions import Fraction



def midpoint(p1, p2):
    """
    Returns the (x, y) location of the midpoint between p1 and p2
    """
    x = 0.5*(p1[0] + p2[0])
    y = 0.5*(p1[1] + p2[1])
    return (x, y)


def distance(p1, p2):
    """
    Eucludean distance between two 2D points
        p1: Point()
        p2: Point()
    """
    ssq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    return np.sqrt(ssq)


def rotate(vec, theta):
    """
    Rotate vector(x,y) by theta radians counterclockwise
    """
    # rotation matrix
    A = np.array([
        [math.cos(theta), -math.sin(theta)],
        [math.sin(theta),  math.cos(theta)]
    ])
    v = A.dot(vec)
    return v


def translate(vec, transv):
    """
    Translate vector vec(x,y) by vector transv(tx, ty)
    """
    v = np.array([vec[0] + transv[0], vec[1] + transv[1]])
    return v


def get_chisquare(ci):
    """
    Upper-tail critical values of chi-square distribution
    with 2 degrees of freedom
    """
    if ci == 0.90:
        return 4.605
    elif ci == 0.95:
        return 5.991
    elif ci == 0.975:
        return 7.378
    else:
        return 5.991


def update_sigma(old_sigma, s_major, s_minor, ci=0.975):
    """
    Get a new covariance matrix from
        old_sigma: old covariance matrix
        s_major: updated semi-major axis
        s_minor: updated semi-minor axis
    """
    # update the eigenvalues
    l1 = (s_major**2)/get_chisquare(ci)
    l2 = (s_minor**2)/get_chisquare(ci)

    # Recover P matrix from the eigenvectors
    P = np.linalg.eig(old_sigma)[1]
    # Diagonal matrix of the new eigenvectors
    D = np.diag((l1, l2))
    # Updated covariance matrix
    cov = np.matmul(P, D)
    cov = np.matmul(cov, np.linalg.inv(P))
    return cov


def get_axes_arrow_shape(xlim, ylim):
    """
    Scale the Axes arrows according to the limits of the axes
    """
    Dx = xlim[1] - xlim[0]
    Dy = ylim[1] - ylim[0]

    # arrow length, x-axis arrow width and y-axis arrow width
    diag  = math.sqrt(math.pow(Dx, 2) + math.pow(Dy, 2))
    leng  = diag/50. 
    width = min(Dx/50., Dy/50.)

    # x-axis and y-axis arrow coordinates
    x_arr = np.array([
        [xlim[1]+2*leng,  0], 
        [xlim[1]+1*leng,  0.5*width], 
        [xlim[1]+1*leng, -0.5*width]
    ])
    y_arr = np.array([
        [ 0        , ylim[1]+2*leng], 
        [-0.5*width, ylim[1]+1*leng], 
        [ 0.5*width, ylim[1]+1*leng]
    ])
    return x_arr, y_arr



def get_theta(x, y, rad=True):
    """
    Get the angle between the x-axis and the point P(x,y)
    """
    theta = math.atan2(y,x)
    if rad == False:
        theta = math.degrees(theta) 
    return theta


def pprint_float(x, digits=3):
    """ 
    Return float as fraction, if it looks good.
    Otherwise keep the float
    """
    if x == int(x):
        return str(int(x))
    
    f = Fraction(x)
    
    if len(str(f.numerator)) < 7:
        s = "%s/%s" % (f.numerator, f.denominator)
    else:
        s = str(np.around(x, digits))
    return s


def get_text_location(x, y, xlim, ylim, loc):
    """
    Get text (x,y) coordinates depending on the loc parameter
    """
    dx = 0.04 * (xlim[1] - xlim[0])
    dy = 0.04 * (ylim[1] - ylim[0])

    if loc == 'up':
        tx = x
        ty = y + dy
    elif loc == 'down':
        tx = x
        ty = y - dy
    elif loc == 'left':
        tx = x - dx
        ty = y
    elif loc == 'right':
        tx = x + dx
        ty = y
    else:
        raise Exception("Unsupported value for loc: '%s' % loc")
    return tx, ty




