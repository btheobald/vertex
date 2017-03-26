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

def getStrengthColour(strength, rangeFac=1):
    if (strength <= -5.00 * rangeFac):
        return "#0099d1"
    elif (strength > -5.00 * rangeFac) and (strength <= -3.00 * rangeFac):
        return "#00b1d1"
    elif (strength > -3.00 * rangeFac) and (strength <= -2.50 * rangeFac):
        return "#00c6d1"
    elif (strength > -2.50 * rangeFac) and (strength <= -2.00 * rangeFac):
        return "#00d1b1"
    elif (strength > -2.00 * rangeFac) and (strength <= -1.50 * rangeFac):
        return "#00eade"
    elif (strength > -1.50 * rangeFac) and (strength <= -1.00 * rangeFac):
        return "#00eaab"  
    elif (strength > -1.00 * rangeFac) and (strength <= -0.50 * rangeFac):
        return "#00ea84"
    elif (strength > -0.50 * rangeFac) and (strength <= -0.25 * rangeFac):
        return "#00ea3e"
    elif (strength > -0.25 * rangeFac) and (strength <= -0.05 * rangeFac):
        return "#36ea00"      
    elif (strength > -0.05 * rangeFac) and (strength <= 0.05 * rangeFac):
        return "#61ea00"
    elif (strength > 0.05 * rangeFac) and (strength <= 0.25 * rangeFac):
        return "#8cea00" 
    elif (strength > 0.25 * rangeFac) and (strength <= 0.50 * rangeFac):
        return "#d6ea00"
    elif (strength > 0.50 * rangeFac) and (strength <= 1.00 * rangeFac):
        return "#eae600"
    elif (strength > 1.00 * rangeFac) and (strength <= 1.50 * rangeFac):
        return "#eaca00"
    elif (strength > 1.50 * rangeFac) and (strength <= 2.00 * rangeFac):
        return "#eab300"
    elif (strength > 2.00 * rangeFac) and (strength <= 2.50 * rangeFac):
        return "#ea9800"
    elif (strength > 2.50 * rangeFac) and (strength <= 3.00 * rangeFac):
        return "#ea6d00"
    elif (strength > 3.00 * rangeFac) and (strength <= 5.00 * rangeFac):
        return "#ea5100"
    elif (strength > 5.00 * rangeFac):
        return "#ea2600"

def drawFieldVectors(canvasObj, calcRes):
    for x in range(len(calcRes)):
        for y in range(len(calcRes[x])):
            fillS = getStrengthColour(calcRes[x][y][4], 0.005)
            canvasObj.create_line(calcRes[x][y][0],
                                  calcRes[x][y][1],
                                  calcRes[x][y][2],
                                  calcRes[x][y][3], fill=fillS, arrow=LAST, arrowshape=(4, 4, 2), width=1)

def drawFieldGradient(canvasObj, calcRes):
    for x in range(len(calcRes)):
        for y in range(len(calcRes[x])):
            fillS = getStrengthColour(calcRes[x][y][2], 0.005)
            canvasObj.create_rectangle(calcRes[x][y][0]-2,
                                       calcRes[x][y][1]-2,
                                       calcRes[x][y][0]+2,
                                       calcRes[x][y][1]+2, fill=fillS, width=0)
            
def drawFieldLines(canvasObj, calcRes):
  for i in range(len(calcRes)):
    for l in range(len(calcRes[i])-1):
      canvasObj.create_line(calcRes[i][l][0].get(0),
                            calcRes[i][l][0].get(1),
                            calcRes[i][l+1][0].get(0),
                            calcRes[i][l+1][0].get(1), fill="grey", width=1)
