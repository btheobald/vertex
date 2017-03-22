"""
Program core / startup module.

Parts of the program not relating directly to startup of the program
should be split out into appropriate modules and imported here.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
from Tkinter import *
from time import sleep

# INTERNAL MODULES
from module import vtx_calc
from module import vtx_draw
from module import vtx_gui
from module import vtx_file
from module import vtx_com

conf = {"rPerm":0.10, "dTime":2.00, "sim":"dynamic", "draw":"fieldVect", "points":0}

"""Init of point set"""
points = [
    vtx_com.PointCharge(_m=10, _c=0.1, _p=vtx_com.vecXY([100, 200])),
    vtx_com.PointCharge(_m= 1, _c=0.1, _p=vtx_com.vecXY([300, 150]) , _v=vtx_com.vecXY([-0.1, 0.030])),
]

"""Get root window handle"""
rtn = vtx_gui.initWindow()

root = rtn[0]
menu = rtn[1]
display = rtn[2]
property = rtn[3]

while True:
    sleep(0.001)
    display.delete(ALL)

    vtx_draw.drawPoints(display, points)
    vtx_calc.iterateDynamicSim(conf, points)
    vtx_gui.updateConfig(conf)

    root.update_idletasks()
    root.update()