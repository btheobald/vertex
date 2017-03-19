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

main = vtx_gui.initWindow()
vMenuBar = vtx_gui.initMenuBar()
vCanvas = vtx_gui.initCanvas()
vPane = vtx_gui.initPropertiesPane()

# TODO: Setup window, menubar, canvas, pane

from Tkinter import *
def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text='Do nothing')
    button.pack()

root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff = 0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()


"""
Init program here
Setup simulation state variables, starting empty
Sent sim state to calculation/simulation core
Obtain results of calculation/simulation if view mode enabled
Send results of calculation/simulation to draw module
Check for any change to inputs if simulation is in static mode
Frame timer collection
"""

while True:
    main.update_idletasks()
    main.update()
