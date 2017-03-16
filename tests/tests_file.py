from module import vtx_file

# Test load JSON point data.
saveData = vtx_file.loadJSONData('test1.json')
pointSet = vtx_file.initPoints(saveData)
print pointSet
if len(pointSet) == 2:
    print "Test load JSON point data: PASS"
else:
    print "Test load JSON point data: FAIL"