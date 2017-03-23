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
import glfw
from OpenGL.GL import *

# INTERNAL MODULES
from module import vtx_calc
from module import vtx_draw
from module import vtx_gui
from module import vtx_com

def glfwWindowInit():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(400, 400, "Vertex", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    return window

def initDisplay(lXRes, lYRes):
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity();
  glOrtho(-lXRes, lXRes, -lYRes, lYRes, 1.0, -1.0)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  glViewport(0, 0, lXRes, lYRes)
  glClearColor(0.0, 0.0, 0.0, 1)

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
root.wm_title("Vertex")
root.resizable(width=False, height=False)
"""Create GUI object and pack"""
gui = vtx_gui.vertexUI(root)
gui.pack()

window = glfwWindowInit()
glfw.make_context_current(window)
initDisplay(400, 400)

"""Main program loop"""
while not glfw.window_should_close(window):
    """Small delay for persistence"""
    sleep(0.0001)
    #gui.display.delete(ALL)

    """Simulation Mode"""
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

    """Calculations and Draw"""
    if conf["view"] == 1: # Force Arrows
        vtx_calc.calculateForces(conf, points)
        #TODO: Draw force arrows on points.
    elif conf["view"] == 2: # Field Vectors
        calcData=vtx_calc.calculateFieldVectors(conf, points)
        #TODO: Draw field vectors.
    elif conf["view"] == 3: # Field Lines
        pass #TODO: Implement field lines.
    #vtx_draw.drawPoints(gui.display, points)

    """UI Interaction Updates"""
    conf["nPoints"] = len(points)
    gui.updatePoints(points)
    gui.updateConfig(conf)

    """Render and Update"""
    glfw.swap_buffers(window)
    glfw.poll_events()
    root.update_idletasks()
    root.update()

glfw.terminate()