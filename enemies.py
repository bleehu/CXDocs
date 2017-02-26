
import psycopg2

def get_monsters():
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, shock, will, reflex, description, pk_id FROM monsters ORDER BY name;")
	monsters = []
	results = myCursor.fetchall()
	for mun in results:
		newmun = {}
		#add new monster's stats. TODO: cast integers to ints
		newmun['name'] = mun[0]
		newmun['health'] = mun[1]
		newmun['nanites'] = mun[2]
		newmun['strength'] = mun[3]
		newmun['perception'] = mun[4]
		newmun['fortitude'] = mun[5]
		newmun['charisma'] = mun[6]
		newmun['intelligence'] = mun[7]
		newmun['dexterity'] = mun[8]
		newmun['luck'] = mun[9]
		newmun['shock'] = mun[10]
		newmun['will'] = mun[11]
		newmun['reflex'] = mun[12]
		newmun['description'] = mun[13]
		newmun['pk_id'] = mun[14]
		monster_id = mun[14]
		
		#add abilities
		newmun['abilities'] = get_monster_abilities(monster_id)
		#add armor
		newmun['armor'] = get_monsters_armor(monster_id)
		#add weapons
		newmun['weapons'] = get_monsters_weapons(monster_id)
		monsters.append(newmun)
	return monsters

def get_monster_abilities(monster_id):
	monster_abilities = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_abilities.pk_id, name, type, description FROM monsters_abilities, monsters_ability_map WHERE monsters_ability_map.fk_monster_id = %s AND monsters_ability_map.fk_ability_id = monsters_abilities.pk_id;" % monster_id)
	results = myCursor.fetchall()
	for line in results:
		ability = {}
		ability['pk_id'] = line[0]
		ability['name'] = line[1]
		ability['type'] = line[2]
		ability['description'] = line[3]
		monster_abilities.append(ability)
	return monster_abilities

def get_monster_abilities_all():
	monster_abilities = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT pk_id, name, type, description FROM monsters_abilities ORDER BY name;")
	results = myCursor.fetchall()
	for line in results:
		ability = {}
		ability['pk_id'] = line[0]
		ability['name'] = line[1]
		ability['type'] = line[2]
		ability['description'] = line[3]
		monster_abilities.append(ability)
	return monster_abilities

def get_monsters_armor(monster_id):
	monster_armor = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_armors.pk_id, name, coverage, damagereduction, description FROM monsters_armors, monsters_armor_map WHERE monsters_armor_map.fk_monster_id = %s AND monsters_armor_map.fk_armor_id = monsters_armors.pk_id ORDER BY name;" % monster_id)
	results = myCursor.fetchall()
	for line in results:
		armor = {}
		armor['pk_id'] = line[0]
		armor['name'] = line[1]
		armor['coverage'] = line[2]
		armor['damageReduction'] = line[2]
		armor['description'] = line[4]
		monster_armor.append(armor)
	return monster_armor

def get_monsters_weapons(monster_id):
	monster_weapons = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_weapons.pk_id, name, range, damage, accuracy, capacity, description FROM monsters_weapons, monsters_weapon_map WHERE monsters_weapon_map.fk_monster_id = %s AND monsters_weapon_map.fk_weapons_id = monsters_weapons.pk_id ORDER BY name;" % monster_id)
	results = myCursor.fetchall()
	for line in results:
		weapon = {}
		weapon['pk_id'] = line[0]
		weapon['name'] = line[1]
		weapon['range'] = line[2]
		weapon['damage'] = line[3]
		weapon['accuracy'] = line[4]
		weapon['capacity'] = line[5]
		weapon['description'] = line[6]
		monster_weapons.append(weapon)
	return monster_weapons

