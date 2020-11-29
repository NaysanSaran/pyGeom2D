import matplotlib.pyplot as plt
import numpy as np


class Segment():
    """
    Segment(p1,p2)
        p1: Point()
        p2: Point()
    """
    def __init__(self, p1, p2, color='#696969', linewidth=1, linestyle='-'):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.items = [p1,p2]
        self.len = 2
        
    def __getitem__(self, index):
        return self.items[index]
    
    def __str__(self):
        return "Segment(%s,%s)" % (self.p1, self.p2)
    
    def __repr__(self):
        return "Segment(%s,%s)" % (self.p1, self.p2)
    
    def __len__(self):
        return self.len
    
    def draw(self):
        x_values = [self.p1[0], self.p2[0]] # Gather x values
        y_values = [self.p1[1], self.p2[1]] # Gatner y values
        plt.plot(
            x_values, 
            y_values, 
            color=self.color, 
            linewidth=self.linewidth,
            linestyle=self.linestyle
        )

