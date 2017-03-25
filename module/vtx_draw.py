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
    if (strength <= -1.40 * rangeFac):
        return "#0000ff"
    elif (strength > -1.40 * rangeFac) and (strength <= -1.20 * rangeFac):
        return "#1100ee"
    elif (strength > -1.20 * rangeFac) and (strength <= -1.00 * rangeFac):
        return "#2200dd"
    elif (strength > -1.00 * rangeFac) and (strength <= -0.80 * rangeFac):
        return "#3300cc"
    elif (strength > -0.80 * rangeFac) and (strength <= -0.60 * rangeFac):
        return "#4400bb"
    elif (strength > -0.60 * rangeFac) and (strength <= -0.40 * rangeFac):
        return "#5500aa"
    elif (strength > -0.40 * rangeFac) and (strength <= -0.20 * rangeFac):
        return "#660099"
    elif (strength > -0.20 * rangeFac) and (strength <= -0.10 * rangeFac):
        return "#770088"
    elif (strength > -0.10 * rangeFac) and (strength <= 0.10 * rangeFac):
        return "#000000"
    elif (strength > 0.10 * rangeFac) and (strength <= 0.20 * rangeFac):
        return "#880077"
    elif (strength > 0.20 * rangeFac) and (strength <= 0.40 * rangeFac):
        return "#990066"
    elif (strength > 0.40 * rangeFac) and (strength <= 0.60 * rangeFac):
        return "#aa0055"
    elif (strength > 0.60 * rangeFac) and (strength <= 0.80 * rangeFac):
        return "#bb0044"
    elif (strength > 0.80 * rangeFac) and (strength <= 1.00 * rangeFac):
        return "#cc0033"
    elif (strength > 1.00 * rangeFac) and (strength <= 1.20 * rangeFac):
        return "#dd0022"
    elif (strength > 1.20 * rangeFac) and (strength <= 1.40 * rangeFac):
        return "#ee0011"
    elif (strength > 1.40 * rangeFac):
        return "#ff0000"

def drawFieldVectors(canvasObj, calcRes):
    for x in range(len(calcRes)):
        for y in range(len(calcRes[x])):
            fillS = getStrengthColour(calcRes[x][y][4])
            canvasObj.create_line(calcRes[x][y][0], calcRes[x][y][1], calcRes[x][y][2], calcRes[x][y][3], fill=fillS, arrow=LAST, arrowshape=(4, 4, 2), width=1)

def drawFieldGradient(canvasObj, calcRes):
    for x in range(len(calcRes)):
        for y in range(len(calcRes[x])):
            fillS = getStrengthColour(calcRes[x][y][2])
            canvasObj.create_rectangle(calcRes[x][y][0]-3, calcRes[x][y][1]-3, calcRes[x][y][0]+3, calcRes[x][y][1]+3, fill=fillS, width=0)