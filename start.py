import argparse #we use the argparse module for passing command-line arguments on startup.
from base64 import b64encode, b64decode
import characters
import ConfigParser
import csv #sometimes we save or read stuff in .csv format. This helps with that a lot.
#these imports are for python files we wrote ourselves. 
import docs_parser #our custom plaintext parser for reading CX rules straight from the repo

from enemies.enemy_routes import enemy_blueprint, initialize_enemies
from characters.character_routes import character_blueprint, initialize_characters

#flask is a python webserver built on Werkzeug. This is what is in charge of our 
#main web app. It's how we respond to HTTP requests, etc.
from flask import Flask, render_template, request, redirect, session, escape, flash

import guestbook #our custom guestbook for showing who all is on at once.
import json #sometimes we load or save things in json. This helps with that.
from mission import Mission #Mission is a custom data typ that we made to organize mission info on the backend.
import pdb	#Python Debuger is what I use to fix borked code. It should not be called in production EVER!
#but it's very helpful when being run locally.

import psycopg2 #psycopg2 lets us make posgres SQL calls from python. That lets us store things in databases
import os	#we need os to read and write files as well as to make our filepaths relative.
import logging #When we aren't running locally, we need the server to log what's happening so we can see any
#intrusions or help debug why it's breaking if it does so. This module handles that beautifully.
import security #our custom code that handles common security tasks like SQL sanitization
import xml.etree.ElementTree #Sometimes we write or read things in XML. This does that well.
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # 1024 bytes x 1024 is a MB. Prevents people from uploading 40 GB pictures
app.config.from_object(__name__)
app.register_blueprint(enemy_blueprint)
global log

global whos_on

"""We call this on startup to get all of the config info from command line. The username/password combination is
		used to prevent having to store the credentials on the box, so we don't have to defend data at rest."""
def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", metavar="###.###.###.###", help="Your local IP address. use ifconfig on linux.")
	parser.add_argument("-u", metavar="PostgresUsername", help="Username for PSQL login profile.")
	parser.add_argument("-p", metavar="PostgresPassword", help="Password for PSQL login profile.")
	args = parser.parse_args()
	return args

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
	for kind in arms:
		toHide = []
		for ageis in arms[kind]:
			for k, v in ageis.items():
				if v == '':
					ageis[k] = '0'
			ageis['minLevel'] = int(ageis['minLevel'])
			if 'username' in session.keys() or ageis['minLevel'] < 10: #don't serve level 10 gear unless logged in
				ageis['cost'] = int(ageis['cost'])
				ageis['primaryMags'] = int(ageis['primaryMags'])
				ageis['secondaryMags'] = int(ageis['secondaryMags'])
				#ageis['damageReduction'] = int(ageis['damageReduction']) +1d10 is screwing it up
			else:
				toHide.append(ageis)
		if len(toHide) > 0:
			for hider in toHide:
				arms[kind].remove(hider)
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

def get_races():
	races = None
	with open("docs/races.json") as racefile:
		races = json.loads(racefile.read())
	return races

def parser_page(config_option):
	if config.has_section('Parser') and config.has_option('Parser', config_option):
		rule_filepath = config.get('Parser', config_option)
		tokens = docs_parser.parse(rule_filepath)
		return render_template("parser.html", elements = tokens)
	else:
		flash("That feature isn't configured.")
		return redirect("/")

"""connect to user login database if said database is set up. uses psychopg2. 
			if user is not found or if posgres database info is not set, returns None. Returns 
			a tuple with username, displayname, realname and password if login is successful."""
def get_user_postgres(username, password, remoteIP):
	if args.u != None and args.p != None:
		#if postgres username and password is set,
		#use username lookup to check username and password
		connection = psycopg2.connect("dbname=mydb user=%s password=%s" % (args.u, args.p))
		myCursor = connection.cursor()
		#log the current attempt
		saniUser = security.sql_escape(username)
		saniPass = security.sql_escape(password)
		myCursor.execute("INSERT INTO login_audit_log (username, password, ip_address) VALUES ('%s', '%s', '%s');" \
			% (saniUser, saniPass, remoteIP))
		connection.commit()
		#check the number of attempts in the last half hour
		myCursor.execute("SELECT * FROM login_audit_log WHERE age(log_time) < '30 minutes' AND ip_address LIKE '%s' AND 'username' LIKE '%s';" % (remoteIP,saniUser))
		logins = myCursor.fetchall()
		if len(logins) > 4: #there have been more than 4 login attempts in the last 30 minutes
			log.error('RATE LIMIT LOGIN ATTEMPTS FROM %s, %s, %s' % (saniUser, saniPass, remoteIP))
			return None 
		myCursor.execute("SELECT * FROM users WHERE username LIKE '%s';" % saniUser)
		results = myCursor.fetchall()
		for result in results:
			if password == result[4]:
				log.info('logged in: %s. Password matches.' % saniUser )
				return result
		return None
	else:
		return None

