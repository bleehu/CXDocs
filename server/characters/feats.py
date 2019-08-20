import characters_common
import pdb
import psycopg2

def get_feats():
    """Return a list of feats from the database."""
    query_string = "%s WHERE deleted_at IS NULL;" % Feat.Select_predicate
    results = characters_common.fetchall_from_db_query(query_string)
    feats = []
    for line in results:
        new_feat = Feat(line)
        feats.append(new_feat)
    return feats

def get_feat_by_id(pk_id):
    query_string = "%s WHERE pk_id=%s;" % (Feat.Select_predicate, pk_id)
    first_database_row = characters_common.fetch_first_from_db_query(query_string)
    my_feat = Feat(first_database_row)
    return my_feat

def update_feat(new_feat):
    pk_id = new_feat['pk_id']
    prereqs = str(new_feat['prerequisites']).replace("'",'"')

    featstring = "('%s', \
     '%s', '%s', '%s', '%s', '%s', '%s')" % \
     (new_feat['feat'], \
        prereqs, \
        new_feat['description'].replace("'", "\\47"),
        new_feat['author'],
        new_feat['created_at'],
        new_feat['private'],
        new_feat['nanite_cost'])
    connection = characters_common.db_connection()
    my_cursor = connection.cursor()
    my_cursor.execute("UPDATE feats SET\
        (feat, \
        prerequisites,\
        description, \
        author, \
        created_at, \
        private, \
        nanite_cost) = %s \
        WHERE pk_id=%s;" % ( featstring,pk_id))
    my_cursor.close()
    connection.commit()

def get_characters_feats(character_pk_id):
    char_pk_id_int = int(character_pk_id)
    query_string = "SELECT f.pk_id, f.feat, f.prerequisites, f.description, f.author,\
        f.created_at, f.private, f.nanite_cost\
        FROM feats_map AS map, feats AS f \
        WHERE map.fk_character_id = %s AND map.fk_feat_id = f.pk_id" % char_pk_id_int
    lines = characters_common.fetchall_from_db_query(query_string)
    characters_feats = []
    for line in lines:
        new_feat = Feat(line)
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
    my_cursor = connection.cursor()
    mapstring = (mapping['character_id'], mapping['feat_id'])
    my_cursor.execute("INSERT INTO feats_map (fk_character_id, fk_feat_id) VALUES (%s, %s);" % mapstring)
    my_cursor.close()
    connection.commit()

class Feat:
    """A Character's feat."""

    Select_predicate = "SELECT \
        pk_id, \
        feat, \
        prerequisites,\
        description, \
        author, \
        created_at, \
        private, \
        nanite_cost \
        FROM feats"

    def __init__(self, line):
        self.pk_id = int(line[0])
        self.name = line[1]
        self.title = line[1]
        prereqs = parse_prereq_list(line[2])
        self.prerequisites = prereqs
        self.description = line[3]
        self.author = line[4]
        self.created_at = line[5]
        self.private = line[6]
        self.nanite_cost = int(line[7])


def parse_prereq_list(prereq_string):
    if prereq_string == "[]":
        return []
    the_splits = prereq_string.split(',')
    prereqs = []
    for prereq in the_splits:
        trimmed = prereq.strip()
        prereqs.append(trimmed)
    return prereqs

