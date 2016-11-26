#must have a postgres database running in order to connect to one!

#check out https://www.postgresql.org/docs/9.5/static/tutorial-createdb.html for help setting up pyton
#postgres comes with ubuntu. Use the command psql --help

#check out http://initd.org/psycopg/docs/usage.html for more python using SQL


import psycopg2

def postgre_test():
	connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
	myCursor = connection.cursor()
	myCursor.execute("SELECT * FROM missions;")
	result = myCursor.fetchone()
	print result
	
if __name__ == "__main__":
	postgre_test()