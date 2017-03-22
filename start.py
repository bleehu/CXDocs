import argparse #we use the argparse module for passing command-line arguments on startup.
from base64 import b64encode, b64decode
import character #character is a custom data type that we created to handle character information on the backend.
import csv #sometimes we save or read stuff in .csv format. This helps with that a lot.
#flask is a python webserver built on Werkzeug. This is what is in charge of our 
#main web app. It's how we respond to HTTP requests, etc.
import enemies
from flask import Flask, render_template, request, redirect, session, escape, flash
import json #sometimes we load or save things in json. This helps with that.
from mission import Mission #Mission is a custom data typ that we made to organize mission info on the backend.
import pdb	#Python Debuger is what I use to fix borked code. It should not be called in production EVER!
#but it's very helpful when being run locally.

import psycopg2 #psycopg2 lets us make posgres SQL calls from python. That lets us store things in databases
import os	#we need os to read and write files as well as to make our filepaths relative.
import logging #When we aren't running locally, we need the server to log what's happening so we can see any
#intrusions or help debug why it's breaking if it does so. This module handles that beautifully.
import xml.etree.ElementTree #Sometimes we write or read things in XML. This does that well.
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(__name__)
global log

"""We call this on startup to get all of the config info from comand line. The username/password combination is
		used to prevent having to store the credentials on the box, so we don't have to defend data at rest."""
def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", metavar="###.###.###.###", help="Your local IP address. use ifconfig on linux.")
	parser.add_argument("-u", metavar="PostgresUsername", help="Username for PSQL login profile.")
	parser.add_argument("-p", metavar="PostgresPassword", help="Password for PSQL login profile.")
	args = parser.parse_args()
	return args

""" we call this any time someone checks out a page on the site that should be off-limits to someone who
		hasn't logged in. If they aren't logged in, it returns false, if they are, it returns true."""
def check_auth(session):
	if 'username' not in session.keys():
		log.error("Anonymous attempt to access %s! user_agent:%s, remoteIP:%s" % (request.path, request.user_agent.string, request.remote_addr))
		return False
	blacklisted_UA = ['zgrab', 'vas', 'burp']
	for ua in blacklisted_UA:
		if ua in request.user_agent.string.lower():
			return False
	return True

""" we use this when we use player input to check postgres for a search. For instance, we don't want 
           badguys trying to log in with SQL injection - that could lead to damage to login data."""
def sql_escape(dirty):
	#string.replace(new, old)
	sani = dirty.replace('*','')
	sani = sani.replace('=','')
	sani = sani.replace('>','')
	sani = sani.replace('<','')
	sani = sani.replace(';','')
	sani = sani.replace("'","''")
	#sani = sani.replace("\\", "\\") #need a way to sanitize backslashes for escape characters
	return sani

"""returns a list of maps where the map represents a class. The value of map['name'] might = 'Soldier' and
			map['armorProficency'] might be equal to ['recon', 'medium', 'light']. Must have the correct .json
			file in /docs/ in order to work."""
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
	myCursor.execute("SELECT name, level, race, class, users.displayname FROM characters JOIN users ON characters.fk_owner = users.pk_id ORDER BY displayname, level, name;")
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
	
"""WARNING!!! DERECATED USE get_user_postgres() instead!"""
def get_users():
	print "WARNING! USE OF get_users() is deprecated due to vulnerability of encrypted user file! Please use Postgres instead!"
	all_users = None
	with open("static/users.enc", "r") as userDoc:
		decrypted = decode(userDoc.read())
		all_users = json.loads(decrypted)
	return all_users

"""connect to user login database if connected to said database. uses psychopg2. 
			if user not found or if posgres database info not set, returns None. Returns 
			a tuple with username, displayname, realname and password if login successful."""
def get_user_postgres(username, password):
	if args.u != None and args.p != None:
		#if postgres username and password is set,
		#use username lookup to check username and password
		connection = psycopg2.connect("dbname=mydb user=%s password=%s" % (args.u, args.p))
		myCursor = connection.cursor()
		saniUser = sql_escape(username)
		#pdb.set_trace()
		myCursor.execute("SELECT * FROM users WHERE username LIKE '%s';" % saniUser)
		results = myCursor.fetchall()
		for result in results:
			if password == result[4]:
				log.info('logged in: %s. Password matches.' % saniUser )
				return result
		return None
	else:
		return None

""" only used externally to write a sort-of encrypted local file with login info, in case 
		setting up postgres is too hard. set_users_to should be a dictionary of dictionaries
		were the first is sorted by username and the second layer of dictionaries holds the 
		information from the character.py data type."""
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

