import characters_common
import psycopg2

def get_characters_skills(character_pk_id):
    char_pk_id_int = int(character_pk_id)
    connection = characters_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("SELECT skillname, points, pk_id FROM skills WHERE fk_owner_id = %s;" % char_pk_id_int)
    lines = myCursor.fetchall()
    characters_skills = []
    for line in lines:
        new_skill = parse_line_to_skill(line)
        characters_skills.append(new_skill)
    return characters_skills

def parse_line_to_skill(line):
    skill = {}
    skill['skill'] = line[0]
    skill['name'] = line[0]
    skill['points'] = line[1]
    skill['pk_id'] = line[2]
    return skill