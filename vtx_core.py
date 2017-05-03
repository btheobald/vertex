"""
Program core / startup module.

Parts of the program not relating directly to startup of the program
should be split out into appropriate modules and imported here.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
from Tkinter import *
from time import sleep
from copy import deepcopy

# INTERNAL MODULES
from module import vtx_calc
from module import vtx_draw
from module import vtx_gui
from module import vtx_com

"""Simulation Config"""
conf = {
    "rPerm":0.10,
    "dTime":1.00,
    "nPoints":0,
    "sim":0,
    "view":0
}

"""Init of point set"""
points = []
"""Backup Store"""
pointsBackup = list(points)
backupMade = False

"""Data store for field vector / line calculation results"""
calcData = None

"""Get root window handle"""
root = Tk()
root.resizable(width=False, height=False)
"""Create GUI object and pack"""
gui = vtx_gui.vertexUI(root)
gui.pack()

# Stop while on exit, prevent exception
shouldClose = False
def windowExit():
    global shouldClose
    shouldClose = True
root.protocol("WM_DELETE_WINDOW", windowExit)

check = 0

"""Main program loop"""
while not shouldClose:
    """Small delay for persistence"""
    sleep(0.0001)
    gui.display.delete(ALL)

    """Simulation Mode"""
    if conf["sim"] == 1:
        check = 1
        if backupMade == False:
            pointsBackup = deepcopy(points)
            backupMade = True
            print "backup done"
        vtx_calc.iterateDynamicSim(conf, points)
        gui.updatePoints(dyn=True, points=points)
    else:
        if check == 1:
            gui.updatePoints(dyn=True, points=pointsBackup)
            check = 0

        if backupMade == True:
            points = deepcopy(pointsBackup)
            backupMade = False
        gui.updatePoints(dyn=False, points=points)

    """UI Interaction Updates"""
    conf["nPoints"] = len(points)
    gui.updateConfig(conf)

    """Calculations and Draw"""
    if conf["view"] == 1: # Force Arrows
        vtx_calc.calculateForces(conf, points)
        vtx_draw.drawForceArrows(gui.display, points)
    elif conf["view"] == 2: # Field Vectors
        calcData=vtx_calc.calculateFieldVectorMap(conf, points)
        vtx_draw.drawFieldVectors(gui.display, calcData)
    elif conf["view"] == 3: # Field Lines
        calcData=vtx_calc.calculateFieldLines(conf, points)
        vtx_draw.drawFieldLines(gui.display, calcData)
    elif conf["view"] == 4: # Field Gradient
        calcData=vtx_calc.calculateFieldGradient(conf, points)
        vtx_draw.drawFieldGradient(gui.display, calcData)

    vtx_draw.drawPoints(gui.display, points)

    """Render and Update"""
    root.update_idletasks()
    root.update()
