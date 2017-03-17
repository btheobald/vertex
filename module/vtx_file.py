"""
Program file handling module.

This module contains sections for dealing with the selection, saving and loading
of files containing simulation settings and data.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
import json

# COMMON MODULE
import vtx_com

def loadJSONData(file):
    """Load in a JSON file into a DOM tree and return"""
    with open(file) as saveFile:
        jsonData = json.load(saveFile)

    return jsonData

def saveJSONData(jsonData):
    """Save a JSON text file with the provided DOM tree."""
    # TODO: Expand stub

def initPoints(jsonData):
    """Init the points, convert jsonData to objects."""
    jsonPointSet = jsonData["save"]["point"]
    objPointSet = []

    # TODO: Parse for invalid data and log.

    for n in range(len(jsonPointSet)):
        objPointSet.append(vtx_com.PointCharge(jsonPointSet[n]))

    return objPointSet