"""handles the display of the main page for the site. """
@app.route("/")	#tells flask what url to trigger this behavior for. In this case, the main page of the site.
def hello():			#tells flask what method to use when you hit a particular route. Same as regular python function definition.
	session['X-CSRF'] = "foxtrot"	#set a session token. This helps prevent session takeover hacks. 
	pc = None	#player character defaults to None if user isn't logged in.
	docs = None
	if config.has_section('Parser'):
		docs = []
		if config.has_option('Parser', 'basic_rules_filepath'):
			docs.append(('Basic Rules','/docs/basic'))

		if config.has_option('Parser', 'races_filepath'):
			docs.append(('Races','/docs/races'))

		if config.has_option('Parser', 'classes_filepath'):
			docs.append(('Classes','/docs/classes'))

		if config.has_option('Parser', 'feats_filepath'):
			docs.append(('Feats','/docs/feats'))

		if config.has_option('Parser', 'melee_weapons_filepath'):
			docs.append(('Melee Weapons','/docs/meleeWeapons'))

		if config.has_option('Parser', 'pistols_filepath'):
			docs.append(('Pistols','/docs/pistols'))

		if config.has_option('Parser', 'smgs_filepath'):
			docs.append(('Submachine Guns','/docs/smgs'))

		if config.has_option('Parser', 'carbines_filepath'):
			docs.append(('Carbines and Assault Rifles','/docs/carbines'))

		if config.has_option('Parser', 'long_rifles_filepath'):
			docs.append(('Long Rifles and DMRs','/docs/longRifles'))

		if config.has_option('Parser', 'machineguns_filepath'):
			docs.append(('Machine Guns and Rocket Launchers','/docs/machineguns'))

		if config.has_option('Parser', 'weapon_attachments_filepath'):
			docs.append(('Weapon Attachments','/docs/weaponAttachments'))

		if config.has_option('Parser', 'armor_filepath'):
			docs.append(('Armor','/docs/armor'))

		if config.has_option('Parser', 'skills_filepath'):
			docs.append(('Skill','/docs/skills'))

		if config.has_option('Parser', 'items_filepath'):
			docs.append(('Items','/docs/items'))

		if config.has_option('Parser', 'Engineer_filepath'):
			docs.append(('Engineer Processes','/docs/engineers'))

		if config.has_option('Parser', 'Medic_filepath'):
			docs.append(('Medic Procedures','/docs/medics'))
	if 'character' in session.keys():	#if player is logged in and has picked a character, we load that character from the session string
		pc = characters.get_character(session['character']) 
	gb = guestbook.get_guestbook()
	return render_template('index.html', session=session, character=pc, docs=docs, guestbook = gb) #the flask method render_template() shows a jinja template 
	#jinja templates are kept in the /templates/ directory. Save them as .html files, but secretly, they use jinja to generate web pages
	#dynamically. 

@app.route("/whoshere")
def whosHereAPI():
	gbook = json.dumps(guestbook.get_guestbook())
	return gbook

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

#begin parser pages

@app.route("/docs/classes")
def docs_classes():
	return parser_page('classes_filepath')

@app.route("/docs/races")
def docs_races():
	return parser_page('races_filepath')

@app.route("/docs/items")
def docs_items():
	return parser_page('items_filepath')

@app.route("/docs/feats")
def docs_feats():
	return parser_page('feats_filepath')

@app.route("/docs/meleeWeapons")
def docs_melee():
	return parser_page('melee_weapons_filepath')

@app.route("/docs/pistols")
def docs_pistols():
	return parser_page('pistols_filepath')

@app.route("/docs/smgs")
def docs_smgs():
	return parser_page('smgs_filepath')

@app.route("/docs/carbines")
def docs_carbines():
	return parser_page('carbines_filepath')

