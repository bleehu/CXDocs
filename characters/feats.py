import characters_common
import psycopg2

def get_feats():
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT feat, prerequisites, description, author,\
        created_at, private, nanite_cost, pk_id\
        FROM feats \
        WHERE deleted_at IS NULL;")
    feats = []
    results = myCursor.fetchall()
    for line in results:
        newFeat = parse_line_to_feat(line)
        feats.append(newFeat)
    return feats

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


def parse_line_to_feat(line):
    feat = {}
    feat['feat'] = line[0]
    feat['name'] = line[0]
    feat['title'] = line[0]
    feat['prerequisites'] = line[1]
    feat['description'] = line[2]
    feat['author'] = line[3]
    feat['created_at'] = line[4]
    feat['private'] = line[5]
    feat['nanite_cost'] = line[6]
    feat['pk_id'] = line[7]
    return feat