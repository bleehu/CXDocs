import argparse
from base64 import b64encode, b64decode
import character
import csv
from flask import Flask, render_template, request, redirect, session, escape
import json
from mission import Mission
import pdb
import psycopg2
import os
import logging
import xml.etree.ElementTree
app = Flask(__name__)
app.config.from_object(__name__)
global log

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", metavar="###.###.###.###", help="Your local IP address. use ifconfig on linux.")
	parser.add_argument("-u", metavar="PostgresUsername", help="Username for PSQL login profile.")
	parser.add_argument("-p", metavar="PostgresPassword", help="Password for PSQL login profile.")
	args = parser.parse_args()
	return args

def check_auth(session):
	if 'username' not in session.keys():
		log.error("Anonymous attempt to access %s! user_agent:%s, remoteIP:%s" % (request.path, request.user_agent.string, request.remote_addr))
		return False
	blacklisted_UA = ['zgrab', 'vas', 'burp']
	for ua in blacklisted_UA:
		if ua in request.user_agent.string.lower():
			return False
	return True

def sql_escape(dirty):
	#string.replace(new, old)
	sani = dirty.replace('*','')
	sani = sani.replace('=','')
	sani = sani.replace('>','')
	sani = sani.replace('<','')
	sani = sani.replace(';','')
	return sani

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
	
def get_guns(session):
	goons = None
	with open("docs/guns.json") as gunfile:
		goons = json.loads(gunfile.read())
	for type in goons:
		toRemove = [] #can't remove in first pass or it'll screw up the iterator
		for peice in goons[type]:
			peice['minLevel'] = int(peice['minLevel'])
			if 'username' in session.keys() or peice['minLevel'] < 10: #hide lv 10 content unless logged in
				peice['cost'] = int(peice['cost'])
				peice['damage'] = int(peice['damage'])
				peice['mag'] = int(peice['mag'])
			else:
				print "removed %s" % peice['name']
				toRemove.append(peice)
		if len(toRemove) > 0:
			for popper in toRemove:
				goons[type].remove(popper)
	return goons

def get_items():
	goons = None
	with open("docs/items1.json") as itemfile:
		goons = json.loads(itemfile.read())
	return goons

def get_armor(session):
	arms = None
	types = []
	by_type = {}
	with open("docs/armor.json") as armfile:
		arms = json.loads(armfile.read())
	for type in arms:
		toHide = []
		for set in arms[type]:
			set['minLevel'] = int(set['minLevel'])
			if 'username' in session.keys() or set['minLevel'] < 10: #don't serve level 10 gear unless logged in
				set['cost'] = int(set['cost'])
				set['primaryMags'] = int(set['primaryMags'])
				set['secondaryMags'] = int(set['secondaryMags'])
				#set['damageReduction'] = int(set['damageReduction']) +1d10 is screwing it up
			else:
				toHide.append(set)
		if len(toHide) > 0:
			for hider in toHide:
				arms[type].remove(hider)
	return arms

def get_missions():
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT * FROM missions ORDER BY level;")
	missions = []
	results = myCursor.fetchall()
	for miss in results:
		pk = int(miss[0])
		name = miss[1]
		description = miss[2]
		level = int(miss[3])
		new_mission = Mission(pk, name, level, description)
		missions.append(new_mission)
	return missions

def get_playercharacters():
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT name, level, race, class, players.displayname FROM characters JOIN players ON characters.owner_fk = players.pk_id ORDER BY displayname, level, name;")
	pcs = []
	results = myCursor.fetchall()
	for pc in results:
		newPC = {}
		newPC['name'] = pc[0]
		newPC['level'] = int(pc[1])
		newPC['race'] = pc[2]
		newPC['class'] = pc[3]
		newPC['displayname'] = pc[4]
		pcs.append(newPC)
	return pcs


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

def get_user_postgres(username, password):
	if args.u != None and args.p != None:
		#if postgres username and password is set,
		#use username lookup to check username and password
		connection = psycopg2.connect("dbname=mydb user=%s password=%s" % (args.u, args.p))
		myCursor = connection.cursor()
		saniUser = sql_escape(username)
		myCursor.execute("SELECT * FROM users WHERE username LIKE '%s';" % saniUser)
		results = myCursor.fetchall()
		for result in results:
			if password == result[4]:
				log.info('logged in: %s. Password matches.' % saniUser )
				return result
		return None
	else:
		return None
	
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
	pc = None
	if 'character' in session.keys():
		pc = character.from_string(session['character'])
	return render_template('index.html', session=session, character=pc)

