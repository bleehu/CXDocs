import characters_common
import psycopg2

def get_feats():
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT feat, prerequisites, description, author,\
        created_at, private, nanite_cost\
        FROM feats \
        WHERE deleted_at IS NULL;")
    feats = []
    results = myCursor.fetchall()
    for line in results:
        newFeat = parse_line_to_feat(line)
        feats.append(newFeat)
    return feats


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
    return feat