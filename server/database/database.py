import psycopg2
from ..cxExceptions import cxExceptions

"""This module creates a generic database that the enemy database and character 
databases inherit from. Ideally, this becomes the adapter for our use of the
psql driver, so if you wanted to switch to MySQL, this would be the only
file you would need to update."""

class CXDatabase(object):

    def __init__(self, config):
        self.db = PsqlDatabase(config)
        
    def fetch_all(self, queryString):
        return self.db.fetchall_from_db_query(queryString)

    def fetch_first(self, queryString):
        return self.db.fetchall_from_db_query(queryString)[0]

    def update(self, updateString):
        return self.db.update(updateString)

class PsqlDatabase():

    def __init__(self, config):
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.name = config['db_name']
        self.host = config['db_host']

    def db_connection(self):
        connection = psycopg2.connect("dbname=%s user=%s password=%s host=localhost" % \
            (self.name, self.username, self.password))
        return connection

    def fetchall_from_db_query(self, query):
        """Run a query on the character database and return all of the results."""
        connection = self.db_connection()
        myCursor = connection.cursor()
        myCursor.execute(query)
        returnMe = myCursor.fetchall()
        myCursor.close()
        connection.commit()
        return returnMe

    def fetch_first_from_db_query(self, query):
        """Run a query on the character database and return the first of the results"""
        all_rows = self.fetchall_from_db_query(query)
        return all_rows[0]

    def update(self, updateString):
        """Run and commit a query on the character database"""
        connection = self.db_connection()
        myCursor = connection.cursor()
        myCursor.execute(updateString)
        myCursor.close()
        connection.commit()

"""
#mysql isn't supported yet.
class mysql_database:
    def __init__(self):
        pass
"""