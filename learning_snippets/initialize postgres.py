#run $createdb mydb 
# and $psql mydb
#		#CREATE USER init PASSWORD 'st4tUp';
#		#GRANT postgres TO init;
# sudo nano /etc/postgresql/9.5/main/pg_hba.conf
# add the line 'local mydb init password' to the config file.
# restart.
#before running this script
#then be sure to run
#$psql mydb
#		#REVOKE postgres FROM init;
#when you're done. Otherwise there will be a rude security leak.


import psycopg2
import pdb

def postgre_initialize():
	connection = psycopg2.connect("dbname=mydb user=init password=st4tUp")
	myCursor = connection.cursor()
	pdb.set_trace()
	#initialize simple mission table
	myCursor.execute("CREATE SEQUENCE missions_pk_seq START WITH 3 NO CYCLE;")
	print myCursor.statusmessage
	myCursor.execute("CREATE TABLE missions (pk_id int primary key DEFAULT nextval('missions_pk_seq'), name text not null, description text not null, level int not null );")
	print myCursor.statusmessage
	myCursor.execute("INSERT INTO missions (name, description, level) VALUES ('Chasing Callihan','A dangerous terrorist is on the loose. Catch him!',1);")
	print myCursor.statusmessage
	connection.commit()
	myCursor.execute("SELECT * FROM missions;")
	result = myCursor.fetchone()
	print result
	
	#initialize sequences
	myCursor.execute("CREATE SEQUENCE events_pk_seq NO CYCLE;")
	myCursor.execute("CREATE SEQUENCE players_pk_seq NO CYCLE;")
	myCursor.execute("CREATE SEQUENCE characters_pk_seq NO CYCLE;")
	myCursor.execute("CREATE SEQUENCE weapons_pk_seq NO CYCLE;")
	myCursor.execute("CREATE SEQUENCE weapon_attachments_pk_seq NO CYCLE;")
	myCursor.execute("CREATE SEQUENCE armors_pk_seq NO CYCLE;")
	myCursor.execute("CREATE SEQUENCE armor_attachments_pk_seq NO CYCLE;")
	#create enum data types
	myCursor.execute("CREATE TYPE role AS ENUM ('ADMIN', 'DM', 'Player')")
	#initialize tables
	myCursor.execute("CREATE TABLE players (pk_id int primary key DEFAULT nextval('players_pk_seq'), username text NOT NULL, displayname text NOT NULL, realname text NOT NULL, password text NOT NULL, role role NOT NULL);")
	myCursor.execute("CREATE TABLE characters (pk_id int primary key DEFAULT nextval('characters_pk_seq'), owner_fk int references players(pk_id) NOT NULL, current_mission int references missions(pk_id), race text NOT NULL, class text NOT NULL, level int NOT NULL);")
	myCursor.execute("CREATE TABLE weapons (pk_id int primary key DEFAULT nextval('weapons_pk_seq'), owner_fk int references characters(pk_id) NOT NULL, name text NOT NULL, manufacturer text, miss int NOT NULL, range int NOT NULL, damage int NOT NULL, clip int NOT NULL, cost int NOT NULL, clip_cost int NOT NULL, notes text);")
	myCursor.execute("CREATE TABLE weapon_attachments (pk_id int primary key DEFAULT nextval('weapon_attachments_pk_seq'), on_fk int references weapons(pk_id) NOT NULL, name text NOT NULL, effect text NOT NULL);")
	myCursor.execute("CREATE TABLE armors (pk_id int primary key DEFAULT nextval('armors_pk_seq'), owner_fk int references characters(pk_id) NOT NULL, cost int NOT NULL, coverage int NOT NULL, damage_reduction int NOT NULL, notes text, primary_clips int NOT NULL, secondary_clips int NOT NULL);")
	myCursor.execute("CREATE TABLE armor_attachments (pk_id int primary key DEFAULT nextval('armor_attachments_pk_seq'), on_fk int references armors(pk_id) NOT NULL, name text NOT NULL, effect text NOT NULL);")
	myCursor.execute("CREATE TABLE events (pk_id int primary key DEFAULT nextval('events_pk_seq'), mission_fk int references missions(pk_id) NOT NULL, location text, time text);")
	
	#fill tables
	#the player table must be filled first, but we can't fill the table with passwords in plain text.
	#so you're gonna have to do this manually.
	
	#grant searcher permissions to look things up on these tables
	try:
		myCursor.execute("CREATE USER searcher PASSWORD 'allDatSQL';")
	except:
		print "Could not create searcher. Does the role already exist?"
	try:
		myCursor.execute("GRANT SELECT ON characters, weapons, weapon_attachments, armors, armor_attachments, events, missions TO searcher;")
		myCursor.execute("GRANT SELECT (pk_id, username, displayname) ON players TO searcher;")
	except:
		pass
	
	connection.commit()
	
	myCursor.close()
	connection.close()
	
if __name__ == "__main__":
	postgre_initialize()