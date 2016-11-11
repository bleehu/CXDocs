import csv
from flask import Flask, render_template, request, redirect
import json
import pdb
import xml.etree.ElementTree
app = Flask(__name__)
app.config.from_object(__name__)

def get_levels():
	levels = []
	with open('docs/levels.csv', 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for line in csv_reader:
			levels.append(line)
	return levels
	
def get_feats():
	feats = []
	with open("docs/feats.csv") as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',',quotechar='"')
		for line in csv_reader:
			feats.append(line)
	return feats
	
def get_guns():
	goons = None
	with open("docs/guns1.json") as gunfile:
		goons = json.loads(gunfile.read())
	return goons

def get_armor():
	arms = None
	types = []
	by_type = {}
	with open("docs/armor.json") as armfile:
		arms = json.loads(armfile.read())
		for armor in arms:
			if armor['type'] not in by_type.keys():
				by_type[armor['type']] = []
			by_type[armor['type']].append(armor)
	return by_type

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/levelup")
def levelUp():
	levels = get_levels()
	return render_template('levelup.html', levels=levels)
	
@app.route("/guns")
def guns():
	guns = get_guns()
	return render_template('guns.html', guns=guns)
	
@app.route("/armor")
def show_armor():
	armor = get_armor()
	return render_template('armor.html', armors=armor)

@app.route("/items")
def show_items():
	return render_template('items.html', items=[])

@app.route("/rules")
def show_rules():
	root = xml.etree.ElementTree.parse("docs/rules.xml").getroot()
	sections = root.findall('section')
	pdb.set_trace()
	return render_template('rules.html', sections=sections)

@app.route("/feats")
def show_feats():
	feats = get_feats()
	return render_template("feats.html", feats=feats)
	
@app.route("/weaponsmith")
def show_weaponsmith():
	guns = get_guns()
	return render_template("weaponsmith.html", guns=guns)

@app.route("/addgun", methods=['POST'])
def make_gun():
	gun = {}
	gun['name'] = request.form['gunname']
	gun['range'] = request.form['range']
	gun['damage'] = request.form['gunDamage']
	gun['type'] = request.form['gunType']
	gun['clip'] = request.form['clip']
	gun['toMiss'] = request.form['toMiss']
	gun['effect'] = request.form['effect']
	gun['cost'] = request.form['cost']
	guns = get_guns()
	guns.append(gun)
	json_string = json.dumps(guns)
	with open("docs/guns1.json", 'w') as gunfile:
		gunfile.write(json_string)
	return redirect("weaponsmith")
	
@app.route("/armorsmith")
def show_armorsmith():
	armor = get_armor()
	pdb.set_trace()
	return render_template("armorsmith.html", armor=armor)

@app.route("/addweapon")
def make_armor():
	newArmor = {}
	newArmor['name'] = request.form['name']
	newArmor['name'] = request.form['name']
	newArmor['name'] = request.form['name']
	newArmor['name'] = request.form['name']
	newArmor['name'] = request.form['name']
	newArmor['name'] = request.form['name']
	armor = get_armor()
	allArmor = []#flatten here
	for type in armor.keys():
		allArmor.extend(armor[type])
	return render_template("armorsmith", armor=allArmor)

if __name__ == "__main__":
    app.run(host = "localhost")