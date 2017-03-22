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
    "mSim":0,
    "mView":0
}

"""Init of point set"""
points = [
    vtx_com.PointCharge(_m=10, _c=0.1, _p=[100, 200]),
    vtx_com.PointCharge(_m= 1, _c=0.1, _p=[300, 150], _v=[-0.1, 0.03])
]

pointsBackup = list(points)
backupMade = False

# Data store for field lines / field vectors
calcData = None

"""Get root window handle"""
rtn = vtx_gui.initWindow()

root = rtn[0]
menu = rtn[1]
display = rtn[2]
property = rtn[3]

while True:
    # Small delay for persistence
    sleep(0.001)
    display.delete(ALL)

    # Simulation
    if conf["mSim"] == 1:
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
    if conf["mView"] == 1: # Force Arrows
        vtx_calc.calculateForces(conf, points)
        #vtx_draw.drawForceArrows(display, points)
    elif conf["mView"] == 2: # Field Vectors
        calcData=vtx_calc.calculateFieldVectors(conf, points)
        #vtx_draw.drawFieldVectors(display, calcData)
    elif conf["mView"] == 3: # Field Lines
        None

    vtx_draw.drawPoints(display, points)

    # UI Updates
    conf["nPoints"] = len(points)
    vtx_gui.updateConfig(conf)

    root.update_idletasks()
    root.update()