@app.route("/levelup")
def levelUp():
	levels = get_levels()
	return render_template('levelup.html', levels=levels)
	
@app.route("/guns")
def show_guns():
	guns = get_guns(session)
	return render_template('guns.html', guns=guns, session=session)

@app.route("/searchguns/<type>")
def show_gun_type(type):
	guns = get_guns(session)
	if type in guns.keys():
		guns = {type:guns[type.lower()]}
		return render_template('guns.html', guns=guns, session=session)
	else:
		show_guns()

@app.route("/characterguns")
def character_guns():
	if 'username' not in session.keys():
		return redirect("/")
	if 'character' not in session.keys():
		return redirect("/")
	character_string = session['character']
	my_character = character.from_string(character_string)
	classes = get_classes()
	my_class = None
	for cc in classes:
		if my_character.my_class == cc['name']:
			my_class = cc
	usable = {}
	profs = []
	for proficiency in my_class['Weapon Proficiencies']:
		profs.append(proficiency.lower())
	guns = get_guns(session)
	for type in guns.keys():
		if type.lower() + 's' in profs:
			usable[type.lower()] = []
			for gun in guns[type]:
				if gun['minLevel'] <= my_character.level:
					usable[type].append(gun)
	return render_template('guns.html', guns=usable, session=session)
	
@app.route("/armor")
def show_armor():
	armor = get_armor(session)
	return render_template('armor.html', armors=armor, session=session)

@app.route("/show/character")
def show_char_select():
	if 'username' not in session.keys():
		return redirect("/")
	chars = character.get_characters(session)
	if 'character' in session.keys():
		pc = character.from_string(session['character'])
	return render_template('character_select.html', characters=chars, session=session, character=pc)

@app.route("/playercharacters")
def show_player_characters():
	#SELECT name, level, race, class, users.displayname FROM characters JOIN users ON characters.owner_fk = users.pk ORDER BY displayname, level, name;
	pcs = get_playercharacters()
	return render_template("player_characters.html", pcs = pcs)
	
@app.route("/select/character", methods=['POST'])
def char_select():
	if not check_auth(session):
		return redirect("/")
	character_blob = character.get_characters(session)
	select_pk = int(request.form['pk'])
	for player_character in character_blob['characters']:
		if player_character.pk == select_pk:
			session['character'] = str(player_character)
	return redirect("/show/character")

@app.route("/modify/character/<pk>")
def char_modify(pk):
	if 'username' not in session.keys():
		return redirect("/")
	to_mod = None
	char_blob = character.get_characters(session)
	if int(pk) not in char_blob['pk_list']:
		return redirect("/show/character")
	for pc in char_blob['characters']:
		if pc.pk == int(pk):
			to_mod = pc
			return render_template("character_modify.html", session=session, character=to_mod)

@app.route("/mod/character", methods=['POST'])
def char_mod():
	if not check_auth(session):
		return redirect("/")

@app.route("/items")
def show_items():
	items = get_items()
	return render_template('items.html', items=items, session=session)

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
	if not check_auth(session):
		return redirect("/")
	guns = get_guns(session)
	return render_template("weaponsmith.html", guns=guns, session=session)

@app.route("/addgun", methods=['POST'])
def make_gun():
	if not check_auth(session):
		return redirect("/")
	gun = {}
	gun['name'] = request.form['gunname']
	gun['range'] = request.form['range']
	gun['damage'] = request.form['gunDamage']
	gun['type'] = request.form['gunType']
	gun['mag'] = request.form['mag']
	gun['toMiss'] = request.form['toMiss']
	gun['effect'] = request.form['effect']
	gun['cost'] = request.form['cost']
	gun['magcost'] = request.form['magcost']
	gun['minLevel'] = request.form['minLevel']
	if request.form['manufacturer']:
		gun['manufacturer'] = request.form['manufacturer']
	guns = get_guns(session)
	type = gun['type'].lower()
	if type not in guns.keys():
		guns[type] = []
	guns[type].append(gun)
	json_string = json.dumps(guns)
	with open("docs/guns.json", 'w') as gunfile:
		gunfile.write(json_string)
	log.info("%s added new gun: %s", (session['username'], gun['name']))
	return redirect("weaponsmith")

@app.route("/missions")
def show_missions():
	missions = get_missions()
	return render_template("missions.html", missions = missions)

@app.route("/itemsmith")
def show_itemsmith():
	if not check_auth(session):
		return redirect("/")
	items = get_items()
	return render_template("itemsmith.html", items = items, session=session)

