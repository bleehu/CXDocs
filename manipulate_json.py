import json

def man():
	guns = None
	with open("docs/guns.json", 'r') as jsonFile:
		gun_string = jsonFile.read()
		guns = json.loads(gun_string)
		for type in guns.keys():
			for peice in guns[type]:
				#do a manipulation on a every weapon
				peice["clipcost"] = 35
	if guns != None:
		jsonFile = open("docs/guns.json", 'w')
		jsonFile.write(json.dumps(guns))

if __name__ == "__main__":
	man()