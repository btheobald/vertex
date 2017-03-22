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

from module import vtx_com

uiVal = dict()
modes = dict()

VIEWMODES = [
    ("Clear",         0),
    ("Force Vectors", 1),
    ("Field Vectors", 2),
    ("Field Lines",   3)
]

SIMMODES = [
    ("Static",  0),
    ("Dynamic", 1)
]

def setUiDefaults():
    uiVal["dTime"].set("1.0")
    uiVal["rPerm"].set("0.1")
    uiVal["nPoints"].set("0")

    modes["mSim"].set(0)
    modes["mView"].set(0)

def initWindow():
    """Call to init Tkinter window"""
    root = Tk()
    root.resizable(width=False, height=False)

    uiVal.update({"dTime" : StringVar(root)})
    uiVal.update({"rPerm" : StringVar(root)})
    uiVal.update({"nPoints" : StringVar(root)})

    modes.update({"mSim" : IntVar(root)})
    modes.update({"mView" : IntVar(root)})

    setUiDefaults()

    menu = _initMenuBar(root)
    display = _initCanvas(root)
    property = _initPropertiesPane(root)

    return [root, menu, display, property]

def _initMenuBar(_handle):
    """Add menu bar to passed window"""
    menubar = Menu(_handle)
    filemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Save")
    filemenu.add_command(label="Save as")
    filemenu.add_separator()
    filemenu.add_command(label="Exit")

    viewmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=viewmenu)
    for label, val in VIEWMODES:
        viewmenu.add_radiobutton(label=label, value=val, variable=modes["mView"])
    viewmenu.add_separator()
    viewmenu.add_command(label="Charges")
    viewmenu.add_command(label="Origin")

    modemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Mode", menu=modemenu)
    for label, val in SIMMODES:
        modemenu.add_radiobutton(label=label, value=val, variable=modes["mSim"])
    modemenu.add_separator()
    modemenu.add_command(label="Reset")
    modemenu.add_command(label="Clear")

    aboutmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="About", menu=aboutmenu)
    aboutmenu.add_command(label="Help")
    aboutmenu.add_command(label="Version info")
    aboutmenu.add_command(label="Credits")

    _handle.config(menu=menubar)
    return menubar

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
    rPermEntry = Spinbox(simConfig, from_=0.01, to=1, increment=0.01, textvariable=uiVal["rPerm"], width=4)
    rPermLabel.grid(column=0, row=0, padx=10, pady=5, sticky="W")
    rPermEntry.grid(column=1, row=0, pady=5, sticky="E")

    dTimeLabel = Label(simConfig, text="Time Step")
    dTimeEntry = Spinbox(simConfig, from_=0, to=10, increment=0.01, textvariable=uiVal["dTime"], width=4)
    dTimeLabel.grid(column=0, row=1, padx=10, pady=5, sticky="W")
    dTimeEntry.grid(column=1, row=1, pady=5, sticky="E")

    nPointsLabel = Label(simConfig, text="# Points")
    nPointsEntry = Entry(simConfig, textvariable=uiVal["nPoints"], width=3)
    nPointsLabel.grid(column=0, row=2, padx=10, pady=5, sticky="W")
    nPointsEntry.grid(column=1, row=2, padx=5, pady=5, sticky="W")

    # POINT PANE
    # Point Select(Spinbox of range(len(pointData))
    # Mass (Spinbox)
    # Charge (Spinbox)
    # Position (Spinbox * 2)
    # Velocity (Spinbox * 2)
    # Acceleration (Spinbox * 2, Non-Editable)
    # Force (Spinbox * 2, Non-Editable)

    property = [simConfig, pointConfig]
    return property

def updateConfig(conf={}):
    conf["rPerm"] = float(uiVal["rPerm"].get())
    conf["dTime"] = float(uiVal["dTime"].get())
    uiVal["nPoints"].set(str(conf["nPoints"]))
    conf["mSim"] = modes["mSim"].get()
    conf["mView"] = modes["mView"].get()

def updatePoints(pointData):
    return None
    # if dynamic, update displayed values with current values in point
    # if static, update pointData with values from GUI

# TODO: Get inputs/outputs linked to actual objects