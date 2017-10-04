import psycopg2
import ConfigParser

global config

def set_config(new_config):
    global config
    config = new_config

def db_connection():
    username = "searcher"
    if config.get('Enemies','enemies_psql_user'):
            username = config.get('Enemies', 'enemies_psql_user')
    db = 'mydb'
    if config.get('Enemies', 'enemies_psql_db'):
        db = config.get('Enemies', 'enemies_psql_db')
    connection = psycopg2.connect("dbname=%s user=%s password=allDatSQL" % (db, username))
    return connection