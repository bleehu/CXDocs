import psycopg2
import pdb

def get_monsters():
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, shock, will, reflex, description, pk_id, author FROM monsters ORDER BY name;")
	monsters = []
	results = myCursor.fetchall()
	for mun in results:
		newmun = {}
		#add new monster's stats. TODO: cast integers to ints
		newmun['name'] = mun[0]
		newmun['health'] = mun[1]
		newmun['nanites'] = mun[2]
		newmun['strength'] = int(mun[3])
		newmun['perception'] = int(mun[4])
		newmun['fortitude'] = int(mun[5])
		newmun['charisma'] = int(mun[6])
		newmun['intelligence'] = int(mun[7])
		newmun['dexterity'] = int(mun[8])
		newmun['luck'] = int(mun[9])
		newmun['shock'] = int(mun[10])
		newmun['will'] = int(mun[11])
		newmun['reflex'] = int(mun[12])
		newmun['description'] = mun[13]
		newmun['pk_id'] = int(mun[14])
		newmun['author'] = mun[15]
		monster_id = mun[14]
		
		newmun['strmod'] = (newmun['strength'] - 5) * 4
		newmun['permod'] = (newmun['perception'] - 5) * 4
		newmun['fortmod'] = (newmun['fortitude'] - 5) * 4
		newmun['chamod'] = (newmun['charisma'] - 5) * 4
		newmun['intmod'] = (newmun['intelligence'] - 5) * 4
		newmun['dexmod'] = (newmun['dexterity'] - 5) * 4
		newmun['lukmod'] = (newmun['luck'] - 5) * 4
		
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
	myCursor.execute("SELECT monsters_abilities.pk_id, name, type, description, author FROM monsters_abilities, monsters_ability_map WHERE monsters_ability_map.fk_monster_id = %s AND monsters_ability_map.fk_ability_id = monsters_abilities.pk_id;" % monster_id)
	results = myCursor.fetchall()
	for line in results:
		ability = {}
		ability['pk_id'] = line[0]
		ability['name'] = line[1]
		ability['type'] = line[2]
		ability['description'] = line[3]
		ability['author'] = line[4]
		monster_abilities.append(ability)
	return monster_abilities
	
def get_abilitys_monsters(ability_id):
	abilitys_monsters = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_ability_map.pk_id, name FROM monsters, monsters_ability_map WHERE monsters_ability_map.fk_ability_id = %s AND monsters_ability_map.fk_monster_id = monsters.pk_id;" % ability_id)
	results = myCursor.fetchall()
	return results

def get_monster_abilities_all():
	monster_abilities = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT pk_id, name, type, description, author FROM monsters_abilities ORDER BY name;")
	results = myCursor.fetchall()
	for line in results:
		ability = {}
		ability['pk_id'] = line[0]
		ability['name'] = line[1]
		ability['type'] = line[2]
		ability['description'] = line[3]
		ability['author'] = line[4]
		monster_abilities.append(ability)
	return monster_abilities

def get_monster_armor_all():
	monster_armor = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT pk_id, name, description, damagereduction, coverage, type, author FROM monsters_armors ORDER BY name;")
	results = myCursor.fetchall()
	for line in results:
		suit = {}
		suit['pk_id'] = line[0]
		suit['name'] = line[1]
		suit['description'] = line[2]
		suit['damagereduction'] = line[3]
		suit['coverage'] = line[4]
		suit['type'] = line[5]
		suit['author'] = line[6]
		monster_armor.append(suit)
	return monster_armor

def get_monsters_armor(monster_id):
	monster_armor = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_armors.pk_id, name, coverage, damagereduction, description, monsters_armors.author FROM monsters_armors, monsters_armor_map WHERE monsters_armor_map.fk_monster_id = %s AND monsters_armor_map.fk_armor_id = monsters_armors.pk_id ORDER BY name;" % monster_id)
	results = myCursor.fetchall()
	for line in results:
		armor = {}
		armor['pk_id'] = line[0]
		armor['name'] = line[1]
		armor['coverage'] = line[2]
		armor['damageReduction'] = line[3]
		armor['description'] = line[4]
		armor['author'] = line[5]
		monster_armor.append(armor)
	return monster_armor

