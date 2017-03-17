"""
Program core / startup module.

Parts of the program not relating directly to startup of the program
should be split out into appropriate modules and imported here.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
from Tkinter import *

# INTERNAL MODULES
from module import vtx_calc
from module import vtx_draw
from module import vtx_gui
from module import vtx_file

main = vtx_gui.initWindow()

while True:
    main.update_idletasks()
    main.update()
