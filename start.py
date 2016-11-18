import argparse
from base64 import b64encode, b64decode
import csv
from flask import Flask, render_template, request, redirect, session, escape
import json
import pdb
import os
import xml.etree.ElementTree
app = Flask(__name__)
app.config.from_object(__name__)

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", metavar="###.###.###.###", help="Your local IP address. use ifconfig on linux.")
	args = parser.parse_args()
	return args

def get_classes():
	classless = None
	with open("docs/classes.json") as classFile:
		classString = classFile.read()
		blob = json.loads(classString)
		classless = blob['classes']
		#sort by name
	return classless

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
	with open("docs/guns.json") as gunfile:
		goons = json.loads(gunfile.read())
	return goons

def get_items():
	goons = None
	with open("docs/items1.json") as itemfile:
		goons = json.loads(itemfile.read())
	return goons

def get_armor():
	arms = None
	types = []
	by_type = {}
	with open("docs/armor.json") as armfile:
		arms = json.loads(armfile.read())
	return arms

def get_races():
	races = None
	with open("docs/races.json") as racefile:
		races = json.loads(racefile.read())
	return races
	
def get_users():
	all_users = None
	with open("static/users.enc", "r") as userDoc:
		decrypted = decode(userDoc.read())
		all_users = json.loads(decrypted)
	return all_users

def set_users(set_users_to):
	if str(type(set_users_to)) != "<type 'dict'>":
		raise ValueError("Cannot set users to a non-dictionary type")
	with open("users.enc", "w") as userDoc:
		encrypted = encode(json.dumps(set_users_to))
		userDoc.write(encrypted)

def decode(cypher):
	ascii = b64decode(cypher)
	plain = ""
	for char in ascii:
		plain = plain + chr(ord(char) - 12)
	return plain
	
def encode(cypher):
	rot12 = ""
	for char in cypher:
		rot12 = rot12 + chr(ord(char) + 12)
	return b64encode(rot12)

@app.route("/")
def hello():
	session['X-CSRF'] = "foxtrot"
	return render_template('index.html', session=session)

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
	items = get_items()
	return render_template('items.html', items=items)

@app.route("/races")
def show_races():
	races = get_races()
	return render_template('races.html', races=races)

@app.route("/rules")
def show_rules():
	root = xml.etree.ElementTree.parse("docs/rules.xml").getroot()
	sections = root.findall('section')
	return render_template('rules.html', sections=sections)

@app.route("/classes")
def show_classes():
	classless = get_classes()
	return render_template("classes.html", classes = classless)

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
	gun['mag'] = request.form['mag']
	gun['toMiss'] = request.form['toMiss']
	gun['effect'] = request.form['effect']
	gun['cost'] = request.form['cost']
	gun['minLevel'] = request.form['minLevel']
	if request.form['manufacturer']:
		gun['manufacturer'] = request.form['manufacturer']
	guns = get_guns()
	guns.append(gun)
	json_string = json.dumps(guns)
	with open("docs/guns1.json", 'w') as gunfile:
		gunfile.write(json_string)
	return redirect("weaponsmith")

@app.route("/itemsmith")
def show_itemsmith():
	items = get_items()
	return render_template("itemsmith.html", items = items)

@app.route("/additem", methods=['POST'])
def make_item():
	item = {}
	item['name'] = request.form['itemname']
	item['type'] = request.form['itemType']
	item['cost'] = request.form['cost']
	item['minLevel'] = request.form['minLevel']
	item['details'] = request.form['details']
	items = get_items()
	items.append(item)
	json_string = json.dumps(items)
	with open("docs/items1.json", 'w') as itemfile:
		itemfile.write(json_string)
	return redirect("itemsmith")

	
@app.route("/armorsmith")
def show_armorsmith():
	armor = get_armor()
	return render_template("armorsmith.html", armor=armor)

@app.route("/addarmor", methods=['POST'])
def make_armor():
	newArmor = {}
	newArmor['name'] = request.form['name']
	newArmor['damageReduction'] = request.form['dr']
	newArmor['type'] = request.form['type']
	newArmor['primaryMags'] = request.form['prime']
	newArmor['secondaryMags'] = request.form['secondary']
	newArmor['coverage'] = request.form['coverage']
	newArmor['cost'] = request.form['cost']
	newArmor['description'] = request.form['effect']
	newArmor['minLevel'] = request.form['minLevel']
	armor = get_armor()
	if newArmor['type'] not in armor.keys():
		armor[newArmor['type']] = []
	armor[newArmor['type']].append(newArmor)
	json_string = json.dumps(armor)
	with open("docs/armor.json", 'w') as armorfile:
		armorfile.write(json_string)
	return redirect("armorsmith")
	
@app.route("/login", methods=['POST'])
def login():
	pdb.set_trace()
	form = request.form
	uname = escape(form['uname'])
	passwerd = escape(form['password'])
	if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
		session.pop('X-CSRF', None)
	else:
		resp = make_response(render_template("501.html"), 403)
		return resp
	users = get_users()
	if uname in users.keys() and passwerd == users[uname]:
		session['username'] = uname
		
	
	return redirect("/")

@app.route("/logout", methods=['POST'])
def logout():
	form = request.form
	if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
		session.pop('username', None)
	return redirect("/")

@app.errorhandler(500)
def borked_it(error):
	return render_template("501.html", error=error)
	
@app.errorhandler(404)
def borked_it(error):
	return render_template("404.html", error=error)

if __name__ == "__main__":
	args = get_args()
	host = "localhost"
	if args.i:
		host = args.i
	app.secret_key = '$En3K9lEj8GK!*v9VtqJ' #todo: generate this dynamically
	app.run(host = host)