def get_armors_monsters(armor_id):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_armor_map.pk_id, name FROM monsters, monsters_armor_map WHERE monsters_armor_map.fk_armor_id = %s AND monsters_armor_map.fk_monster_id = monsters.pk_id;" % armor_id)
	results = myCursor.fetchall()
	return results
	

def get_monster_weapons_all():
	monster_weapons = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT pk_id, name, range, damage, accuracy, capacity, description, author, type FROM monsters_weapons ORDER BY name;")
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
		weapon['author'] = line[7]
		weapon['type'] = line[8]
		monster_weapons.append(weapon)
	return monster_weapons

def get_monsters_weapons(monster_id):
	monster_weapons = []
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_weapons.pk_id, name, range, damage, accuracy, capacity, description, monsters_weapons.author FROM monsters_weapons, monsters_weapon_map WHERE monsters_weapon_map.fk_monster_id = %s AND monsters_weapon_map.fk_weapons_id = monsters_weapons.pk_id ORDER BY name;" % monster_id)
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
		weapon['author'] = line[7]
		monster_weapons.append(weapon)
	return monster_weapons

def get_weapons_monsters(weapon_id):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT monsters_weapon_map.pk_id, name FROM monsters, monsters_weapon_map WHERE monsters_weapon_map.fk_weapons_id = %s AND monsters_weapon_map.fk_monster_id = monsters.pk_id;" % weapon_id)
	results = myCursor.fetchall()
	return results

def validate_monster(form, user):
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
		monster['author'] = user
		
		monster['strmod'] = (monster['strength'] - 5) * 4
		monster['permod'] = (monster['perception'] - 5) * 4
		monster['fortmod'] = (monster['fortitude'] - 5) * 4
		monster['chamod'] = (monster['charisma'] - 5) * 4
		monster['intmod'] = (monster['intelligence'] - 5) * 4
		monster['dexmod'] = (monster['dexterity'] - 5) * 4
		monster['lukmod'] = (monster['luck'] - 5) * 4
	except Exception (e):
		return False
	if monster['health'] < 1 or monster['nanites'] < 1 or monster['strength'] < 1 or monster['perception'] < 1 or monster['fortitude'] < 1 or monster['charisma'] < 1 or monster['intelligence'] < 1 or monster['luck'] < 1 or monster['level'] < 1:
		return False
	if monster['description'].strip() == '' or monster['name'].strip() == '':
		return False
	return monster

def validate_monster_ability(form, user):
	if user == None or user == '':
		return False
	expected = set(['type', 'description', 'name'])
	if expected ^ set(form.keys()) != set([]):
		return False
	ability = {}
	try:
		ability['name'] = sql_escape(form['name'])[:60]
		ability['type'] = sql_escape(form['type'])[:60]
		ability['description'] = sql_escape(form['description'])[:3000]
		ability['author'] = user
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
	

def validate_monster_weapon(form, user):
	if user == None or user == '':
		return False
	expected = set(['damage','range','name','description','toMiss','mag', 'cost', 'magCost', 'type'])
	if expected ^ set(form.keys()) != set([]):
		return False
	damage = None
	range = None
	name = None
	description = None
	accuracy = None
	capacity = None
	cost = None
	type = None
	magCost = None
	try:
		damage = int(form['damage'])
		range = int(form['range'])
		name = sql_escape(form['name'])
		description = sql_escape(form['description'])
		accuracy = int(form['toMiss'])
		capacity = int(form['mag'])
		type = sql_escape(form['type'])
		cost = int(form['cost'])
		magCost = int(form['magCost'])
	except:
		return False
	if range < 0 or cost < 0:
		return False
	if name == '' or description == '':
		return False
	return {'damage':damage,'range':range, 'name':name, 'description':description, 'toMiss':accuracy,'mag': capacity, 'cost':cost, 'magCost':magCost, 'type':type, 'author':user}

def validate_monster_weapon_map(form):
	expected = set(['monster_id', 'weapon_id'])
	if expected ^ set(form.keys()) != set([]):
		return False
	monster_id = None
	weapon_id = None
	try:
		monster_id = int(form['monster_id'])
		weapon_id = int(form['weapon_id'])
	except:
		return False
	if monster_id < 1 or weapon_id < 1:
		return False
	return {'monster_id': monster_id,'weapon_id':weapon_id}