@app.route("/docs/longRifles")
def docs_long_rifles():
	return parser_page('long_rifles_filepath')

@app.route("/docs/machineguns")
def docs_machineguns():
	return parser_page('machineguns_filepath')

@app.route("/docs/weaponAttachments")
def docs_wep_attachments():
	return parser_page('weapon_attachments_filepath')

@app.route("/docs/armor")
def docs_armor():
	return parser_page('armor_filepath')

@app.route("/docs/skills")
def docs_skills():
	return parser_page('skills_filepath')

@app.route("/docs/basic")
def docs_basic():
	return parser_page('basic_rules_filepath')

@app.route("/docs/medics")
def docs_medics():
	return parser_page('Medic_filepath')

@app.route("/docs/engineers")
def docs_engineers():
	return parser_page('Engineer_filepath')

#End parser pages

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
	if not security.check_auth(session):
		return redirect("/")
	guns = get_guns(session)
	return render_template("weaponsmith.html", guns=guns, session=session)

@app.route("/addgun", methods=['POST'])
def make_gun():
	if not security.check_auth(session):
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
	if not security.check_auth(session):
		return redirect("/")
	items = get_items()
	return render_template("itemsmith.html", items = items, session=session)

@app.route("/additem", methods=['POST'])
def make_item():
	if not security.check_auth(session):
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
	if not security.check_auth(session):
		return redirect("/")
	armor = get_armor(session)
	return render_template("armorsmith.html", armor=armor, session=session)

@app.route("/addarmor", methods=['POST'])
def make_armor():
	if not security.check_auth(session):
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
	if not security.check_auth(session):
		return redirect("/")
	races = get_races()
	return render_template("racesmith.html", races=races, session=session)

@app.route("/addrace", methods=['POST'])
def make_race():
	if not security.check_auth(session):
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
	user = get_user_postgres(uname, passwerd, request.remote_addr)
	if user != None:
		session['username'] = uname
		session['displayname'] = user[2]
		session['role'] = user[5]
		log.info("%s logged in" % uname)
		flash('Logged in.')
		guestbook.sign_guestbook(user[2])
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

@app.route("/gamelogs")
def gamelogs():
	return render_template("gamelogs.html")

@app.route("/designhowto")
def show_design_howto():
	return render_template("design_how_to.html")

@app.route("/monsterweaponshowto")
def show_monster_weapons_howto():
	return render_template("monster_weapon_how_to.html")

@app.route("/monsterarmorhowto")
def show_monster_armor_howto():
	return render_template("monster_armor_how_to.html")

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
    host = "localhost" #default to local only when running.
    
    global config
    config = ConfigParser.RawConfigParser()
    config.read('config/cxDocs.cfg')
    
    seconds_away = 60
    seconds_out = 3600
    if config.has_option('WhosHere', 'Seconds_away'):
    	seconds_away = config.get('WhosHere', 'Seconds_away')
    if config.has_option('WhosHere', 'Seconds_out'):
    	seconds_out = config.get('WhosHere', 'Seconds_out')
    guestbook.initialize(seconds_away, seconds_out)

    args = get_args()
    if args.i:	# if given a -i ip.ip.ip.address, open that on LAN, so friends can visit your site.
        host = args.i
    local_dir = os.path.dirname(__file__) #get local directory, so we know where we are saving files.
    log_filename = os.path.join(local_dir,"cxDocs.log") #save a log of web traffic in case something goes wrong.
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    global log
    log = logging.getLogger("cxDocs:")
    initialize_enemies(config, log)
    initialize_characters(config, log)
    app.secret_key = '$En3K9lEj8GK!*v9VtqJ' #todo: generate this dynamically
    #app.config['SQLAlchemy_DATABASE_URI'] = 'postgresql://searcher:AllDatSQL@localhost/mydb'
    #app.config['SQLAlchemy_ECHO'] = True
    
    app.run(host = host, threaded=True)
	
"""
CREATE SEQUENCE login_log_seq NO CYCLE; 
CREATE TABLE login_audit_log (
	pk_id int PRIMARY KEY DEFAULT nextval('login_log_seq'),
    username text NOT NULL,
    password text NOT NULL,
    ip_address text NOT NULL,
    log_time timestamp DEFAULT now()
);
GRANT UPDATE ON login_log_seq TO validator;
GRANT ALL ON login_audit_log TO validator;
"""

#was 1223 lines before split, is 714 after.