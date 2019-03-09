from ..database import database
import character
from ..cxExceptions import cxExceptions

"""This Module contains methods used by many of the character code files. It is
    not intended for standalone use.
    """

class character_database(database.cx_database):

    def __init__(self, config):
        config_map = {"port":5432, 
            "db_host":"localhost", 
            "db_name":"mydb"}
        if config.has_section('Characters'):
            for option in config.options('Characters'):
                config_map[option] = config.get('Characters', option)
        else:
            raise cxExceptions.ConfigOptionMissingException("Characters config section")
        if not config.has_option('Characters', 'username') or not config.has_option('Characters', 'password'):
            raise cxExceptions.ConfigOptionMissingException("Characters database username and password")
        self.my_db = database.cx_database(config_map)

    def get_characters(self):
        queryString = "SELECT name, health, nanites, \
            strength, perception, fortitude, charisma, intelligence, dexterity,\
            luck, level, shock, will, reflex, description, race, class, fk_owner_id, \
            money, created_at, pk_id, carry_ability, move_speed, skill_gain\
            FROM characters \
            WHERE deleted_at IS NULL ORDER BY level;"
        characters = []
        results = self.my_db.fetch_all(queryString)
        for line in results:
            newCharacter = character.cx_character(line)
            characters.append(newCharacter)
        return characters

    """ Owner should be the pk_id of the user who generated the character in integer form. 
    This method mostly used in the copy character route; in which case the character
    should be the map of the character, such as the output from parse_character_line() """
    def insert_character(self, character):
        queryString = "INSERT INTO characters \
            SET (name, health, nanites, strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
            reflex, will, shock, level, class, race, description, money, fk_owner_id) \
            = (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', E'%s', %s, '%s');" \
            % character.tuple()
        self.my_db.insert(queryString)

    def create_blank_character(self, owner_pk_id):
        insertString = "INSERT INTO characters (name, health, nanites, \
            strength, perception, dexterity, fortitude, charisma, intelligence, luck, \
            reflex, will, shock, level, class, race, description, money, fk_owner_id, \
            carry_ability, move_speed, skill_gain) \
            VALUES ('New Character', 100, 100, 6, 6, 6, 6, 6, 6, 6, 12, 12, 12, 1, \
            'Soldier', 'Human', '', 0, '%s', 6, 6, 6);" % int(owner_pk_id)
        self.my_db.update(insertString)
        return self.get_users_newest_character(owner_pk_id)

    """Get a character by searching for it's primary key id. This should return a
    character regardless of whether it's been soft-deleted or not; we use this method
    to report on which character we just deleted as well. If no character matches
    this pk_id, returns none. """
    def get_character_by_id(self, pk_id):
        sani_pk_id = int(pk_id)
        queryString = "SELECT name, health, nanites, \
            strength, perception, fortitude, charisma, intelligence, dexterity,\
            luck, level, shock, will, reflex, awareness, description, race, class, fk_owner_id, \
            money, created_at, pk_id, carry_ability, move_speed, skill_gain\
            FROM characters \
            WHERE pk_id = %s;" % pk_id
        db_tuple = self.my_db.fetch_first(queryString)
        this_character = character.cx_character(db_tuple)
        return this_character

    def get_users_characters(self, user_pk_id):
        user_id = int(user_pk_id)
        these_characters = []
        queryString = "SELECT c.name, c.health, c.nanites, \
            c.strength, c.perception, c.fortitude, c.charisma, c.intelligence, \
            c.dexterity, c.luck, c.level, c.shock, c.will, c.reflex, c.awareness, c.description, \
            c.race, c.class, c.fk_owner_id, c.money, c.created_at, c.pk_id, \
            c.carry_ability, c.move_speed, c.skill_gain\
            FROM characters AS c WHERE c.fk_owner_id = %s;" % user_id
        lines = self.my_db.fetch_all(queryString)
        for line in lines:
            these_characters.append(character.cx_character(line))
        return these_characters

    def get_users_newest_character(self, user_pk_id):
        queryString = "SELECT c.pk_id FROM characters AS c, users AS u \
            WHERE u.pk_id = %s AND c.fk_owner_id = u.pk_id \
            ORDER BY c.pk_id DESC;" % int(user_pk_id)
        all_pk_ids = self.my_db.fetch_all(queryString)
        new_pk_id = all_pk_ids[0][0]
        new_character = self.get_character_by_id(new_pk_id)
        return new_character

    def update_character(self, character):
        if character.valid():
            pk_id = character.pk_id
            flat_tuple = character.db_string() + character.tuple() + pk_id
            updateString = "UPDATE characters\
                SET % =\
                (E'%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, E'%s', E'%s', E'%s', %s, %s, %s, %s)\
                WHERE pk_id=%s;" \
                % flat_tuple
            self.my_db.update(updateString)
        else:
            raise cxException()

    """ Add a delete timestamp to the deleted_at  column of the character postgres table.  
    pk_id is assumed to have been sanitized in the route (character_routes.py) and the 
    user permissions are assumed to have been checked there too."""
    def delete_character(self, pk_id):
        updateQuery = "UPDATE characters SET deleted_at=now() WHERE pk_id=%s;" % pk_id
        self.my_db.update(updateQuery)