def validate_monster(form):
	expected = set(['name', 'description', 'strength', 'perception', 'dexterity', 'fortitude', 'charisma', 'intelligence', 'luck', 'reflex', 'will', 'shock', 'health', 'nanites', 'level', 'role'])
	if expected ^ set(form.keys()) != set([]):
		return False
	monster = {}
	try:
		monster['health'] = int(form['health'])
		monster['nanites'] = int(form['nanites'])
		monster['strength'] = int(form['strength'])
		monster['perception'] = int(form['perception'])
		monster['dexterity'] = int(form['dexterity'])
		monster['fortitude'] = int(form['fortitude'])
		monster['charisma'] = int(form['charisma'])
		monster['intelligence'] = int(form['intelligence'])
		monster['luck'] = int(form['luck'])
		monster['reflex'] = int(form['reflex'])
		monster['will'] = int(form['will'])
		monster['shock'] = int(form['shock'])
		monster['level'] = int(form['level'])
		monster['role'] = sql_escape(form['role'])[:30]
		monster['description'] = sql_escape(form['description'])[:3000]
		monster['name'] = sql_escape(form['name'])[:46]
	except Exception (e):
		return False
	if monster['health'] < 1 or monster['nanites'] < 1 or monster['strength'] < 1 or monster['perception'] < 1 or monster['fortitude'] < 1 or monster['charisma'] < 1 or monster['intelligence'] < 1 or monster['luck'] < 1 or monster['level'] < 1:
		return False
	if monster['description'].strip() == '' or monster['name'].strip() == '':
		return False
	return monster

def validate_monster_ability(form):
	expected = set(['type', 'description', 'name'])
	if expected ^ set(form.keys()) != set([]):
		return False
	ability = {}
	try:
		ability['name'] = sql_escape(form['name'])[:60]
		ability['type'] = sql_escape(form['type'])[:60]
		ability['description'] = sql_escape(form['description'])[:3000]
	except Exception(e):
		return False
	if ability['name'].strip() == '' or ability['type'].strip() == '' or ability['description'].strip() == '':
		return False
	return ability

def validate_monster_ability_map(form):
	expected = set(['monster_id', 'ability_id'])
	if expected ^ set(form.keys()) != set([]):
		return False
	monster_id = None
	ability_id = None
	try:
		monster_id = int(form['monster_id'])
		ability_id = int(form['ability_id'])
	except Exception(e):
		return False
	if ability_id < 1 or monster_id < 1:
		return False
	return {'monster_id':monster_id, 'ability_id':ability_id}

def insert_monster(monster):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	monstring = (monster['name'], monster['health'], monster['nanites'], monster['strength'], monster['perception'], monster['dexterity'], monster['fortitude'], monster['charisma'], monster['intelligence'], monster['luck'], monster['reflex'], monster['will'], monster['shock'], monster['level'], monster['role'], monster['description'])
	myCursor.execute("INSERT INTO monsters (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, reflex, will, shock, level, role, description) VALUES (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s' );" % monstring)
	myCursor.close()
	connection.commit()
	
def insert_monster_ability(ability):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	abstring = (ability['name'], ability['type'], ability['description'])
	myCursor.execute("INSERT INTO monsters_abilities (name, type, description) VALUES (E'%s', E'%s', E'%s' );" % abstring)
	myCursor.close()
	connection.commit()
	

def insert_monster_ability_map(mapping):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	mapstring = (mapping['monster_id'], mapping['ability_id'])
	myCursor.execute("INSERT INTO monsters_ability_map (fk_monster_id, fk_ability_id) VALUES (%s, %s)" % mapstring)
	myCursor.close()
	connection.commit()

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
	
