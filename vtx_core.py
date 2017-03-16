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
from module import vtx_file
from module import vtx_gui
from module import vtx_com

# INTEGRATION TEST MODULES
# TODO: Remove from final version.
from tests import tests_core

tests_core.module_test()

# TODO: Initialise Tkinter Window
# Initially write basic setup in this file but migrate to module/vtx_gui.py.
# TODO: Write GUI init function in vtx_gui, call here. Return window handler.
