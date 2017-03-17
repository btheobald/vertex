"""
Program calculation / simulation module.

Parts of the program pertaining to the calculation of results
used in the runtime of the program, to be stored for later use
in the draw module.

Keep cyclic imports to minimum, ie write in a way where modules are not interlinked.
"""

import math
import vtx_com

def calculateVecDist(pointData=[vtx_com.PointCharge()], a=0, b=0):
    """Calculate the vector distance between two points"""
    posA = pointData[a].pPos.get()
    posB = pointData[b].pPos.get()
    return [posA[0]-posB[0], posA[1]-posB[1]]

def calculateForces(simConf, pointData=[vtx_com.PointCharge()]):
    """Calculate individual and net forces on points and set"""
    for a in range(len(pointData)):
        for b in range(a+1, len(pointData)):
            # Calculate individual force on point pair ab
            dVec = calculateVecDist(pointData, a, b)
            dMag = math.sqrt(dVec[0]**2 + dVec[1]**2)

            # Vector force calculation
            forcePreVec = (1/simConf["rPerm"]) * ((a.pCharge * b.pCharge) / dMag ** 3)
            forceX = -forcePreVec * dVec[0]
            forceY = -forcePreVec * dVec[1]

            # Apply to both bodies
            pointData[a].pIdvF.append(vtx_com.vecXY([forceX, forceY]))
            pointData[b].pIdvF.append(vtx_com.vecXY([-forceX, -forceY]))

        # Update net properties once all individual forces are given.
        pointData[a].updateNetF()
        pointData[a].updateAcc()