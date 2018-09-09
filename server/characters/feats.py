from . import characters_common
import csv
import pdb
import psycopg2

def get_feats():
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT pk_id, feat, prerequisites, description, author,\
        created_at, private, nanite_cost\
        FROM feats \
        WHERE deleted_at IS NULL;")
    feats = []
    results = myCursor.fetchall()
    for line in results:
        newFeat = parse_line_to_feat(line)
        feats.append(newFeat)
    return feats

def get_feat_by_id(pk_id):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT \
        pk_id, \
        feat, \
        prerequisites,\
        description, \
        author, \
        created_at, \
        private, \
        nanite_cost, \
        FROM feats WHERE pk_id=%s;" % pk_id)
    myCursor.close()
    connection.commit()
    line = myCursor.fetchall[0]
    my_feat = parse_line_to_feat(line)
    return my_feat

def update_feat(newFeat):
    pk_id = newFeat['pk_id']
    prereqs = str(newFeat['prerequisites']).replace("'",'"')

    featstring = "('%s', \
     '%s', '%s', '%s', '%s', '%s', '%s')" % \
     (newFeat['feat'], \
        prereqs, \
        newFeat['description'].replace("'", "\\47"),
        newFeat['author'],
        newFeat['created_at'],
        newFeat['private'],
        newFeat['nanite_cost'])
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE feats SET\
        (feat, \
        prerequisites,\
        description, \
        author, \
        created_at, \
        private, \
        nanite_cost) = %s \
        WHERE pk_id=%s;" % ( featstring,pk_id))
    myCursor.close()
    connection.commit()

def parse_line_to_feat(line):
    feat = {}
    feat['pk_id'] = line[0]
    feat['feat'] = line[1]
    feat['name'] = line[1]
    feat['title'] = line[1]
    if line[2] == "[]":
        feat['prerequisites'] = []
    else:
        prereq_string = line[2][1:-1]
        the_splits = prereq_string.split(',')
        prereqs = []
        for prereq in the_splits:
            trimmed = prereq.strip()[1:-1]
            prereqs.append(trimmed)
        feat['prerequisites'] = prereqs
    feat['description'] = line[3]
    feat['author'] = line[4]
    feat['created_at'] = line[5]
    feat['private'] = line[6]
    feat['nanite_cost'] = line[7]
    return feat

def parse_prereqs(prereq_string):
    prereqs = []
    parser = csv.reader(prereq_string, delimiter=",", quotechar='"')

    return prereqs
  
def get_characters_feats(character_pk_id):
    char_pk_id_int = int(character_pk_id)
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT f.feat, f.prerequisites, f.description, f.author,\
        f.created_at, f.private, f.nanite_cost, f.pk_id\
        FROM feats_map AS map, feats AS f \
        WHERE map.fk_character_id = %s AND map.fk_feat_id = f.pk_id" % char_pk_id_int)
    lines = myCursor.fetchall()
    characters_feats = []
    for line in lines:
        new_feat = parse_line_to_feat(line)
        characters_feats.append(new_feat)
    return characters_feats

def validate_character_feat_map(form):
    expected = set(['character_id', 'feat_id'])
    if expected ^ set(form.keys()) != set([]): #if the form has been tampered with
        return False  #stop trying to parse a tampered form for security reasons.
    character_id = None
    feat_id = None
    try:
        character_id = int(form['character_id'])
        feat_id = int(form['feat_id'])
    except:
        return False #if the ids aren't integers, this isn't a valid mapping
    return {'character_id': character_id, 'feat_id': feat_id}

def insert_character_feat_map(mapping):
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    mapstring = (mapping['character_id'], mapping['feat_id'])
    myCursor.execute("INSERT INTO feats_map (fk_character_id, fk_feat_id) VALUES (%s, %s);" % mapstring)
    myCursor.close()
    connection.commit()