def validate_monster_armor(form, user):
	if None == user or user == '':
		return False
	expected = set(['name', 'description', 'type', 'coverage', 'damagereduction'])
	if expected ^ set(form.keys()) != set([]):
		return False
	valid_armor = {}
	try:
		valid_armor['name'] = sql_escape(form['name'])
		valid_armor['description'] = sql_escape(form['description'])
		valid_armor['coverage'] = int(form['coverage'])
		valid_armor['damagereduction'] = sql_escape(form['damagereduction'])
		valid_armor['type'] = sql_escape(form['name'])
		valid_armor['author'] = user
		
	except:
		return False
	return valid_armor

def validate_monster_armor_map(form):
	expected = set(['monster_id', 'armor_id'])
	if expected ^ set(form.keys()) != set([]):
		return False
	monster_id = None
	armor_id = None
	try:
		monster_id = int(form['monster_id'])
		armor_id = int(form['armor_id'])
	except:
		return False
	return {'monster_id': monster_id, 'armor_id': armor_id}

def insert_monster(monster):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	monstring = (monster['name'], monster['health'], monster['nanites'], monster['strength'], monster['perception'], monster['dexterity'], monster['fortitude'], monster['charisma'], monster['intelligence'], monster['luck'], monster['reflex'], monster['will'], monster['shock'], monster['level'], monster['role'], monster['description'], monster['author'])
	myCursor.execute("INSERT INTO monsters (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, reflex, will, shock, level, role, description, author) VALUES (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', '%s');" % monstring)
	myCursor.close()
	connection.commit()
	
def insert_monster_ability(ability):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	abstring = (ability['name'], ability['type'], ability['description'], ability['author'])
	myCursor.execute("INSERT INTO monsters_abilities (name, type, description, author) VALUES (E'%s', E'%s', E'%s', '%s');" % abstring)
	myCursor.close()
	connection.commit()
	

def insert_monster_ability_map(mapping):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	mapstring = (mapping['monster_id'], mapping['ability_id'])
	myCursor.execute("INSERT INTO monsters_ability_map (fk_monster_id, fk_ability_id) VALUES (%s, %s)" % mapstring)
	myCursor.close()
	connection.commit()

def insert_monster_weapon(weapon):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	wepstring = (weapon['name'], weapon['range'], weapon['damage'], weapon['toMiss'], weapon['mag'], weapon['type'], weapon['description'], weapon['author'])
	myCursor.execute("INSERT INTO monsters_weapons (name, range, damage, accuracy, capacity, type, description, author) VALUES (E'%s', %s, %s, %s, %s, E'%s', E'%s', '%s');" % wepstring)
	myCursor.close()
	connection.commit()

def insert_monster_weapon_map(mapping):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	mapstring = (mapping['monster_id'], mapping['weapon_id'])
	myCursor.execute("INSERT INTO monsters_weapon_map (fk_monster_id, fk_weapons_id) VALUES (%s, %s)" % mapstring)
	myCursor.close()
	connection.commit()

def insert_monster_armor(armor):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	armorstring = (armor['name'], armor['coverage'], armor['damagereduction'], armor['type'], armor['description'], armor['author'])
	myCursor.execute("INSERT INTO monsters_armors (name, coverage, damagereduction, type, description, author) VALUES (E'%s', %s, %s, E'%s', E'%s', E'%s');" % armorstring)
	myCursor.close()
	connection.commit()

def insert_monster_armor_map(mapping):
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	mapstring = (mapping['monster_id'], mapping['armor_id'])
	myCursor.execute("INSERT INTO monsters_armor_map (fk_monster_id, fk_armor_id) VALUES (%s, %s)" % mapstring)
	myCursor.close()
	connection.commit()

def delete_monster_ability_map(map_id):
	del_id = None
	try:
		del_id = int(map_id)
	except:
		return None
	if del_id < 1:
		return None
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters_ability_map WHERE pk_id = %s;" % del_id)
	myCursor.close()
	connection.commit()

def delete_monster_weapon_map(map_id):
	del_id = None
	try:
		del_id = int(map_id)
	except:
		return None
	if del_id < 1:
		return None
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters_weapon_map WHERE pk_id = %s;" % del_id)
	myCursor.close()
	connection.commit()

