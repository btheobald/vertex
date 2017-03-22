"""
Program draw module.

This module is to contain code relating to the drawing of
the simulation onto the main Tkinter Canvas or other drawing libraries.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""


from module import vtx_com
from Tkinter import *

# TODO: implement Tkinter draw functions based on data collected from calculation.

def _create_circle(canvas, cx, cy, r, **options):
    """Simplify the drawing of constant radius objects, pass on options"""
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, options)

def drawPoints(canvasObj, pointData):
    """Draw all points provided in data to provided canvas."""
    for n in range(len(pointData)):
        if pointData[n].pCharge > 0:
            fill = "orangeRed4"
            line = "red"
        else:
            fill = "deepSkyBlue3"
            line = "cyan"

        _create_circle(canvasObj, pointData[n].pPos.get(0), pointData[n].pPos.get(1), pointData[n].pRadius, fill=fill, outline=line, width=1)