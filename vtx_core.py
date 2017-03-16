"""
Program core / startup module.

Parts of the program not relating directly to startup of the program
should be split out into appropriate modules and imported here.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# IMPORTS
import vtx_pcom
import vtx_calc
import vtx_draw
import vtx_file
import vtx_ifce

# TEST MODULES
# TODO: Remove from final version.
import vtx_test

vtx_test.module_test()

