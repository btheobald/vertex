"""
Program draw module.

This module is to contain code relating to the drawing of
the simulation onto the main Tkinter Canvas or other drawing libraries.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""


from module import vtx_com
from Tkinter import *
from math import *
from OpenGL.GL import *

# TODO: implement Tkinter draw functions based on data collected from calculation.

def _create_circle(canvas, cx, cy, r, **options):
    """Simplify the drawing of constant radius objects, pass on options"""
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, options)

#def drawPoints(canvasObj, pointData):
def drawPoints(pointData):
    """Draw all points provided in data to provided canvas."""
    for n in range(len(pointData)):
        """
        if pointData[n].pCharge > 0:
            fill = "orangeRed4"
            line = "red"
        else:
            fill = "deepSkyBlue3"
            line = "cyan"
        """
        #_create_circle(canvasObj, pointData[n].pPos.get(0), pointData[n].pPos.get(1), pointData[n].pRadius, fill=fill, outline=line, width=1)
        drawPoint(pointData[n])

def drawPoint(point=vtx_com.PointCharge()):
    segments = 64

    theta = 2 * pi / segments
    tanFact = tan(theta)
    radFact = cos(theta)

    posX = point.pPos.get(0)
    posY = point.pPos.get(1)

    x = point.pRadius
    y = 0

    if point.pCharge > 0:
        fill = [1.0, 0.2, 0.2]
    else:
        fill = [0.2, 0.4, 1.0]

    glColor3f(fill[0], fill[1], fill[2])
    glBegin(GL_POINTS)
    glVertex2f(posX,  posY)
    glEnd()

    glBegin(GL_POLYGON)
    for n in range(segments):
        glVertex2f(x + posX, y + posY)

        lx = -y
        ly =  x

        x += lx * tanFact
        y += ly * tanFact

        x *= radFact
        y *= radFact
    glEnd()
