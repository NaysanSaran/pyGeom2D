# pyGeom2D

Python package to create 2D geometries.

# Getting Started

## Installation

```sh
pip install pyGeom2D
```

# Usage Examples

## Cartesian coordinate axes + points

```python
from pygeom import Axes, Point

# Create the cartesian axis
axes = Axes(xlim=(-1,8), ylim=(-1,18), figsize=(9,7))

# Create two points
p1 = Point(2,  5, color='#ffa500')
p2 = Point(7, 17, color='#0000ff')

axes.addMany([p1, p2])
axes.draw()
```

<img src="./img/python_cartesian_axis_points.png" />


## Line Demo

```python
from pygeom import Axes, Point, Line

# Create the cartesian axis
axes = Axes(xlim=(-1,7), ylim=(-1,7), figsize=(7,6))

# Points
p1 = Point(1, 1, color='red')
p2 = Point(5, 4, color='green')

l = Line(p1=p1, p2=p2)

axes.addMany([p1, p2, l])
axes.draw("line_demo.png")
```

<img src="./img/line_2points.png" />


## Triangle Demo

```python
from pygeom import Axes, Point, Triangle

# Create the cartesian axis
axes = Axes(xlim=(-1,10), ylim=(-1,10), figsize=(12,10))

# Points
p1 = Point(1, 1, color='grey')
p2 = Point(5, 5, color='grey')
p3 = Point(8, 5, color='grey')

tr = Triangle(p1, p2, p3, alpha=0.5)

axes.addMany([p1, p2, p3])
axes.add(tr)
axes.draw()
```

<img src="./img/triangle.png" />



## Rectangle Demo

```python
from pygeom import Axes, Point, Rectangle

# Create the cartesian axis
axes = Axes(xlim=(-1,7), ylim=(-1,7), figsize=(12,10))

# Points
bottomLeft = Point(1, 1, color='red')
topRight = Point(5, 4, color='green')

shape = Rectangle(bottomLeft, topRight, alpha=0.5)

axes.addMany([bottomLeft, topRight])
axes.add(shape)
axes.draw()
```

<img src="./img/rectangle.png" />



## Polygon Demo

```python
from pygeom import Axes, Point, Polygon

# Create the cartesian axis
axes = Axes(xlim=(-1,10), ylim=(-1,10), figsize=(12,10))

# Points
p1 = Point(1, 1, color='red')
p2 = Point(1, 2, color='green')
p3 = Point(4, 7, color='red')
p4 = Point(9, 1, color='green')


shape = Polygon([p1, p2, p3, p4], alpha=0.5)

axes.addMany([p1, p2, p3, p4])
axes.add(shape)
axes.draw()
```

<img src="./img/polygon.png" />



