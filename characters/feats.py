import characters_common
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