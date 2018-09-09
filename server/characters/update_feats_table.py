import pdb
from . import characters_common
import psycopg2
import configparser
from . import feats

global config


""" The primary routine of this script. This routine pulls the
text from which ever document CXDocs is configured to point to
to read feats from (see config/cxDocs.cfg) and then parses that
plaintext page. The routine then checks the feats psql database
that the CXDocs character creator is configured to read from and
compares the differences. It then prompts the user of this script
to make changes to the psql database to keep it up to date."""
def update_feats():
    connection = characters_common.db_connection()
    cursor = connection.cursor()
    if not config.has_option('Parser', 'feats_filepath'):
        print("../cxDocs.cfg doesn't have the [Parser] feats_filepath doc configuration set.")
        return 0
    feat_filepath = config.get('Parser', 'feats_filepath')
    doc_feats = ingest_feats_doc(feat_filepath)
    psql_feats = feats.get_feats()
    psql_feat_map = {}
    for feat in psql_feats:
        psql_feat_map[feat['feat']] = feat
    doc_feat_map = {}
    for feat in doc_feats:
        doc_feat_map[feat['feat']] = feat
        if feat['feat'] not in list(psql_feat_map.keys()):
            add_feat(feat)
        elif diff_feat(feat, psql_feat_map[feat['feat']]):
            #if there is a matching feat in the database, but it's different
            update_a_feat(feat, psql_feat_map[feat['feat']])
    print("All done!")
    pdb.set_trace()




""" read the feats from the plain text file. 
Expected feat_filepath to be an absolute filepath to the Compound_X
feats document. """
def ingest_feats_doc(feat_filepath):
    feats = []
    lines = []
    #by looping over the doc once first, we get the ability to backtrack up the line list
    with open(feat_filepath, 'r') as feat_file:
        for line in feat_file:
            lines.append(line)

    #split up the feats doc into discrete feats
    index_of_last_title = 0
    index = -1
    for line in lines:
        index = index + 1
        #if the parser has found the start of the next feat
        if line.strip() == "==============================":
            pass
        elif (line[:2] == "==" and line.strip()[-2:]) or index == len(lines):
            new_feat = parse_a_feat(lines[index_of_last_title:index-1])
            feats.append(new_feat)
            index_of_last_title = index
    print("Collected doc feats")
    for feat in feats:
        print("%s\t%s\t%s" % (feat['feat'], feat['nanite_cost'], feat['prerequisites']))

    return feats

def parse_a_feat(lines):
    this_feat = {}
    #find and parse title and nanite cost
    try:
        start_index = lines[0].index('[')
        end_index = lines[0].index('Nanites]')
        nanite_cost = lines[0][start_index + 1:end_index].strip()
        this_feat['nanite_cost'] = nanite_cost
        title = lines[0][2:start_index].strip()
        this_feat['feat'] = title
    except:
        this_feat['nanite_cost'] = 0
        this_feat['feat'] = lines[0].strip()[2:-2]
    #find and parse prerequisites
    end_of_prereqs = 0
    prereq_flag = False
    this_feat['prerequisites'] = []
    index = -1
    for line in lines:
        index = index + 1
        if prereq_flag and len(line.strip()) > 0 and line.strip()[0] != '*':
               prereq_flag = False
               end_of_prereqs = index
        elif prereq_flag and len(line.strip()) > 0 and line.strip()[0] == '*':
            this_feat['prerequisites'].append(line[1:].strip())
        if line.strip() == "Prerequisites:":
            prereq_flag = True
    #find and parse description
    this_feat['description'] = ""
    for line in lines[end_of_prereqs:]:
        this_feat['description'] = "%s %s" % (this_feat['description'], line)

    return this_feat

