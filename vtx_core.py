"""
Program core / startup module.

Parts of the program not relating directly to startup of the program
should be split out into appropriate modules and imported here.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
from Tkinter import *
from time import sleep
from time import time
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
    "fpsc":0,
    "sim":0,
    "view":0
}

"""Init of point set"""
points = []
"""State var"""
init = 0
"""Backup Store"""
pointsBackup = list(points)
backupMade = False

"""Data store for field vector / line calculation results"""
calcData = None

"""FPS counter var"""
currentInterval = time()
framesInInterval = 0
currentFPS = 0

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

"""Main program loop"""
while not shouldClose:
    """Small delay for persistence"""
    gui.display.delete(ALL)

    """Simulation Mode"""
    if conf["sim"] == 1:
        """Dynamic"""
        init = 1
        if backupMade == False:
            """Make initial points backup"""
            pointsBackup = deepcopy(points)
            backupMade = True
            print "backup done"
        """Iterate sim"""
        vtx_calc.iterateDynamicSim(conf, points)
        """Update gui points store"""
        gui.updatePoints(dyn=True, points=points)
    else:
        """Static"""
        if init == 1:
            """When first switched, update gui store with backup"""
            gui.updatePoints(dyn=True, points=pointsBackup)
            init = 0

        if backupMade == True:
            """Update sim store from backup"""
            points = deepcopy(pointsBackup)
            backupMade = False
        """Update gui points store"""
        gui.updatePoints(dyn=False, points=points)

    """Modes selections"""
    if conf["view"] == 1: # Force Arrows
        """Force arrows"""
        vtx_calc.calculateForces(conf, points)
        vtx_draw.drawForceArrows(gui.display, points)
    elif conf["view"] == 2: # Field Vectors
        """Field vector map"""
        calcData=vtx_calc.calculateFieldVectorMap(conf, points)
        vtx_draw.drawFieldVectors(gui.display, calcData)
    elif conf["view"] == 3: # Field Lines
        """Field lines"""
        calcData=vtx_calc.calculateFieldLines(conf, points)
        vtx_draw.drawFieldLines(gui.display, calcData)
    elif conf["view"] == 4: # Field Gradient
        """Field gradient"""
        calcData=vtx_calc.calculateFieldGradient(conf, points)
        vtx_draw.drawFieldGradient(gui.display, calcData)

    """Draw points"""
    vtx_draw.drawPoints(gui.display, points, int(gui.pointVal["pSelect"].get()))

    if conf["fpsc"]:
        """FPS counter"""
        if time() > (currentInterval + 2):
            currentInterval = time()
            currentFPS = (framesInInterval + 1) / 2
            if (currentFPS > 60):
                currentFPS = 60
            framesInInterval = 0
        else:
            framesInInterval += 1
        """Render FPS counter"""
        vtx_draw.drawFPSCounter(gui.display, currentFPS)

    """UI Interaction Updates"""
    conf["nPoints"] = len(points)
    gui.updateConfig(conf)

    """Render and Update"""
    root.update_idletasks()
    root.update()