@app.route("/additem", methods=['POST'])
def make_item():
	if not check_auth(session):
		return redirect("/")
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
	log.info("%s added new race: %s", (session['username'], item['name']))
	return redirect("itemsmith")

	
@app.route("/armorsmith")
def show_armorsmith():
	if not check_auth(session):
		return redirect("/")
	armor = get_armor(session)
	return render_template("armorsmith.html", armor=armor, session=session)

@app.route("/addarmor", methods=['POST'])
def make_armor():
	if not check_auth(session):
		return redirect("/")
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
	armor = get_armor(session)
	if newArmor['type'] not in armor.keys():
		armor[newArmor['type']] = []
	armor[newArmor['type']].append(newArmor)
	json_string = json.dumps(armor)
	with open("docs/armor.json", 'w') as armorfile:
		armorfile.write(json_string)
	log.info("%s added new armor: %s", (session['username'], newArmor['name']))
	return redirect("armorsmith")

@app.route("/racesmith")
def show_racesmith():
	if not check_auth(session):
		return redirect("/")
	races = get_races()
	return render_template("racesmith.html", races=races, session=session)

@app.route("/addrace", methods=['POST'])
def make_race():
	if not check_auth(session):
		return redirect("/")
	newRace = {}
	newRace['name'] = request.form['name']
	newRace['society'] = request.form['society']
	newRace['world'] = request.form['world']
	newRace['info'] = request.form['info']
	newRace['type'] = request.form['type']
	newRace['size'] = request.form['size']
	newRace['speed'] = request.form['speed']
	newRace['mods'] = request.form['mods']
	newRace['languages'] = request.form['languages']
	newRace['traits'] = request.form['traits']
	newRace['weaks'] = request.form['weaks']
	races = get_races()
	races.append(newRace)
	json_string = json.dumps(races)
	with open("docs/races.json", 'w') as racefile:
		racefile.write(json_string)
	log.info("%s added new race: %s", (session['username'], newRace['name']))
	return redirect("racesmith")
	
@app.route("/login", methods=['POST'])
def login():
	form = request.form
	uname = escape(form['uname'])
	passwerd = escape(form['password'])
	if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
		session.pop('X-CSRF', None)
	else:
		resp = make_response(render_template("501.html"), 403)
		log.error("An attacker removed their CSRF token! uname:%s, pass:%s, user_agent:%s, remoteIP:%s" % (uname, passwerd, request.user_agent.string, request.remote_addr))
		return resp
	user = get_user_postgres(uname, passwerd)
	if user != None:
		session['username'] = uname
		session['displayname'] = user[2]
		session['role'] = user[5]
		log.info("%s logged in" % uname)
	else:
		log.warn("%s failed to log in with password %s. user_agent:%s, remoteIP:%s" % (uname, passwerd, request.user_agent.string, request.remote_addr))
	return redirect("/")

@app.route("/logout", methods=['POST'])
def logout():
	form = request.form
	if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
		log.info("%s logged out" % session['username'])
		session.pop('username', None)
		session.pop('character', None)
	return redirect("/")

"""Most legitimate web scrapers check a text file in /robots.txt to see 
	where they should be allowed to look. This is how google, bing and bindu
	catalogue pages available to search. By default, we tell these robots to
	leave us alone."""
@app.route('/robots.txt')
def roblocker():
	return "User-agent: *\nDisallow: /"

@app.errorhandler(500)
def borked_it(error):
	uname = "Anonymous"
	if 'username' in session.keys():
		uname = session['username']
	log.error("%s got a 500 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
	return render_template("501.html", error=error)
	
@app.errorhandler(404)
def missed_it(error):
	uname = "Anonymous"
	if 'username' in session.keys():
		uname = session['username']
	log.warn("%s got a 404 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
	return render_template("404.html", error=error)

if __name__ == "__main__":
	args = get_args()
	host = "localhost"
	if args.i:
		host = args.i
	local_dir = os.path.dirname(__file__)
	log_filename = os.path.join(local_dir,"cxDocs.log")
	logging.basicConfig(filename=log_filename, level=logging.INFO)
	global log
	log = logging.getLogger("cxDocs:")
	app.secret_key = '$En3K9lEj8GK!*v9VtqJ' #todo: generate this dynamically
	#app.config['SQLAlchemy_DATABASE_URI'] = 'postgresql://searcher:AllDatSQL@localhost/mydb'
	#app.config['SQLAlchemy_ECHO'] = True
	app.run(host = host)