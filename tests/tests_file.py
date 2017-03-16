from module import vtx_file
from module import vtx_com

# Test load JSON point data.
saveData = vtx_file.loadJSONData('test1.json')
pointSet = vtx_file.initPoints(saveData)
print pointSet
if len(pointSet) == 2:
    print "Test load JSON point data: PASS"
else:
    print "Test load JSON point data: FAIL"

print pointSet[0].pPos.get()
if pointSet[0].pPos.get() == [100,200]:
    print "Point[0] position data match: PASS"
else:
    print "Point[0] position data match: FAIL [100,200]"

print pointSet[1].pPos.get()
if pointSet[1].pPos.get() == [300,200]:
    print "Point[1] position data match: PASS"
else:
    print "Point[1] position data match: FAIL [300,200]"