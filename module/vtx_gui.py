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
from random import random
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
            "view" : IntVar(master),
        }
        self.uiVal = {
            "dTime" : StringVar(master),
            "rPerm" : StringVar(master),
            "nPoints" : StringVar(master)
        }

        self.fpsCtr = BooleanVar(master)
        self.paused = BooleanVar(master)
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
        file.add_command(label="Exit", command=self.destroy)

        view = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view)
        for label, val in VIEWMODES:
            view.add_radiobutton(label=label, value=val, variable=self.modes["view"])
        view.add_separator()
        view.add_checkbutton(label="FPS Counter", variable=self.fpsCtr)

        mode = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Mode", menu=mode)
        for label, val in SIMMODES:
            mode.add_radiobutton(label=label, value=val, variable=self.modes["sim"])
        mode.add_checkbutton(label="Paused", variable=self.paused)

        #about = Menu(self.menubar, tearoff=0)
        #self.menubar.add_command(label="Help")

        self.master.config(menu=self.menubar)

    def checkParticleSelect(self, mX, mY):
        for n in range(len(self.uiPoints)):
            tmp = self.uiPoints[n]
            # X Check
            if (not(mX > tmp.pPos.get(0) + tmp.pRadius or mX < tmp.pPos.get(0) - tmp.pRadius)):
                # Y Check
                if (not (mY > tmp.pPos.get(1) + tmp.pRadius or mY < tmp.pPos.get(1) - tmp.pRadius)):
                    #print "clicked point ", n
                    return n


    def canvasClick(self, event):
        #print "click", event.x, event.y
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
        self.pointVal["pSelect"].set("0")

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

        self.simPause = Checkbutton(self.simConfig, text="Paused", variable=self.paused)
        self.simPause.grid(column=3, row=0, rowspan=3)

        # POINT PANE
        self.pSelectLabel = Label(self.pointConfig, text="Selected")
        self.pSelectEntry = Entry(self.pointConfig, state=DISABLED, textvariable=self.pointVal["pSelect"], width=16)
        self.pSelectLabel.grid(column=0, columnspan=2, padx=5, row=0, pady=4, sticky="W")
        self.pSelectEntry.grid(column=1, columnspan=2, row=0, pady=3, sticky="WE")

        self.pMassLabel = Label(self.pointConfig, text="Mass")
        self.pMassEntry = Spinbox(self.pointConfig, from_=0.1, to=100, increment=0.1, textvariable=self.pointVal["pMass"], width=16)
        self.pMassLabel.grid(column=0, columnspan=2, padx=5, row=1, pady=4, sticky="W")
        self.pMassEntry.grid(column=1, columnspan=2, row=1, pady=3, sticky="WE")

        self.pChargeLabel = Label(self.pointConfig, text="Charge")
        self.pChargeEntry = Spinbox(self.pointConfig, from_=-1, to=1, increment=0.1, textvariable=self.pointVal["pCharge"], width=16)
        self.pChargeLabel.grid(column=0, columnspan=2, padx=5, row=2, pady=4, sticky="W")
        self.pChargeEntry.grid(column=1, columnspan=2, row=2, pady=3, sticky="WE")

        self.xLabel = Label(self.pointConfig, text="X")
        self.yLabel = Label(self.pointConfig, text="Y")
        self.xLabel.grid(column=1, row=3)
        self.yLabel.grid(column=2, row=3)

        self.pPosLabel = Label(self.pointConfig, text="Position")
        self.pPosXEntry = Spinbox(self.pointConfig, from_=0, to=400, increment=0.1, textvariable=self.pointVal["pPos"][0], width=8)
        self.pPosLabel.grid(column=0, row=4, padx=5, pady=4, sticky="W")
        self.pPosXEntry.grid(column=1, row=4, pady=3, sticky="E")
        self.pPosYEntry = Spinbox(self.pointConfig, from_=0, to=400, increment=0.1, textvariable=self.pointVal["pPos"][1], width=8)
        self.pPosYEntry.grid(column=2, row=4, pady=3, sticky="E")

        self.pVelLabel = Label(self.pointConfig, text="Velocity")
        self.pVelXEntry = Spinbox(self.pointConfig, from_=-100, to=100, increment=0.1, textvariable=self.pointVal["pVel"][0], width=8)
        self.pVelLabel.grid(column=0, row=5, padx=5, pady=3, sticky="W")
        self.pVelXEntry.grid(column=1, row=5, pady=3, sticky="E")
        self.pVelYEntry = Spinbox(self.pointConfig, from_=-100, to=100, increment=0.1, textvariable=self.pointVal["pVel"][1], width=8)
        self.pVelYEntry.grid(column=2, row=5, pady=3, sticky="E")

        self.pAccLabel = Label(self.pointConfig, text="Accel.")
        self.pAccXEntry = Entry(self.pointConfig, state=DISABLED, textvariable=self.pointVal["pAcc"][0], width=10)
        self.pAccLabel.grid(column=0, row=6, padx=5, pady=3, sticky="W")
        self.pAccXEntry.grid(column=1, row=6, pady=3, sticky="E")
        self.pAccYEntry = Entry(self.pointConfig, state=DISABLED, textvariable=self.pointVal["pAcc"][1], width=10)
        self.pAccYEntry.grid(column=2, row=6, pady=3, sticky="E")

        self.pForLabel = Label(self.pointConfig, text="Force")
        self.pForXEntry = Entry(self.pointConfig, state=DISABLED, textvariable=self.pointVal["pForce"][0], width=10)
        self.pForLabel.grid(column=0, row=7, padx=5, pady=3, sticky="W")
        self.pForXEntry.grid(column=1, row=7, pady=3, sticky="E")
        self.pForYEntry = Entry(self.pointConfig, state=DISABLED, textvariable=self.pointVal["pForce"][1], width=10)
        self.pForYEntry.grid(column=2, row=7, pady=3, sticky="E")

        self.pNewButton = Button(self.pointConfig, text="New", command=self.__sRandomPoint)
        self.pNewButton.grid(column=0, columnspan=2, row=8, padx=5, pady=3, sticky="EW")
        self.pDelButton = Button(self.pointConfig, text="Delete", command=self.__sDeletePoint)
        self.pDelButton.grid(column=2, columnspan=1, row=8, padx=5, pady=3, sticky="EW")

        self.updateCurrentUIPoint()

    def updateEditableBoxes(self, dyn):
        if dyn:
            self.pMassEntry.configure(state=DISABLED)

            self.pChargeEntry.configure(state=DISABLED)

            self.pPosXEntry.configure(state=DISABLED)
            self.pPosYEntry.configure(state=DISABLED)

            self.pVelXEntry.configure(state=DISABLED)
            self.pVelYEntry.configure(state=DISABLED)
        else:
            self.pMassEntry.configure(state=NORMAL)

            self.pChargeEntry.configure(state=NORMAL)

            self.pPosXEntry.configure(state=NORMAL)
            self.pPosYEntry.configure(state=NORMAL)

            self.pVelXEntry.configure(state=NORMAL)
            self.pVelYEntry.configure(state=NORMAL)

    def updateConfig(self, conf={}):
        try:
            conv = float(self.uiVal["rPerm"].get())
            if conv <= 0:
                raise ValueError('Value cannot be <= 0')
            conf["rPerm"] = conv
        except:
            conf["rPerm"] = 1

        if (self.paused.get()):
            conf["dTime"] = 0
        else:
            try:
                conv = float(self.uiVal["dTime"].get())
                conf["dTime"] = conv
            except:
                conf["dTime"] = 0

        self.uiVal["nPoints"].set(str(conf["nPoints"]))
        conf["fpsc"] = self.fpsCtr.get()
        conf["sim"] = self.modes["sim"].get()
        conf["view"] = self.modes["view"].get()

        """Blank/Allow boxes"""
        self.updateEditableBoxes(conf["sim"])

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
            self.pointVal["pMass"].set(round(current.pMass,3))
            self.pointVal["pCharge"].set(round(current.pCharge,3))

            self.pointVal["pPos"][0].set(round(current.pPos.get(0),3))
            self.pointVal["pPos"][1].set(round(current.pPos.get(1),3))

            self.pointVal["pVel"][0].set(round(current.pVel.get(0),3))
            self.pointVal["pVel"][1].set(round(current.pVel.get(1),3))

            self.pointVal["pAcc"][0].set(round(current.pAcc.get(0),3))
            self.pointVal["pAcc"][1].set(round(current.pAcc.get(1),3))

            self.pointVal["pForce"][0].set(round(current.pNetF.get(0),3))
            self.pointVal["pForce"][1].set(round(current.pNetF.get(1),3))

    def updateActualPoint(self, points):
        if(len(points) > 0):
            tmp = vtx_com.PointCharge()

            try:
                try:
                    if points[int(self.pointVal["pSelect"].get())] == None:
                        raise IndexError('Out of Bounds')
                except ValueError:
                    self.pointVal["pSelect"].set("0")
            except IndexError:
                self.pointVal["pSelect"].set("0")

            try:
                tmp.pMass = float(self.pointVal["pMass"].get())
                if(tmp.pMass <= 0):
                    raise ValueError('Value cannot be <= 0')
            except ValueError:
                tmp.pMass = 1.0

            try:
                tmp.pCharge = float(self.pointVal["pCharge"].get())
            except ValueError:
                tmp.pCharge = 0

            try:
                tmp.pPos.set([float(self.pointVal["pPos"][0].get()), float(self.pointVal["pPos"][1].get())])
            except ValueError:
                tmp.pPos.set([200.0,200.0])

            try:
                tmp.pVel.set([float(self.pointVal["pVel"][0].get()), float(self.pointVal["pVel"][1].get())])
            except ValueError:
                tmp.pVel.set([0, 0])

            tmp.pAcc.set()
            tmp.pNetF.set()

            points[int(self.pointVal["pSelect"].get())] = tmp

            # Command functions
    def __fNew(self):
        self.uiPoints = []
        self.loaded = 1
        self.filename = ''
        self.modes["sim"].set(1)
        self.pointVal["pSelect"].set(0)
        self.updateCurrentUIPoint()
        self.modes["sim"].set(10)

    def __fOpen(self):
        self.modes["sim"].set(0)

        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        if self.filename != '':
            data = vtx_file.loadJSONData(self.filename)
            self.uiPoints = deepcopy(vtx_file.initPoints(data))

            self.uiVal["rPerm"].set(data["save"]["config"]["rPerm"])
            self.uiVal["dTime"].set(data["save"]["config"]["dTime"])
            self.modes["sim"].set(0)

            self.pointVal["pSelect"].set(0)

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

    def rangeCheck(self):
        for n in range(len(self.uiPoints)):
            if (self.uiPoints[n].pPos.get(0) > 500) or (self.uiPoints[n].pPos.get(0) < -100) or \
               (self.uiPoints[n].pPos.get(1) > 500) or (self.uiPoints[n].pPos.get(1) < -100):
                self.uiPoints.pop(n)

                self.loaded = 1
                self.updateCurrentUIPoint()
                break


    def __sDeletePoint(self):
        self.uiPoints.pop(int(self.pointVal["pSelect"].get()))

        self.loaded = 1
        self.updateCurrentUIPoint()

    def __sRandomPoint(self):
        self.uiPoints.append(vtx_com.PointCharge(_m=1.0, _c=(random()*2)-1, _p=[random()*400, random()*400]))

        #TODO: Select new body after creation.

        self.loaded = 1
        self.updateCurrentUIPoint()