"""handles the display of the main page for the site. """
@app.route("/")	#tells flask what url to trigger this behavior for. In this case, the main page of the site.
def hello():			#tells flask what method to use when you hit a particular route. Same as regular python function definition.
	session['X-CSRF'] = "foxtrot"	#set a session token. This helps prevent session takeover hacks. 
	pc = None	#player character defaults to None if user isn't logged in.
	if 'character' in session.keys():	#if player is logged in and has picked a character, we load that character from the session string
		pc = character.from_string(session['character']) 
	return render_template('index.html', session=session, character=pc) #the flask method render_template() shows a jinja template 
	#jinja templates are kept in the /templates/ directory. Save them as .html files, but secretly, they use jinja to generate web pages
	#dynamically. 

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
	pc = None
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
	
@app.route("/files")
def show_files():
	return render_template("files.html")

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

@app.route("/monster")
def show_monsters():
	if not check_auth(session):
		return redirect("/")
	munsters = enemies.get_monsters()
	return render_template("monsters.html", monsters = munsters, session=session)

@app.route("/monstereditor")
def show_monster_editor():
	if not check_auth(session):
		return redirect("/")
	monsters = enemies.get_monsters()
	return render_template("monster_smith.html", session=session, monsters=monsters);

@app.route("/monsterpic")
def show_monster_photographer():
	if not check_auth(session):
		return redirect("")
	monsters = enemies.get_monsters()
	return render_template("monster_photographer.html", monsters=monsters)

@app.route("/newMonster", methods=['POST'])
def make_monster():
	if not check_auth(session):
		flash('Must be logged in to see this page');
		return redirect("/")
	user = session['displayname']
	monster = enemies.validate_monster(request.form, user)
	if not  monster:
		flash('Enemy invalid. Could not add');
		return redirect("/monstereditor")
	enemies.insert_monster(monster)
	flash('Enemy added!');
	return redirect("/monstereditor")

@app.route("/newMonsterpic", methods=['POST'])
def make_monster_pic():
	if not check_auth(session):
		flash('You must be logged in to do that. This incident has been logged.')
		return redirect('/')
	user = session['displayname']
	allowed_filetypes = set(['png'])
	file = request.files['monster_pic']
	filename = secure_filename(file.filename)
	if not '.' in filename and filename.split('.')[1].lower() in allowed_filetypes:
		flash('invalid file. This incident has been logged.')
		return redirect('/monsterpic')
	monster_id = int(request.form['monster_id'])
	file.save(os.path.join("/home/michaelhedges/Desktop/Secret stuff/Don't look in here/flaskr/CXDocs/static/images/monsters/bypk_id","%s.png" % monster_id))
	return redirect("/monsterpic")

@app.route("/newMonsterAbility", methods = ['POST'])
def make_monster_ability():
	if not check_auth(session):
		flash("Must be logged in to do that.")
		return redirect("/")
	user = session['displayname']
	ability = enemies.validate_monster_ability(request.form, user)
	if not ability:
		flash("New ability not valid. Could not add.")
		return redirect("/monsterabilityeditor")
	enemies.insert_monster_ability(ability)
	flash("Enemy Ability Added!")
	return redirect("/monsterabilityeditor")

@app.route("/newMonsterWeapon", methods = ['POST'])
def make_monster_weapon():
	if not check_auth(session):
		flash("Must be logged in to do that. This incident will be logged.")
		return redirect("/")
	user = session['displayname']
	weapon = enemies.validate_monster_weapon(request.form, user)
	if not weapon:
		flash("New Weapon is invalid. Could not add.")
		return redirect("/monsterweaponeditor")
	enemies.insert_monster_weapon(weapon)
	flash("Enemy Weapon Added to Armory!")
	return redirect("/monsterweaponeditor")

@app.route("/newMonsterArmor", methods=['Post'])
def make_monster_armor():
	if not check_auth(session):
		flash("Must be logged in to do that. This incident willbe logged.")
		return redirect("/")
	user = session['displayname']
	armor = enemies.validate_monster_armor(request.form, user)
	if not armor:
		flash("New Armor is invalid. Could not add.")
		return redirect("/monsterarmoreditor")
	enemies.insert_monster_armor(armor)
	flash("Enemy Armor Added successfully!")
	return redirect("/monsterarmoreditor")

@app.route("/assignMonsterAbility", methods=['POST'])
def make_monster_ability_mapping():
	if not check_auth(session):
		flash("Must be logged in to do that.")
		return redirect("/")
	mapping = enemies.validate_monster_ability_map(request.form)
	if not mapping:
		flash("New mapping not valid. Could not add.")
		return redirect("/monsterabilityeditor")
	enemies.insert_monster_ability_map(mapping)
	flash("Enemy Ability Assigned!")
	return redirect("/monsterabilityeditor")

