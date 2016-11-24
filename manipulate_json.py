import json
import pdb

def man():
	guns = None
	with open("docs/guns.json", 'r') as jsonFile:
		gun_string = jsonFile.read()
		guns = json.loads(gun_string)
		for type in guns.keys():
			for peice in guns[type]:
				#do a manipulation on a every weapon
				#peice["clipcost"] = 35
				if 'minLevel' not in peice.keys():
					print peice['name']
					pdb.set_trace()
					peice['level'] = 0
	if guns != None:
		jsonFile = open("docs/guns.json", 'w')
		jsonFile.write(json.dumps(guns))

if __name__ == "__main__":
	man()