from module import vtx_calc
from module import vtx_com

simconf = {"rPerm":1.00, "dTime":2.0}

points = [vtx_com.PointCharge(_m=100, _c=1, _p=vtx_com.vecXY([0.0,0.0])), vtx_com.PointCharge(_m=1, _c=-1,_p=vtx_com.vecXY([10.0,0.0]),_v=vtx_com.vecXY([0, 0.31]))]

for n in range(100):
    print str(points[0].pPos.get(0)), str(points[0].pPos.get(1)), str(points[1].pPos.get(0)), str(points[1].pPos.get(1))
    vtx_calc.iterateDynamicSim(simconf, points)