@app.route("/assignMonsterWeapon", methods=['POST'])
def make_monster_weapon_mapping():
	if not check_auth(session):
		flash("Must be logged in to do that.")
		return redirect("/")
	mapping = enemies.validate_monster_weapon_map(request.form)
	if not mapping:
		flash("New mapping not valid. Could not add.")
		return redirect("/")
	enemies.insert_monster_weapon_map(mapping)
	flash("Weapon Assigned to Enemy Successfully!")
	return redirect("/monsterweaponeditor")

@app.route("/assignMonsterArmor", methods=['POST'])
def make_monster_armor_mapping():
	if not check_auth(session):
		flash("Must be logged in to do that.")
		return redirect("/")
	mapping = enemies.validate_monster_armor_map(request.form)
	if not mapping:
		flash("New armor assignment invalid. Could not add.")
		return redirect("/")
	enemies.insert_monster_armor_map(mapping)
	flash("Armor Assignment successful!")
	return redirect("/monsterarmoreditor")

@app.route("/deletemonster/<pk_id>", methods=['POST'])
def delete_monster(pk_id):
	if not check_auth(session):
		flash("Must be logged in to do that. This incident has been reported.")
		return redirect("/")
	monster_id = None
	try:
		monster_id = int(pk_id)
	except Exception(e):
		flash("error parsing id of monster. This incident will be logged.")
		return redirect("/monstereditor")
	
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters WHERE pk_id = %s;" % monster_id)
	myCursor.close()
	connection.commit()
	
	flash('Enemy deleted!')
	return redirect("/monstereditor")

@app.route("/deletemonsterability/<pk_id>", methods=['POST'])
def delete_monster_ability(pk_id):
	if not check_auth(session):
		flash("Must be logged in to do that. This incident will be logged.")
		return redirect("/")
	monster_ability_id = None
	try: 
		monster_ability_id = int(pk_id)
	except Exception(e):
		flash("Error Parsing ID of monster. This incident will be logged.")
		return redirect("/")
	
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters_abilities WHERE pk_id = %s;" % pk_id)
	myCursor.close()
	connection.commit()
	
	flash('ability Deleted')
	return redirect("/monsterabilityeditor")

@app.route("/deletemonsterweapon/<pk_id>", methods=['POST'])
def delete_monster_weapon(pk_id):
	if not check_auth(session):
		flash("must be logged in to do that. This incident will be reported.")
		return redirect("/")
	monster_weapon_id = None
	try:
		monster_weapon_id = int(pk_id)
	except Exception(e):
		flash("error parsing ID of monster. This incident will be logged")
		return redirect("/")
	
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters_weapons WHERE pk_id = %s;" % pk_id)
	myCursor.close()
	connection.commit()
	
	flash('weapon Deleted successfuly!')
	return redirect("/monsterweaponeditor")

@app.route("/deletemonsterarmor/<pk_id>", methods=['POST'])
def delete_monster_armor(pk_id):
	if not check_auth(session):
		flash("You must be logged in to do that. This incident will be looged.")
		return redirect("/")
	monster_armor_id = None
	try: 
		monster_armor_id = int(pk_id)
	except:
		flash("error parsing ID of monster. This incident will be logged.")
		return redirect("/")
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters_armors WHERE pk_id = %s;" % pk_id)
	myCursor.close()
	connection.commit()
	
	flash('armor Deleted successfuly!')
	return redirect("/monsterarmoreditor")

@app.route("/deletemonsterabilitymap", methods=['post'])
def delete_monster_ability_map():
	if not check_auth(session):
		flash("You must be logged in to do that. This incident has been logged.")
		return redirect("/")
	flash("Ability taken away successfully")
	enemies.delete_monster_ability_map(request.form['pk_id'])
	return redirect("/monsterabilities")

@app.route("/deletemonsterweaponmap", methods=['post'])
def delete_monster_weapon_map():
	if not check_auth(session):
		flash("You must be logged in to do that. This incident has been logged.")
		return redirect("/")
	flash("Weapon taken away successfully")
	enemies.delete_monster_weapon_map(request.form['pk_id'])
	return redirect("/monsterweapons")

@app.route("/deletemonsterarmormap", methods=['post'])
def delete_monster_armor_map():
	if not check_auth(session):
		flash("You must be logged in to do that. This incident has been logged.")
		return redirect("/")
	flash("Armor taken away successfully")
	enemies.delete_monster_armor_map(request.form['pk_id'])
	return redirect("/monsterarmor")

