from module import vtx_calc
from module import vtx_com
from pprint import *

simconf = {"rPerm":0.10, "dTime":2.0}

points = [vtx_com.PointCharge(_m=100, _c=1, _p=[200.0,200.0]), vtx_com.PointCharge(_m=1, _c=-1,_p=[300.0,200.0],_v=[0, 0.31])]


calcData=vtx_calc.calculateFieldVectors(simconf, points)

print
print "Field vector Data"
pprint(calcData)

print
print "Iterate 100 Frames"
for n in range(100):
    print str(points[0].pPos.get(0)), str(points[0].pPos.get(1)), str(points[1].pPos.get(0)), str(points[1].pPos.get(1))
    vtx_calc.iterateDynamicSim(simconf, points)

