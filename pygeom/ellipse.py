import sys
import matplotlib.pyplot as plt
import numpy as np
import math

from scipy import stats
import matplotlib.patches as patches
import matplotlib.transforms as transforms

from .point import Point
from .vector import Vector
from .util import rotate


class Ellipse():

    def __init__(self, mu, sigma, ci=0.95, color='#4ca3dd'):
        self.mu     = mu
        self.sigma  = sigma
        self.ci     = ci
        self.color  = color
        self.chi2   = None
        self.set_chisquare()
        self.set_axes()
        self.set_vectors()


    def __str__(self):
        return "Ellipse(%s,%s)" % (self.mu, self.sigma)

    def __repr__(self):
        return "Ellipse(%s,%s)" % (self.mu, self.sigma)

    def set_chisquare(self):
        """
        Upper-tail critical values of chi-square distribution with 2 degrees of freedom
        """
        if self.ci == 0.90:
            self.chi2 = 4.605
        elif self.ci == 0.95:
            self.chi2 = 5.991
        elif self.ci == 0.975:
            self.chi2 = 7.378
        else:
            self.chi2 = 5.991
    
    
    def set_axes(self):
        """
        Set the minor, major axes as well as the alpha angle
        Also set the eigenvalues and eigenvectors of the covariance matrix
        https://www.math.ubc.ca/~pwalls/math-python/linear-algebra/eigenvalues-eigenvectors/
        """
        # Eigeinvalues and corresponding eigenvectors
        # of the covariance matrix
        eig_val, eig_vec = np.linalg.eig(self.sigma)
        # Sort the eigenvalues by descending order
        self.eigs = [(np.abs(eig_val[i]), eig_vec[:,i]) for i in range(len(eig_val))]
        self.eigs.sort(key=lambda x: x[0], reverse=True)
    
        # semi-major and semi-minor axes length
        self.semi_major = math.sqrt(self.eigs[0][0]*self.chi2)
        self.semi_minor = math.sqrt(self.eigs[1][0]*self.chi2)
    
        # Get the eigenvector associated to the largest eigenvalue
        vec = self.eigs[0][1]
        # The ellipse orientation is the arctan of that vector y/x
        self.alpha = np.arctan(vec[1]/vec[0])



    def set_vectors(self):
        """
        Create the major and minor axis vectors
        """
        # Start at the origin
        major = np.array([1, 0]) * self.semi_major
        minor = np.array([0, 1]) * self.semi_minor
        # Rotate by alpha
        major = rotate(major[0], major[1], self.alpha)
        minor = rotate(minor[0], minor[1], self.alpha)
        # Translate by mu
        mu = Point(self.mu[0], self.mu[1])
        ma = Point(major[0]+self.mu[0], major[1]+self.mu[1])
        mi = Point(minor[0]+self.mu[0], minor[1]+self.mu[1])
        self.v_major = Vector(mu, ma, color=self.color)
        self.v_minor = Vector(mu, mi, color=self.color)


    def draw(self, ax):

        ellipse = patches.Ellipse(
            (0, 0), 
            width=1, 
            height=1, 
            facecolor=self.color, 
            alpha=0.2
        )
        transf  = transforms.Affine2D() \
            .scale(self.semi_major*2., self.semi_minor*2.) \
            .rotate(self.alpha) \
            .translate(self.mu[0], self.mu[1])

        ellipse.set_transform(transf + ax.transData)
        return ax.add_patch(ellipse)