def delete_monster_armor_map(map_id):
	del_id = None
	try:
		del_id = int(map_id)
	except:
		return None
	if del_id < 1:
		return None
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("DELETE FROM monsters_armor_map WHERE pk_id = %s;" % del_id)
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
		role text,
		author text
	);
	INSERT INTO monsters (name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, shock, will, reflex, description, role, level) VALUES ('Pirate Breacher', 210, 70, 8,3,10,2,2,6,2,12,12,6, 'A 200lb 6 foot man holding a crude rusty shotgun walks with a heavy gait. His hair is greasy and wild, and should you get close enough, you smell that he clearly has not showered in days. He wears a gas mask over his face patched with duct tape, but the soft "cooh-pah" that it makes in time with his breathing clearly shows that it is functional.', 'Tank', 5);
	CREATE TABLE monsters_abilities (
		pk_id int primary key default nextval('monster_ability_pk_seq'),
		name text NOT NULL,
		type text NOT NULL,
		description text NOT NULL,
		author text
	);
	INSERT INTO monsters_abilities (name, type, description) values ( 'Bulltrue', 'reaction', E'Once per round when an enemy moved into an area that the breacher can see which is within 3m and if the breacher has a round still in their shotgun and the weapon is drawn cher may interrupt their opponent\'s turn to fire at that enemy. The enemy then resumes their turn as normal.');
	SELECT monsters.name, monsters_abilities.name FROM monsters, monsters_abilities, monster_ability_map WHERE monster_ability_map.fk_monster_id = monsters.pk_id AND monster_ability_map.fk_ability_id = monsters_abilities.pk_id;
	 CREATE TABLE monsters_armors(
		pk_id int primary key default nextval('monster_armor_pk_seq'),
		name text NOT NULL,
		coverage int NOT NULL CHECK (coverage > -1) CHECK (coverage < 101),
		damageReduction int NOT NULL CHECK (damageReduction > -1),
		description TEXT,
		type TEXT NOT NULL,
		author text);
	CREATE TABLE monsters_weapons(
		pk_id int primary key default nextval('monster_weapon_pk_seq'),
		name text NOT NULL,
		range int NOT NULL CHECK (range > -1),
		damage int NOT NULL CHECK (damage > -1),
		accuracy int NOT NULL CHECK (accuracy > -101) CHECK (accuracy < 101),
		capacity int NOT NULL CHECK (capacity > -1),
		description text,
		author text);
	CREATE TABLE monsters_armor_map(
		pk_id int primary key default nextval('monster_armor_map_pk_seq'),
		fk_monster_id int references monsters(pk_id) ON DELETE CASCADE,
		fk_monsters_armors int references monsters_armors(pk_id)) ON DELETE CASCADE;
	CREATE TABLE monsters_weapon_map(
		pk_id int primary key default nextval('monster_weapon_map_pk_seq'),
		fk_monster_id int references monsters(pk_id) ON DELETE CASCADE,
		fk_weapons_id int references monsters_weapons(pk_id)) ON DELETE CASCADE;
	GRANT UPDATE on monster_ability_pk_seq TO searcher;
	GRANT INSERT, UPDATE, DELETE ON monsters_armors TO searcher;
	GRANT INSERT, UPDATE, DELETE ON monsters_armor_map TO searcher;
	GRANT SELECT, INSERT, DELETE on monsters_abilities TO searcher;
	GRANT UPDATE ON monster_armor_pk_seq TO searcher;
	GRANT UPDATE ON monsters_ability_map TO searcher;
	GRANT UPDATE ON monster_ability_map_pk_seq TO searcher;
	GRANT UPDATE ON monster_armor_pk_seq TO searcher;
	GRANT UPDATE ON monster_armor_map_pk_seq TO searcher;
	GRANT INSERT, DELETE ON monsters_ability_map TO searcher;
	ALTER TABLE monsters_ability_map DROP CONSTRAINT monsters_ability_map_fk_ability_id_fkey;
	SELECT * FROM information_schema.key_column_usage WHERE position_in_unique_constraint is not null;
ALTER TABLE monsters_ability_map ADD CONSTRAINT monsters_ability_map_fk_ability_id_fkey
foreign key (fk_ability_id) references monsters_abilities(pk_id)
 on delete cascade;
	"""