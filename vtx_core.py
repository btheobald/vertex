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
from module import vtx_file
from module import vtx_com

conf = {
    "rPerm":0.10,
    "dTime":2.00,
    "nPoints":0,
    "sim":0,
    "view":0
}

"""Init of point set"""
points = []

pointsBackup = list(points)
backupMade = False

# Data store for field lines / field vectors
calcData = None

"""Get root window handle"""
root = Tk()
root.resizable(width=False, height=False)

gui = vtx_gui.vertexUI(root)
gui.pack()

while True:
    # Small delay for persistence
    sleep(0.001)
    gui.display.delete(ALL)

    # Simulation
    if conf["sim"] == 1:
        if backupMade == False:
            pointsBackup = deepcopy(points)
            backupMade = True
            print "backup done"
        vtx_calc.iterateDynamicSim(conf, points)
    else:
        if backupMade == True:
            points = deepcopy(pointsBackup)
            print "backup loaded"
            backupMade = False

    # Render / Calculations
    if conf["view"] == 1: # Force Arrows
        vtx_calc.calculateForces(conf, points)
        #vtx_draw.drawForceArrows(display, points)
    elif conf["view"] == 2: # Field Vectors
        calcData=vtx_calc.calculateFieldVectors(conf, points)
        #vtx_draw.drawFieldVectors(display, calcData)
    elif conf["view"] == 3: # Field Lines
        None

    vtx_draw.drawPoints(gui.display, points)

    # UI Interaction Updates
    conf["nPoints"] = len(points)
    gui.updatePoints(points)
    gui.updateConfig(conf)

    root.update_idletasks()
    root.update()