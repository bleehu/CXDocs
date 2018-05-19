import psycopg2
import ConfigParser

global config

def set_config(new_config):
    global config
    config = new_config

def db_connection():
    username = "searcher"
    if config.has_option('Characters','characters_psql_user'):
            username = config.get('Characters', 'characters_psql_user')
    db = 'mydb'
    if config.has_option('Characters', 'characters_psql_db'):
        db = config.get('Characters', 'characters_psql_db')
    db_pass = "allDatSQL"
    if config.has_option('Characters','characters_psql_pass'):
        db_pass = config.get('Characters','characters_psql_pass')
    connection = psycopg2.connect("dbname=%s user=%s password=%s" % (db, username,db_pass))
    return connection