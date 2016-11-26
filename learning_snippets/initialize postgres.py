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
	connection = psycopg2.connect("dbname=mydb2 user=init password=st4tUp")
	myCursor = connection.cursor()
	pdb.set_trace()
	myCursor.execute("CREATE SEQUENCE missions_pk_seq START WITH 3 NO CYCLE;")
	print myCursor.statusmessage
	myCursor.execute("CREATE TABLE missions (pk int primary key DEFAULT nextval('missions_pk_seq'), name text not null, description text not null, level int not null );")
	print myCursor.statusmessage
	myCursor.execute("INSERT INTO missions (name, description, level) VALUES ('Chasing Callihan','A dangerous terrorist is on the loose. Catch him!',1);")
	print myCursor.statusmessage
	connection.commit()
	myCursor.execute("SELECT * FROM missions;")
	result = myCursor.fetchone()
	print result
	myCursor.close()
	connection.close()
	
if __name__ == "__main__":
	postgre_initialize()