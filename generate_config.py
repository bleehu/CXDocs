import ConfigParser
import os
import pdb

if not os.path.exists('config'):
    os.mkdir('config')
config = ConfigParser.RawConfigParser()

config.add_section('Enemies')
config.set('Enemies', 'pics_file_path', os.path.abspath('static/images/monsters/bypk_id'))
config.set('Enemies', 'enemies_psql_user', 'searcher')
config.set('Enemies', 'enemies_psql_db', 'mydb')

with open('config/cxDocs.cfg', 'wb') as configfile:
    config.write(configfile)