""" 
	sql commands for initializing monsters database for tracking the beastiary
	
	CREATE SEQUENCE monsters_pk_seq NO CYCLE;
	CREATE TABLE monsters (
		pk_id int primary key default nextval('monsters_pk_seq'),
		name text NOT NULL,
		health int NOT NULL CHECK (health > 0),
		nanites int NOT NULL CHECK (nanites > 0),
		strength int NOT NULL CHECK (strength > 0),
		perception int NOT NULL CHECK (perception > 0),
		fortitude int NOT NULL CHECK (fortitude > 0),
		charisma int NOT NULL CHECK (charisma > 0),
		intelligence int NOT NULL CHECK (intelligence > 0),
		dexterity int NOT NULL CHECK (dexterity > 0),
		luck int NOT NULL CHECK (luck > 0),
		level int NOT NULL CHECK (level > -1),
		shock int NOT NULL,
		will int NOT NULL,
		reflex int NOT NULL,
		description text,
		role text
	);
	INSERT INTO monsters (name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, shock, will, reflex, description, role, level) VALUES ('Pirate Breacher', 210, 70, 8,3,10,2,2,6,2,12,12,6, 'A 200lb 6 foot man holding a crude rusty shotgun walks with a heavy gait. His hair is greasy and wild, and should you get close enough, you smell that he clearly has not showered in days. He wears a gas mask over his face patched with duct tape, but the soft "cooh-pah" that it makes in time with his breathing clearly shows that it is functional.', 'Tank', 5);
	CREATE TABLE monsters_abilities (
		pk_id int primary key default nextval('monster_ability_pk_seq'),
		name text NOT NULL,
		type text NOT NULL,
		description text NOT NULL
	);
	INSERT INTO monsters_abilities (name, type, description) values ( 'Bulltrue', 'reaction', E'Once per round when an enemy moved into an area that the breacher can see which is within 3m and if the breacher has a round still in their shotgun and the weapon is drawn cher may interrupt their opponent\'s turn to fire at that enemy. The enemy then resumes their turn as normal.');
	SELECT monsters.name, monsters_abilities.name FROM monsters, monsters_abilities, monster_ability_map WHERE monster_ability_map.fk_monster_id = monsters.pk_id AND monster_ability_map.fk_ability_id = monsters_abilities.pk_id;
	 CREATE TABLE monsters_armors(
		pk_id int primary key default nextval('monster_armor_pk_seq'),
		name text NOT NULL,
		coverage int NOT NULL CHECK (coverage > -1) CHECK (coverage < 101),
		damageReduction int NOT NULL CHECK (damageReduction > -1),
		description TEXT);
	CREATE TABLE monsters_weapons(
		pk_id int primary key default nextval('monster_weapon_pk_seq'),
		name text NOT NULL,
		range int NOT NULL CHECK (range > -1),
		damage int NOT NULL CHECK (damage > -1),
		accuracy int NOT NULL CHECK (accuracy > -101) CHECK (accuracy < 101),
		capacity int NOT NULL CHECK (capacity > -1),
		description text);
	CREATE TABLE monsters_armor_map(
		pk_id int primary key default nextval('monster_armor_map_pk_seq'),
		fk_monster_id int references monsters(pk_id),
		fk_monsters_armors int references monsters_armors(pk_id));
	CREATE TABLE monsters_weapon_map(
		pk_id int primary key default nextval('monster_weapon_map_pk_seq'),
		fk_monster_id int references monsters(pk_id),
		fk_weapons_id int references monsters_weapons(pk_id));
	GRANT UPDATE on monster_ability_pk_seq TO searcher;
	GRANT SELECT, INSERT, DELETE on monsters_abilities TO searcher;
	GRANT UPDATE ON monsters_ability_map TO searcher;
	GRANT UPDATE ON monster_ability_map_pk_seq TO searcher;
	GRANT INSERT, DELETE ON monsters_ability_map TO searcher;
	ALTER TABLE monsters_ability_map DROP CONSTRAINT monsters_ability_map_fk_ability_id_fkey;
	SELECT * FROM information_schema.key_column_usage WHERE position_in_unique_constraint is not null;
ALTER TABLE monsters_ability_map ADD CONSTRAINT monsters_ability_map_fk_ability_id_fkey
foreign key (fk_ability_id) references monsters_abilities(pk_id)
 on delete cascade;
	"""