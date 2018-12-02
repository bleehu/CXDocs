import psycopg2
import ConfigParser
import os
global config

def set_config(new_config):
    global config
    config = new_config

def db_connection():
    username = "searcher"
    if config.has_option('Enemies','enemies_psql_user'):
            username = config.get('Enemies', 'enemies_psql_user')
    db = 'mydb'
    if config.has_option('Enemies', 'enemies_psql_db'):
        db = config.get('Enemies', 'enemies_psql_db')
    token = 'allDatSQL'
    if config.has_option('Enemies', 'enemies_psql_pass'):
        token = config.get('Enemies', 'enemies_psql_pass')
    connection = psycopg2.connect("dbname=%s user=%s password=%s host=localhost" % (db, username, token))
    return connection

def check_has_pic(pk_id):
    filepath = "%s/%s.png" % (config.get('Enemies', 'pics_file_path'), pk_id)
    return os.path.exists(filepath)