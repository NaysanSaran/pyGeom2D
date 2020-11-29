import unittest
import sys

from pygeom import Point, Line

class TestLine(unittest.TestCase):

    def test_twoPoints(self):
        p1 = Point(1, 1)
        p2 = Point(5, 4)
        l = Line(p1=p1, p2=p2)
        
        assert l.slope == 0.75, "slope should be 0.75"
        assert l.intercept == 0.25, "intercept should be 0.25"
    
    def test_pointSlope(self):
        p1 = Point(1, 1)
        slope = 0.750 
        l = Line(p=p1, slope=slope)
        
        assert l.slope == 0.75, "slope should be 0.75"
        assert l.intercept == 0.25, "intercept should be 0.25"


if __name__ == "__main__":
    unittest.main()


