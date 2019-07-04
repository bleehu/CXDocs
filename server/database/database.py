import psycopg2
from ..cxExceptions import cxExceptions

"""This module creates a generic database that the enemy database and character 
databases inherit from. Ideally, this becomes the adapter for our use of the
psql driver, so if you wanted to switch to MySQL, this would be the only
file you would need to update."""

class CXDatabase(object):

    def __init__(self, config):
        self.db = PsqlDatabase(config)
        
    def fetch_all(self, query_string):
        return self.db.fetchall_from_db_query(query_string)

    def fetch_first(self, query_string):
        return self.db.fetchall_from_db_query(query_string)[0]

    def update(self, update_string):
        return self.db.update(update_string)

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
        my_cursor = connection.cursor()
        my_cursor.execute(query)
        return_me = my_cursor.fetchall()
        my_cursor.close()
        connection.commit()
        return return_me

    def fetch_first_from_db_query(self, query):
        """Run a query on the character database and return the first of the results"""
        all_rows = self.fetchall_from_db_query(query)
        return all_rows[0]

    def update(self, update_string):
        """Run and commit a query on the character database"""
        connection = self.db_connection()
        my_cursor = connection.cursor()
        my_cursor.execute(update_string)
        my_cursor.close()
        connection.commit()

"""
#mysql isn't supported yet.
class mysql_database:
    def __init__(self):
        pass
"""