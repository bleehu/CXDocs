import json

classFile = open("classes2.json")
classString = classFile.read()
blob = json.loads(classString)
print "it werked"
