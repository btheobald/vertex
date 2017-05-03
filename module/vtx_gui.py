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
    ("Field Lines", 3),
    ("Field Gradient", 4)
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
        self.init = 0
        self.uiPoints = []
        self.pointVal = {
            "pSelect" : StringVar(master),
            "pMass" : StringVar(master),
            "pCharge" : StringVar(master),
            "pPos" : [StringVar(master), StringVar(master)],
            "pVel" : [StringVar(master), StringVar(master)],
            "pAcc" : [StringVar(master), StringVar(master)],
            "pForce" : [StringVar(master), StringVar(master)],
        }

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

        file.add_command(label="New", command=self.__fNew)
        file.add_command(label="Open", command=self.__fOpen)
        file.add_command(label="Save", command=self.__fSave)
        file.add_command(label="Save As", command=self.__fSaveAs)
        file.add_separator()
        file.add_command(label="Exit", command=self.quit())

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

    def checkParticleSelect(self, mX, mY):
        for n in range(len(self.uiPoints)):
            tmp = self.uiPoints[n]
            # X Check
            if (not(mX > tmp.pPos.get(0) + tmp.pRadius or mX < tmp.pPos.get(0) - tmp.pRadius)):
                # Y Check
                if (not (mY > tmp.pPos.get(1) + tmp.pRadius or mY < tmp.pPos.get(1) - tmp.pRadius)):
                    print "clicked point ", n
                    return n


    def canvasClick(self, event):
        print "click", event.x, event.y
        sel = self.checkParticleSelect(event.x, event.y)
        if sel != None:
            self.pointVal["pSelect"].set(sel)
            self.updateCurrentUIPoint()

    def __initCanvas(self):
        """Add canvas to passed window"""
        self.display = Canvas(self, bg="black", width=400, height=400, relief=SUNKEN, bd=2, highlightthickness=0)
        self.display.bind("<Button-1>", self.canvasClick)
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
        self.simConfig.grid(row=0, column=1, padx=10, ipadx=5, ipady=5, sticky="NEW")
        self.pointConfig = LabelFrame(self, text="Point")
        self.pointConfig.grid(row=1, column=1, padx=10, ipadx=5, ipady=5, sticky="NEW")

        # SIMULATION PANE
        self.rPermLabel = Label(self.simConfig, text="Relative ε")
        self.rPermEntry = Spinbox(self.simConfig, from_=0.01, to=1, increment=0.01, textvariable=self.uiVal["rPerm"], width=4)
        self.rPermLabel.grid(column=0, row=0, padx=10, pady=4, sticky="W")
        self.rPermEntry.grid(column=1, columnspan=2, row=0, padx=5, pady=5, sticky="E")

        self.dTimeLabel = Label(self.simConfig, text="Time Step")
        self.dTimeEntry = Spinbox(self.simConfig, from_=0, to=10, increment=0.01, textvariable=self.uiVal["dTime"], width=4)
        self.dTimeLabel.grid(column=0, row=1, padx=10, pady=4, sticky="W")
        self.dTimeEntry.grid(column=1, columnspan=2, row=1, padx=5, pady=5, sticky="E")

        self.nPointsLabel = Label(self.simConfig, text="# Points")
        self.nPointsEntry = Entry(self.simConfig, textvariable=self.uiVal["nPoints"], width=3)
        self.nPointsLabel.grid(column=0, row=2, padx=10, pady=4, sticky="W")
        self.nPointsEntry.grid(column=1, columnspan=2, row=2, padx=5, pady=5, sticky="E")

        # POINT PANE
        self.pSelectLabel = Label(self.pointConfig, text="Selected Point")
        self.pSelectEntry = Spinbox(self.pointConfig, from_=0, to=9, increment=1, textvariable=self.pointVal["pSelect"], width=4)
        self.pSelectLabel.grid(column=0, columnspan=2, row=0, padx=10, pady=4)
        self.pSelectEntry.grid(column=2, columnspan=2, row=0, padx=5, pady=4, sticky="E")

        self.pMassLabel = Label(self.pointConfig, text="Mass (m)")
        self.pMassEntry = Spinbox(self.pointConfig, from_=0.1, to=100, increment=0.1, textvariable=self.pointVal["pMass"], width=4)
        self.pMassLabel.grid(column=0, columnspan=2, row=1, padx=10, pady=4)
        self.pMassEntry.grid(column=2, columnspan=2, row=1, padx=5, pady=4, sticky="E")

        self.pChargeLabel = Label(self.pointConfig, text="Charge (Q)")
        self.pChargeEntry = Spinbox(self.pointConfig, from_=-1, to=1, increment=0.1, textvariable=self.pointVal["pCharge"], width=4)
        self.pChargeLabel.grid(column=0, columnspan=2, row=2, padx=10, pady=4)
        self.pChargeEntry.grid(column=2, columnspan=2, row=2, padx=5, pady=4, sticky="E")

        self.pPosXLabel = Label(self.pointConfig, text="pX")
        self.pPosXEntry = Spinbox(self.pointConfig, from_=0, to=400, increment=0.1, textvariable=self.pointVal["pPos"][0], width=5)
        self.pPosXLabel.grid(column=0, row=3, padx=5, pady=4, sticky="W")
        self.pPosXEntry.grid(column=1, row=3, pady=4, sticky="E")
        self.pPosYLabel = Label(self.pointConfig, text="pY")
        self.pPosYEntry = Spinbox(self.pointConfig, from_=0, to=400, increment=0.1, textvariable=self.pointVal["pPos"][1], width=5)
        self.pPosYLabel.grid(column=2, row=3, padx=5, pady=5, sticky="W")
        self.pPosYEntry.grid(column=3, row=3, pady=5, sticky="E")

        self.pVelXLabel = Label(self.pointConfig, text="vX")
        self.pVelXEntry = Spinbox(self.pointConfig, from_=-100, to=100, increment=0.1, textvariable=self.pointVal["pVel"][0], width=5)
        self.pVelXLabel.grid(column=0, row=4, padx=5, pady=4, sticky="W")
        self.pVelXEntry.grid(column=1, row=4, pady=4, sticky="E")
        self.pVelYLabel = Label(self.pointConfig, text="vY")
        self.pVelYEntry = Spinbox(self.pointConfig, from_=-100, to=100, increment=0.1, textvariable=self.pointVal["pVel"][1], width=5)
        self.pVelYLabel.grid(column=2, row=4, padx=5, pady=4, sticky="W")
        self.pVelYEntry.grid(column=3, row=4, pady=4, sticky="E")

        self.pAccXLabel = Label(self.pointConfig, text="aX")
        self.pAccXEntry = Entry(self.pointConfig, state="readonly", textvariable=self.pointVal["pAcc"][0], width=7)
        self.pAccXLabel.grid(column=0, row=5, padx=5, pady=4, sticky="W")
        self.pAccXEntry.grid(column=1, row=5, pady=4, sticky="E")
        self.pAccYLabel = Label(self.pointConfig, text="aY")
        self.pAccYEntry = Entry(self.pointConfig, state="readonly", textvariable=self.pointVal["pAcc"][1], width=7)
        self.pAccYLabel.grid(column=2, row=5, padx=5, pady=4, sticky="W")
        self.pAccYEntry.grid(column=3, row=5, pady=4, sticky="E")

        self.pForXLabel = Label(self.pointConfig, text="fX")
        self.pForXEntry = Entry(self.pointConfig, state="readonly", textvariable=self.pointVal["pForce"][0], width=7)
        self.pForXLabel.grid(column=0, row=6, padx=5, pady=4, sticky="W")
        self.pForXEntry.grid(column=1, row=6, pady=4, sticky="E")
        self.pForYLabel = Label(self.pointConfig, text="fY")
        self.pForYEntry = Entry(self.pointConfig, state="readonly", textvariable=self.pointVal["pForce"][1], width=7)
        self.pForYLabel.grid(column=2, row=6, padx=5, pady=4, sticky="W")
        self.pForYEntry.grid(column=3, row=6, pady=4, sticky="E")

        self.NewButton = Button(self.pointConfig, text="New")
        self.NewButton.grid(column=0, columnspan=2, row=7, padx=5, pady=4, sticky="EW")
        self.DelButton = Button(self.pointConfig, text="Delete")
        self.DelButton.grid(column=2, columnspan=2, row=7, padx=5, pady=4, sticky="EW")

        self.updateCurrentUIPoint()

    def updateConfig(self, conf={}):
        conf["rPerm"] = float(self.uiVal["rPerm"].get())
        conf["dTime"] = float(self.uiVal["dTime"].get())
        self.uiVal["nPoints"].set(str(conf["nPoints"]))
        conf["sim"] = self.modes["sim"].get()
        conf["view"] = self.modes["view"].get()

    def updatePoints(self, dyn, points=[]):
        if(dyn):
            self.updateCurrentUIPoint()
            self.init = 1
        else:
            self.updateActualPoint(points)
            if (self.init == 1):
                self.init = 0
                self.updateCurrentUIPoint()

        if self.loaded == 1:
            self.loaded = 0
            for n in range(len(points)):
                points.pop()  # Remove existing
            for n in range(len(self.uiPoints)):
                points.append(self.uiPoints[n])  # Add New
        else:
            self.uiPoints = deepcopy(points)


    def updateCurrentUIPoint(self):
        if (len(self.uiPoints) > 0):
            if (not (int(self.pointVal["pSelect"].get()) < len(self.uiPoints))):
                self.pointVal["pSelect"].set(len(self.uiPoints) - 1)

            current = self.uiPoints[int(self.pointVal["pSelect"].get())]
            self.pointVal["pMass"].set(current.pMass)
            self.pointVal["pCharge"].set(current.pCharge)

            self.pointVal["pPos"][0].set(current.pPos.get(0))
            self.pointVal["pPos"][1].set(current.pPos.get(1))

            self.pointVal["pVel"][0].set(current.pVel.get(0))
            self.pointVal["pVel"][1].set(current.pVel.get(1))

            self.pointVal["pAcc"][0].set(current.pAcc.get(0))
            self.pointVal["pAcc"][1].set(current.pAcc.get(1))

            self.pointVal["pForce"][0].set(current.pNetF.get(0))
            self.pointVal["pForce"][1].set(current.pNetF.get(1))

    def updateActualPoint(self, points):
        if(len(points) > 0):
            tmp = vtx_com.PointCharge()

            try:
                tmp.pMass = float(self.pointVal["pMass"].get())
            except ValueError:
                tmp.pMass = 1

            tmp.pCharge = float(self.pointVal["pCharge"].get())
            tmp.pPos.set([float(self.pointVal["pPos"][0].get()), float(self.pointVal["pPos"][1].get())])
            tmp.pVel.set([float(self.pointVal["pVel"][0].get()), float(self.pointVal["pVel"][1].get())])
            tmp.pAcc.set()
            tmp.pNetF.set()

            points[int(self.pointVal["pSelect"].get())] = tmp

            # Command functions
    def __fNew(self):
        self.uiPoints = []
        self.loaded = 1
        self.filename = ''
        self.modes["sim"].set(0)

    def __fOpen(self):
        self.modes["sim"].set(0)

        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        if self.filename != '':
            data = vtx_file.loadJSONData(self.filename)
            self.uiPoints = deepcopy(vtx_file.initPoints(data))

            self.uiVal["rPerm"].set(data["save"]["config"]["rPerm"])
            self.uiVal["dTime"].set(data["save"]["config"]["dTime"])
            self.modes["sim"].set(0)

            self.loaded = 1

            self.updateCurrentUIPoint()

    def __fSaveAs(self):
        self.filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        if self.filename != '':
            vtx_file.saveJSONData(self.filename, self.uiPoints, self.uiVal)

    def __fSave(self):
        if self.filename == '':
            self.filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        if self.filename != '':
            vtx_file.saveJSONData(self.filename, self.uiPoints, self.uiVal)