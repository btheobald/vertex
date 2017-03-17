"""
Program interface module

This module is responsible for providing functions for setting
up and initialising the Tkinter GUI and the updating and
integration with the program runtime.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

import Tkinter

import vtx_com


def initWindow():
    """Call to init Tkinter window"""
    handle = Tkinter.Tk()
    return handle

def initMenuBar(_handle=Tkinter.Tk(None)):
    """Add menu bar to passed window"""
    item = None
    return item

def initCanvas(_handle=Tkinter.Tk(None)):
    """Add canvas to passed window"""
    item = None
    return item

def initPropertiesPane(_handle=Tkinter.Tk(None)):
    """Add properties pane to window"""
    item = None
    return item