@app.route("/monsterabilities")
def show_monster_abilities():
	if not check_auth(session):
		flash("You must be logged in to see that.")
		return redirect("/")
	mAbilities = enemies.get_monster_abilities_all()
	munsters = enemies.get_monsters()
	for ability in mAbilities:
		maps = enemies.get_abilitys_monsters(ability['pk_id'])
		ability['maps'] = maps
	return render_template("monster_abilities.html", abilities=mAbilities, monsters=munsters)

@app.route("/monsterweapons")
def show_monster_weapons():
	if not check_auth(session):
		flash("you must be logged in to see that.")
		return redirect("/")
	mWeapons = enemies.get_monster_weapons_all()
	munsters = enemies.get_monsters()
	for weapon in mWeapons:
		maps = enemies.get_weapons_monsters(weapon['pk_id'])
		weapon['maps'] = maps
	return render_template("monster_weapons.html", weapons=mWeapons, monsters=munsters)

@app.route("/monsterarmor")
def show_monster_armor():
	if not check_auth(session):
		flash("you must be logged in to see that")
		return redirect("/")
	mArmor = enemies.get_monster_armor_all()
	munsters = enemies.get_monsters()
	for suit in mArmor:
		maps = enemies.get_armors_monsters(suit['pk_id'])
		suit['maps'] = maps
	return render_template("monster_armor.html", armor=mArmor, monsters=munsters)

@app.route("/monsterabilityeditor")
def show_monster_ability_editor():
	if not check_auth(session):
		flash("Must be logged in to do that.")
		return redirect("/")
	mAbilities = enemies.get_monster_abilities_all()
	munsters = enemies.get_monsters()
	return render_template("monster_ability_smith.html", session=session, abilities=mAbilities, monsters=munsters)

@app.route("/monsterweaponeditor")
def show_monster_weapon_editor():
	if not check_auth(session):
		flash("must be logged in to see that.")
		return redirect("/")
	mWeps = enemies.get_monster_weapons_all()
	munsters = enemies.get_monsters()
	return render_template("monster_weapon_smith.html", session=session, weapons=mWeps, monsters=munsters)

@app.route("/monsterarmoreditor")
def show_monster_armor_editor():
	if not check_auth(session):
		flash("you must be logged in to see that.")
		return redirect("/")
	mArmor = enemies.get_monster_armor_all()
	munsters = enemies.get_monsters()
	return render_template("monster_armor_smith.html", session=session, armor=mArmor, monsters=munsters)

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
		flash('Logged in.')
	else:
		log.warn("%s failed to log in with password %s. user_agent:%s, remoteIP:%s" % (uname, passwerd, request.user_agent.string, request.remote_addr))
		flash('Failed to log in; username or password incorrect.')
	return redirect("/")

@app.route("/logout", methods=['POST'])
def logout():
	form = request.form
	if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
		log.info("%s logged out" % session['username'])
		session.pop('username', None)
		session.pop('character', None)
	return redirect("/")

@app.route("/npcgen", methods=['GET'])
def npcgen():
	return render_template("npcgen.html")

"""Most legitimate web scrapers check a text file in /robots.txt to see 
	where they should be allowed to look. This is how google, bing and bindu
	catalogue pages available to search. By default, we tell these robots to
	leave us alone."""
@app.route('/robots.txt')
def roblocker():
	return "User-agent: *\nDisallow: /"

""" set generic handlers for common errors."""
@app.errorhandler(500) #an HTTP 500 is given when there's a server error, for instance if  there's a Nonetype error in python. 
def borked_it(error):
	uname = "Anonymous"
	if 'username' in session.keys():
		uname = session['username']
	log.error("%s got a 500 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
	return render_template("501.html", error=error)
	
@app.errorhandler(404) # an HTTP 404 Not Found happens if the user searches for a url which doesn't exist. like /fuzzyunicorns
def missed_it(error):
	uname = "Anonymous"
	if 'username' in session.keys():
		uname = session['username']
	log.warn("%s got a 404 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
	return render_template("404.html", error=error)

if __name__ == "__main__":
	args = get_args()
	host = "localhost" #default to local only when running.
	if args.i:	# if given a -i ip.ip.ip.address, open that on LAN, so friends can visit your site.
		host = args.i
	local_dir = os.path.dirname(__file__) #get local directory, so we know where we are saving files.
	log_filename = os.path.join(local_dir,"cxDocs.log") #save a log of web traffic in case something goes wrong.
	logging.basicConfig(filename=log_filename, level=logging.INFO)
	global log
	log = logging.getLogger("cxDocs:")
	app.secret_key = '$En3K9lEj8GK!*v9VtqJ' #todo: generate this dynamically
	#app.config['SQLAlchemy_DATABASE_URI'] = 'postgresql://searcher:AllDatSQL@localhost/mydb'
	#app.config['SQLAlchemy_ECHO'] = True
	app.run(host = host, threaded=True)
	