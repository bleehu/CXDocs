import psycopg2
import ConfigParser

global config

"""this file contains methods used by many of the character code files. It is not intended for
    standalone use. """

""" This method sets the configuration for database connections. It should be called during the 
    initialization of whatever program is using it. For more on cxdocs configs, see repo/config/README.md

    new_config: the ConfigParser config object to send logs to.  """
def set_config(new_config):
    global config
    config = new_config

""" returns a psycopg2 database connection to the character postgres database.  """
def db_connection():
    #database username defaults to searcher
    username = "searcher"
    if config.has_option('Characters','characters_psql_user'):
            username = config.get('Characters', 'characters_psql_user')
    #database name defaults to mydb
    db = 'mydb'
    if config.has_option('Characters', 'characters_psql_db'):
        db = config.get('Characters', 'characters_psql_db')
    #this default password has already been changed
    db_pass = "allDatSQL"
    if config.has_option('Characters','characters_psql_pass'):
        db_pass = config.get('Characters','characters_psql_pass')
    connection = psycopg2.connect("dbname=%s user=%s password=%s" % (db, username,db_pass))
    return connection