""" Expects feat to be a map with the keys
* title
* description
* prerequisites
* nanite cost
Also expects that the global config file has the section 'Characters'
with the configs 'characters_psql_pass' and 'characters_psql_user'
options set. 
uses psycopg2 to insert a new feat into the database """
def add_feat(feat):
    print('\n\n\n')
    print("\033[94m" + "This feat isn't currently in the database." + '\033[0m')
    print("Title: %s" % feat['feat'])
    print("Nanite Cost: %s" % feat['nanite_cost'])
    print("Prerequisites: %s " % str(feat['prerequisites']))
    print("Description: %s" % feat['description'])
    print("")
    answer = yes_or_no("Should we add it? (y/n)")
    if answer:
        title = feat['feat'].replace("'", "%39")
        description = feat['description'].replace("'","%39")
        prereqs = str(feat['prerequisites']).replace("'",'"')
        prereqs = prereqs.replace(',', '\\54')
        featstring = "('%s', '%s', '%s', 'feat_parser', now(), '%s', 'f')" % \
        (title, description, feat['nanite_cost'], \
            prereqs)
        connection = characters_common.db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO feats (feat, description, nanite_cost, \
            author, created_at, prerequisites, private) \
            VALUES %s;" % featstring)
        cursor.close()
        connection.commit()

""" prompt to change a feat in the database to match what's on the page """
def update_a_feat(doc_feat, psql_feat):
    print('\n\n\n')
    print('\033[94mThe feat "%s" is different in the database than it is on paper.\033[0m' % doc_feat['feat'])
    print('')
    print("\033[91m(old) Database feat:\033[0m")
    print("%s" % psql_feat['feat'])
    print("Nanite Cost: %s" % psql_feat['nanite_cost'])
    print("Prerequisites:")
    print(psql_feat['prerequisites'])
    print(psql_feat['description'])
    print('')
    print("\033[92m(new) Docs feat:\033[0m")
    print("%s" % doc_feat['feat'])
    print("Nanite Cost: %s" % doc_feat['nanite_cost'])
    print("Prerequisites:")
    print(doc_feat['prerequisites'])
    print(doc_feat['description'])
    print('')
    answer =  yes_or_no('Would you like to update to the new feat? (y/n)')
    if answer:
        doc_feat['pk_id'] = psql_feat['pk_id']
        doc_feat['created_at'] = psql_feat['created_at']
        doc_feat['private'] = psql_feat['private']
        doc_feat['author'] = "feat_parser"
        feats.update_feat(doc_feat)


""" Expects feat_1 and feat_2 to be maps representing feats in the
psql database for CXDocs. Each map should have the following keys:
* title
* description
* nanite cost
* prerequisites
Returns False if the two feats have the same title, prerequisites,
nanite cost and description. 
Returns True otherwise. 
Raises exceptions if the feats passed do not match the standard format."""
def diff_feat(feat_1, feat_2):
    if "feat" not in list(feat_1.keys()):
        print("Error! feat_1 has no name! Feat: %s" % str(feat_1))
        raise Exception
    if "feat" not in list(feat_2.keys()):
        print("Error! feat_2 has no name! Feat: %s" % str(feat_2))
        raise Exception
    if "description" not in list(feat_1.keys()):
        print("Error! feat_1 has no description! Feat: %s" % feat_1['feat'])
        raise Exception
    pdb.set_trace()
    if "description" not in list(feat_2.keys()):
        print("Error! feat_2 has no description! Feat: %s" % feat_2['feat'])
    if feat_1['feat'].strip() != feat_2['feat'].strip():
        return True 
    if feat_1['description'].strip() != feat_2['description'].strip():
        return True
    if sorted(feat_1['prerequisites']) != sorted(feat_2['prerequisites']):
        return True
    if str(feat_1['nanite_cost']).strip() != str(feat_2['nanite_cost']).strip():
        return True
    return False


""" Expects the prompt to be a string containing a 
yes or no question to ask the user of the script. 
Prompts the user with the yes or no question until 
the user replies with either y or n. then returns 
True if the user replied y, returns False if the user
replied n."""
def yes_or_no(prompt):
    answer = input(prompt)
    if answer.strip() == 'y':
        return True
    elif answer.strip() == 'n':
        return False
    else:
        yes_or_no(prompt)

""" This is the main method; this script is intended
to be run from the command line and uses shell input
to decide what to do and to complete running. This
script can not be run by the CX Flask application. """
if __name__ == "__main__":
    global config
    config = configparser.RawConfigParser()
    config.read('../config/cxDocs.cfg')
    characters_common.set_config(config)
    update_feats()