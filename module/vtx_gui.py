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
from copy import deepcopy
import tkFileDialog

from module import vtx_com
from module import vtx_file

VIEWMODES = [
    ("Clear", 0),
    ("Force Vectors", 1),
    ("Field Vectors", 2),
    ("Field Lines", 3)
]
SIMMODES = [
    ("Static", 0),
    ("Dynamic", 1)
]

class vertexUI(Frame):
    def __init__(self, master=None):
        # Mode variables
        self.modes = {
            "sim" : IntVar(master),
            "view" : IntVar(master)
        }
        self.uiVal = {
            "dTime" : StringVar(master),
            "rPerm" : StringVar(master),
            "nPoints" : StringVar(master)
        }

        self.loaded = 0
        self.uiPoints = []

        # File setup
        self.file_opt = options = {}
        options['defaultextension'] = '.json'
        options['filetypes'] = [('Vertex Savefile', '.json')]
        options['initialdir'] = '.'
        options['initialfile'] = 'save.json'
        options['parent'] = master
        options['title'] = 'Browse'

        ## MENU BAR ##
        Frame.__init__(self, master)

        self.__setUiDefaults()
        self.__initMenuBar()
        self.__initCanvas()
        self.__initPropertiesPane()

    def __initMenuBar(self):
        self.menubar = Menu(self)

        file = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file)

        file.add_command(label="New", command=self.fNew)
        file.add_command(label="Open", command=self.fOpen)
        file.add_command(label="Save", command=self.fSave)
        file.add_command(label="Save As", command=self.fSaveAs)
        file.add_separator()
        file.add_command(label="Exit")

        view = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view)
        for label, val in VIEWMODES:
            view.add_radiobutton(label=label, value=val, variable=self.modes["view"])
        view.add_separator()
        view.add_checkbutton(label="Origin")
        view.add_checkbutton(label="Charges")
        view.add_checkbutton(label="FPS Counter")

        mode = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Mode", menu=mode)
        for label, val in SIMMODES:
            mode.add_radiobutton(label=label, value=val, variable=self.modes["sim"])

        about = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="About", menu=about)
        about.add_command(label="Help")
        about.add_command(label="Debug Info")
        about.add_command(label="About Vertex")

        self.master.config(menu=self.menubar)

    def __initCanvas(self):
        """Add canvas to passed window"""
        self.display = Canvas(self, bg="black", width=400, height=400, relief=SUNKEN, bd=2, highlightthickness=0)
        self.display.grid(row=0, column=0, rowspan=2)
        return self.display

    def __setUiDefaults(self):
        self.uiVal["dTime"].set("1.0")
        self.uiVal["rPerm"].set("0.1")
        self.uiVal["nPoints"].set("0")
        self.modes["view"].set(0)
        self.modes["sim"].set(0)

    def __initPropertiesPane(self):
        """Add properties pane to window"""
        self.simConfig = LabelFrame(self, text="Simulation")
        self.simConfig.grid(row=0, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky="NEW")
        self.pointConfig = LabelFrame(self, text="Point")
        self.pointConfig.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=10, sticky="NEW")

        # SIMULATION PANE
        self.rPermLabel = Label(self.simConfig, text="Relative ε")
        self.rPermEntry = Spinbox(self.simConfig, from_=0.01, to=1, increment=0.01, textvariable=self.uiVal["rPerm"], width=4)
        self.rPermLabel.grid(column=0, row=0, padx=10, pady=5, sticky="W")
        self.rPermEntry.grid(column=1, row=0, pady=5, sticky="E")

        self.dTimeLabel = Label(self.simConfig, text="Time Step")
        self.dTimeEntry = Spinbox(self.simConfig, from_=0, to=10, increment=0.01, textvariable=self.uiVal["dTime"], width=4)
        self.dTimeLabel.grid(column=0, row=1, padx=10, pady=5, sticky="W")
        self.dTimeEntry.grid(column=1, row=1, pady=5, sticky="E")

        self.nPointsLabel = Label(self.simConfig, text="# Points")
        self.nPointsEntry = Entry(self.simConfig, textvariable=self.uiVal["nPoints"], width=3)
        self.nPointsLabel.grid(column=0, row=2, padx=10, pady=5, sticky="W")
        self.nPointsEntry.grid(column=1, row=2, padx=5, pady=5, sticky="W")

        # POINT PANE
        # Point Select(Spinbox of range(len(pointData))
        # Mass (Spinbox)
        # Charge (Spinbox)
        # Position (Spinbox * 2)
        # Velocity (Spinbox * 2)
        # Acceleration (Spinbox * 2, Non-Editable)
        # Force (Spinbox * 2, Non-Editable)

    def updateConfig(self, conf={}):
        conf["rPerm"] = float(self.uiVal["rPerm"].get())
        conf["dTime"] = float(self.uiVal["dTime"].get())
        self.uiVal["nPoints"].set(str(conf["nPoints"]))
        conf["sim"] = self.modes["sim"].get()
        conf["view"] = self.modes["view"].get()

    def updatePoints(self, points=[]):
        if self.loaded == 1:
            self.loaded = 0
            for n in range(len(points)):
                points.pop() # Remove existing
            for n in range(len(self.uiPoints)):
                points.append(self.uiPoints[n]) # Add New
        else:
            self.uiPoints = deepcopy(points)

    # Command functions
    def fNew(self):
        self.uiPoints = []
        self.loaded = 1
        self.filename = ''
        self.modes["sim"].set(0)

    def fOpen(self):
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        if self.filename != '':
            data = vtx_file.loadJSONData(self.filename)
            self.uiPoints = deepcopy(vtx_file.initPoints(data))

            self.uiVal["rPerm"].set(data["save"]["config"]["rPerm"])
            self.uiVal["dTime"].set(data["save"]["config"]["dTime"])
            self.modes["sim"].set(0)

            self.loaded = 1

    def fSaveAs(self):
        self.filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        if self.filename != '':
            vtx_file.saveJSONData(self.filename, self.uiPoints, self.uiVal)

    def fSave(self):
        if self.filename == '':
            self.filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        if self.filename != '':
            vtx_file.saveJSONData(self.filename, self.uiPoints, self.uiVal)