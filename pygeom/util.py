import numpy as np
import math

def distance(p1, p2):
    """
    Eucludean distance between two 2D points
        p1: Point()
        p2: Point()
    """
    ssq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    return np.sqrt(ssq)


def rotate(x, y, beta):
    """
    Rotate vector(x,y) by beta radians counterclockwise
    https://matthew-brett.github.io/teaching/rotation_2d.html
    """
    x2 = math.cos(beta)*x - math.sin(beta)*y
    y2 = math.sin(beta)*x + math.cos(beta)*y
    return (x2, y2)


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


