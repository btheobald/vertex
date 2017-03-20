"""
Program core / startup module.

Parts of the program not relating directly to startup of the program
should be split out into appropriate modules and imported here.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
import Tkinter

# INTERNAL MODULES
from module import vtx_calc
from module import vtx_draw
from module import vtx_gui
from module import vtx_file
from modlue import vtx_com

main = vtx_gui.initWindow()
vMenuBar = vtx_gui.initMenuBar()
vCanvas = vtx_gui.initCanvas()
vPane = vtx_gui.initPropertiesPane()

# TODO: Setup window, menubar, canvas, pane

"""
Init program here
Setup simulation state variables, starting empty
Sent sim state to calculation/simulation core
Obtain results of calculation/simulation if view mode enabled
Send results of calculation/simulation to draw module
Check for any change to inputs if simulation is in static mode
Frame timer collection
"""

points = [
    vtx_com.PointCharge(_m=10, _c=0.1, _p=vtx_com.vecXY([100, 200])),
    vtx_com.PointCharge(_m= 1, _c=0.1, _p=vtx_com.vecXY([300, 150]) , _v=vtx_com.vecXY([-0.1, 0.030])),
]

while True:

    # How we want do to draw particles
    #vtx_calc.drawPoints(vCanvas, points)

    main.update_idletasks()
    main.update()
