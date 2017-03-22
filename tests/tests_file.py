from module import vtx_file
from module import vtx_com

conf = {"rPerm":0.10, "dTime":2.00, "nPoints":0, "sim":0, "view":0}
# Test load JSON point data and check resulting objects.
print "File Load Test"
saveData = vtx_file.loadJSONData('test1.json')
pointSet = vtx_file.initPoints(saveData)
print pointSet
print

print "Data Integrity Test"
if len(pointSet) == 2:
    print "Test load JSON point data: PASS"
else:
    print "Test load JSON point data: FAIL"

print "Object Data:", str(pointSet[0].pPos.get())
if pointSet[0].pPos.get() == [100,200]:
    print "Point[0] position [100,200] data match: PASS"
else:
    print "Point[0] position [100,200] data match: FAIL "

print "Object Data:", str(pointSet[1].pPos.get())
if pointSet[1].pPos.get() == [300,200]:
    print "Point[1] position [300,200] data match: PASS"
else:
    print "Point[1] position [300,200] data match: FAIL "

print
print "Save current data."
vtx_file.saveJSONData('test1out.json', pointSet, conf)
print "Done!"

print
print "Reload saved data."
saveData = vtx_file.loadJSONData('test1out.json')
pointSet = vtx_file.initPoints(saveData)
print saveData

print
print "Data Integrity Test 2"
if len(pointSet) == 2:
    print "Test load JSON point data: PASS"
else:
    print "Test load JSON point data: FAIL"

print "Object Data:", str(pointSet[0].pPos.get())
if pointSet[0].pPos.get() == [100,200]:
    print "Point[0] position [100,200] data match: PASS"
else:
    print "Point[0] position [100,200] data match: FAIL "

print "Object Data:", str(pointSet[1].pPos.get())
if pointSet[1].pPos.get() == [300,200]:
    print "Point[1] position [300,200] data match: PASS"
else:
    print "Point[1] position [300,200] data match: FAIL "