import ConfigParser
import os
import pdb

if not os.path.exists('config'):
    os.mkdir('config')
config = ConfigParser.RawConfigParser()

config.add_section('Section1')
config.set('Section1', 'pics_file_path', os.path.abspath('static/images/monsters/bypk_id'))

with open('config/cxDocs.cfg', 'wb') as configfile:
    config.write(configfile)