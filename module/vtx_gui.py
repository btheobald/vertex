#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Program interface module

This module is responsible for providing functions for setting
up and initialising the Tkinter GUI and the updating and
integration with the program runtime.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

from Tkinter import *

import vtx_com

uiValues = {
    "rPerm" : None,
    "dTime" : None,
    "count" : None
}

def donothing():
    filewin = Toplevel()
    button = Button(filewin, text='Do nothing')
    button.pack()

def setDefaults(root):
    uiValues = {
        "rPerm": StringVar(root),
        "dTime": StringVar(root),
        "count": StringVar(root)
    }

    uiValues["rPerm"].set("0.1")
    uiValues["dTime"].set("1.0")

def initWindow():
    """Call to init Tkinter window"""
    root = Tk()
    root.resizable(width=False, height=False)

    setDefaults(root)

    menu = _initMenuBar(root)
    display = _initCanvas(root)
    property = _initPropertiesPane(root)

    return [root, menu, display, property]

def _initMenuBar(_handle):
    """Add menu bar to passed window"""
    menubar = Menu(_handle)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_command(label="Close", command=donothing)

    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=_handle.quit)
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
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    _handle.config(menu=menubar)


def _initCanvas(_handle):
    """Add canvas to passed window"""
    display = Canvas(_handle, bg="black", width=400, height=400, relief=SUNKEN, bd=2, highlightthickness=0)
    display.grid(row=0, column=0, rowspan=2)
    return display

def _initPropertiesPane(_handle):
    """Add properties pane to window"""
    simConfig = LabelFrame(_handle, text="Simulation")
    simConfig.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky="NEW")
    pointConfig = LabelFrame(_handle, text="Point")
    pointConfig.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky="NEW")

    # SIMULATION PANE
    rPermLabel = Label(simConfig, text="Relative ε")
    rPermEntry = Spinbox(simConfig, from_=0.01, to=1, increment=0.01, textvariable=uiValues["rPerm"], width=4)
    rPermLabel.grid(column=0, row=0, padx=10, pady=5, sticky="W")
    rPermEntry.grid(column=1, row=0, pady=5, sticky="E")

    dTimeLabel = Label(simConfig, text="Time Step")
    dTimeEntry = Spinbox(simConfig, from_=0, to=10, increment=0.01, textvariable=uiValues["dTime"], width=4)
    dTimeLabel.grid(column=0, row=1, padx=10, pady=5, sticky="W")
    dTimeEntry.grid(column=1, row=1, pady=5, sticky="E")

    nPointsLabel = Label(simConfig, text="# Points")
    nPointsEntry = Entry(simConfig, textvariable=uiValues["count"], width=3)
    nPointsLabel.grid(column=0, row=2, padx=10, pady=5, sticky="W")
    nPointsEntry.grid(column=1, row=2, padx=5, pady=5, sticky="W")

    clearButton = Button(simConfig, text="Clear")
    clearButton.grid(column=0, columnspan=2, row=3, pady=5, padx=10, sticky="EW")

    # POINT PANE
    # Point Select(Spinbox of range(len(pointData))
    # Mass (Spinbox)
    # Charge (Spinbox)
    # Position (Spinbox * 2)
    # Velocity (Spinbox * 2)
    # Acceleration (Spinbox * 2, Non-Editable)
    # Force (Spinbox * 2, Non-Editable)

    property = [simConfig, pointConfig]

def updateConfig(conf={}, ):
    conf["rPerm"] = float(uiValues["rPerm"])
    conf["dTime"] = float(uiValues["dTime"])
    uiValues["count"] = set(str(conf["count"]))
    #conf["sim"] = self.simMode.get()
    #conf["draw"] = self.viewMode.get()

def updatePoints(pointData):
    return None
    # if dynamic, update displayed values with current values in point
    # if static, update pointData with values from GUI

# TODO: Get inputs/outputs linked to actual objects