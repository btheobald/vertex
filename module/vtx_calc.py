"""
Program calculation / simulation module.

Parts of the program pertaining to the calculation of results
used in the runtime of the program, to be stored for later use
in the draw module.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

from math import *

from module import vtx_com

def calculateVecDist(pointData=[vtx_com.PointCharge()], a=0, b=0):
    """Calculate the vector distance between two points"""
    posA = pointData[a].pPos.get()
    posB = pointData[b].pPos.get()
    return [posA[0]-posB[0], posA[1]-posB[1]]

def calculateForces(simConf, pointData=[vtx_com.PointCharge()]):
    """Calculate individual and net forces on points and set"""
    for n in range(len(pointData)):
        pointData[n].pIdvF = [] # Reset existing forces

    for a in range(len(pointData)):
        for b in range(a+1, len(pointData)):
            # Calculate individual force on point pair ab
            dVec = calculateVecDist(pointData, a, b)
            dMag = sqrt(dVec[0]**2 + dVec[1]**2)

            # Vector force calculation
            forcePreVec = (1/simConf["rPerm"])*((pointData[a].pCharge*pointData[b].pCharge)/dMag**3)
            forceX = forcePreVec * dVec[0]
            forceY = forcePreVec * dVec[1]

            # Apply to both bodies
            pointData[a].pIdvF.append(vtx_com.vecXY([forceX, forceY]))
            pointData[b].pIdvF.append(vtx_com.vecXY([-forceX, -forceY]))

        # Update net properties once all individual forces are given.
        pointData[a].updateNetF()
        pointData[a].updateAcc()

def iterateDynamicSim(simConf, pointData=[vtx_com.PointCharge()]):
    """Perform leapfrog integration of simulation at time step."""
    for n in range(len(pointData)): # 1/2v
        pointData[n].updateVel(simConf["dTime"]/2)

    for n in range(len(pointData)): # x
        pointData[n].updatePos(simConf["dTime"])

    # TODO: collisions
    calculateForces(simConf, pointData) # a

    for n in range(len(pointData)): # 1/2v
        pointData[n].updateVel(simConf["dTime"]/2)

def _calculateFieldVector(simConf, pointData=[vtx_com.PointCharge()], x=0, y=0):
    vector = [0.0, 0.0]

    vAngle = 0
    for n in range(len(pointData)):
        xDist = x - pointData[n].pPos.get(0)
        yDist = y - pointData[n].pPos.get(1)
        vDist = sqrt(pow(xDist, 2) + pow(yDist, 2))

        # Protect divide by zero
        if not vDist == 0:
            E = 1/simConf["rPerm"]*(pointData[n].pCharge / vDist**3)
        else:
            E = 0

        vector[0] += E * xDist
        vector[1] += E * yDist

        net = sqrt(vector[0] ** 2 + vector[1] ** 2) * 1E3

        vAngle = atan2(vector[1],vector[0])

    vector[0] = x+10*cos(vAngle)
    vector[1] = y+10*sin(vAngle)

    return [x, y, vector[0], vector[1], net]

def calculateFieldVectors(simConf, pointData=[vtx_com.PointCharge()]):
    resultData = []
    for x in range(401):
        if (x % 20) == 0:
            resultData.append([])
            for y in range(401):
                if (y % 20) == 0:
                    resultData[x/20].append(_calculateFieldVector(simConf, pointData, x, y))
    return resultData

def calculateFieldLines(simConf, pointData=[vtx_com.PointCharge()]):
    return None