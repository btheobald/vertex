"""
Program file handling module.

This module contains sections for dealing with the selection, saving and loading
of files containing simulation settings and data.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

# EXTERNAL LIBRARIES
import json

# COMMON MODULE
from module import vtx_com

def loadJSONData(file):
    """Load in a JSON file into a DOM tree and return"""
    with open(file) as saveFile:
        jsonData = json.load(saveFile)

    return jsonData

def saveJSONData(file, pointData, confData):
    """Save a JSON text file with the provided DOM tree."""

    point_list=[]

    for i in range(len(pointData)):
        point_list.append(pointData[i].getJSON())

    confDataTree = {
     "dTime": confData["dTime"],
     "rPerm": confData["rPerm"]
    }

    JSON_TREE = { "save": {
        "point": point_list,
        "config": confDataTree
    }}
    return JSON_TREE


def initPoints(jsonData):
    """Init the points, convert jsonData to objects."""
    jsonPointSet = jsonData["save"]["point"]
    objPointSet = []

    for n in range(len(jsonPointSet)):
        objPointSet.append(vtx_com.PointCharge(jsonPointSet[n]))

    return objPointSet