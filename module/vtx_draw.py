"""
Program draw module.

This module is to contain code relating to the drawing of
the simulation onto the main Tkinter Canvas or other drawing libraries.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""


from module import vtx_com
from Tkinter import *
from math import *

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

def drawForceArrows(canvasObj, pointData):
    for n in range(len(pointData)):
        xy0 = pointData[n].pPos.get()
        xyD = pointData[n].pNetF.get()
        angle = atan2(xyD[1], xyD[0])
        xyP = [xy0[0]+25*cos(angle), xy0[1]+25*sin(angle)]

        canvasObj.create_line(xy0[0], xy0[1], xyP[0], xyP[1], fill="green", arrow=LAST, arrowshape=(8,8,3), width=3)

        for i in range(len(pointData[n].pIdvF)):
            xy0 = pointData[n].pPos.get()
            xyD = pointData[n].pIdvF[i].get()
            angle = atan2(xyD[1], xyD[0])
            xyP = [xy0[0]+20*cos(angle), xy0[1]+20*sin(angle)]

            canvasObj.create_line(xy0[0], xy0[1], xyP[0], xyP[1], fill="purple", arrow=LAST, arrowshape=(4,4,2), width=1)

def getStrengthColour(strength, rangeFac=0.1):
    if (strength <= -5.00 * rangeFac):
        return "#0099d1"
    elif (strength > -5.00 * rangeFac) and (strength <= -3.00 * rangeFac):
        return "#00b1d1"
    elif (strength > -3.00 * rangeFac) and (strength <= -2.50 * rangeFac):
        return "#00c6d1"
    elif (strength > -2.50 * rangeFac) and (strength <= -2.00 * rangeFac):
        return "#00d1b1"
    elif (strength > -2.00 * rangeFac) and (strength <= -1.50 * rangeFac):
        return "#00d18e"
    elif (strength > -1.50 * rangeFac) and (strength <= -1.00 * rangeFac):
        return "#00d16b"  
    elif (strength > -1.00 * rangeFac) and (strength <= -0.50 * rangeFac):
        return "#00d13e"
    elif (strength > -0.50 * rangeFac) and (strength <= -0.25 * rangeFac):
        return "#22d100"
    elif (strength > -0.25 * rangeFac) and (strength <= -0.05 * rangeFac):
        return "#68d100"      
    elif (strength > -0.05 * rangeFac) and (strength <= 0.05 * rangeFac):
        return "#92d100"
    elif (strength > 0.05 * rangeFac) and (strength <= 0.25 * rangeFac):
        return "#9cd100" 
    elif (strength > 0.25 * rangeFac) and (strength <= 0.50 * rangeFac):
        return "#aed100"
    elif (strength > 0.50 * rangeFac) and (strength <= 1.00 * rangeFac):
        return "#bcd100"
    elif (strength > 1.00 * rangeFac) and (strength <= 1.50 * rangeFac):
        return "#d1c300"
    elif (strength > 1.50 * rangeFac) and (strength <= 2.00 * rangeFac):
        return "#d1ae00"
    elif (strength > 2.00 * rangeFac) and (strength <= 2.50 * rangeFac):
        return "#a87000"
    elif (strength > 2.50 * rangeFac) and (strength <= 3.00 * rangeFac):
        return "#a95200"
    elif (strength > 3.00 * rangeFac) and (strength <= 5.00 * rangeFac):
        return "#aa2500"
    elif (strength > 5.00 * rangeFac):
        return "#aa0000"

def drawFieldVectors(canvasObj, calcRes):
    for x in range(len(calcRes)):
        for y in range(len(calcRes[x])):
            fillS = getStrengthColour(calcRes[x][y][4])
            canvasObj.create_line(calcRes[x][y][0], calcRes[x][y][1], calcRes[x][y][2], calcRes[x][y][3], fill=fillS, arrow=LAST, arrowshape=(4, 4, 2), width=1)

def drawFieldGradient(canvasObj, calcRes):
    for x in range(len(calcRes)):
        for y in range(len(calcRes[x])):
            fillS = getStrengthColour(calcRes[x][y][2], 0.01)
            canvasObj.create_rectangle(calcRes[x][y][0]-2, calcRes[x][y][1]-2, calcRes[x][y][0]+2, calcRes[x][y][1]+2, fill=fillS, width=0)
