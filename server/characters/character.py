import character_database
from ..security import security
import pdb

class CXCharacter:

    def __init__(self, form, owner_id):
        self.name = security.sql_escape(form['name'])
        self.description = security.sql_escape(form['description'])
        self.primaryStats = {}
        self.primaryStats['Strength'] = int(form['strength'])
        self.primaryStats['Perception'] = int(form['perception'])
        self.primaryStats['Dexterity'] =int(form['dexterity'])
        self.primaryStats['Fortitude'] = int(form['fortitude'])
        self.primaryStats['Charisma'] = int(form['charisma'])
        self.primaryStats['Intelligence'] = int(form['intelligence'])
        self.primaryStats['Luck'] = int(form['luck'])
        self.saves = {}
        self.saves['Reflex'] = int(form['reflex'])
        self.saves['Shock'] = int(form['shock'])
        self.saves['Will'] = int(form['will'])
        self.saves['Awareness'] = int(form['awareness'])
        self.maxHealth = int(form['maxHealth'])
        self.maxNanites = int(form['maxNanites'])
        self.level = int(form['level'])
        self.species = security.sql_escape(form['species'])
        self.subSpecies = None #coming soon?
        self.background = None #coming soon?
        self.skills = [] #Coming soon
        self.inventory = [] #coming eventually
        self.cxClass = security.sql_escape(form['classname'])
        self.secondaryStats = {}
        self.secondaryStats['Carry Ability'] = int(form['carry_ability'])
        self.secondaryStats['Move Speed'] = int(form['move_speed'])
        self.secondaryStats['Skill Gain'] = int(form['skill_gain'])
        self.pk_id = int(form['pk_id'])
        self.owner_id = int(owner_id) 

    def __init__(self, db_tuple):
        self.name = db_tuple[0]
        self.maxHealth = int(db_tuple[1])
        self.maxNanites = int(db_tuple[2])
        self.primaryStats = {}
        self.primaryStats['Strength'] = int(db_tuple[3])
        self.primaryStats['Perception'] = int(db_tuple[4])
        self.primaryStats['Fortitude'] = int(db_tuple[5])
        self.primaryStats['Charisma'] = int(db_tuple[6])
        self.primaryStats['Intelligence'] = int(db_tuple[7])
        self.primaryStats['Dexterity'] = int(db_tuple[8])
        self.primaryStats['Luck'] = int(db_tuple[9])
        self.level = int(db_tuple[10])
        self.saves = {}
        self.saves['Shock'] = int(db_tuple[11])
        self.saves['Will'] = int(db_tuple[12])
        self.saves['Reflex'] = int(db_tuple[13])
        self.saves['Awareness'] = int(db_tuple[14])
        self.description = db_tuple[15]
        self.species = db_tuple[16]
        self.cxClass = db_tuple[17]
        self.owner_id = int(db_tuple[18])
        self.money = int(db_tuple[19])
        self.created_at = db_tuple[20]
        self.pk_id = int(db_tuple[21])
        self.secondaryStats = {}
        self.secondaryStats['Carry Ability'] = int(db_tuple[22])
        self.secondaryStats['Move Speed'] = int(db_tuple[23])
        self.secondaryStats['Skill Gain'] = int(db_tuple[24])

    def db_string():
        insert_string = "(name, health, nanites, \
            strength,\
            perception,\
            fortitude,\
            charisma, \
            intelligence, \
            dexterity, \
            luck, \
            level, \
            shock, will, reflex, awareness,\
            description, \
            species, \
            class, \
            fk_owner_id,\
            money, \
            created_at, \
            pk_id, \
            carry_ability, \
            move_speed, \
            skill_gain)"
        return insert_string

    def level_up():
        self.level = self.level + 1
        return self.level
    
    """ user is the pk_id of the user """
    def valid(self):
        if self.name.strip() == '' or len(self.name) > 400:
            return False
        if self.description.strip() == '' or len(self.description) > 10000:
            return False
        if maxHealth < 0 or maxHealth > 2000:
            return False
        if maxNanites < 0 or  maxNanites > 2000:
            return False
        for stat in primaryStats:
            if self.primaryStats[stat] < 1:
                return False
            if self.primaryStats[stat] > 40:
                return False
        for stat in secondaryStats:
            if self.secondaryStats[stat] < -80:
                return False
            if self.secondaryStats[stat] > 80:
                return False
        if level < 0 or level > 100:
            return False    
        return True

    def tuple(self):
        return self.__repr__()

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        #ending a line with a backslash keeps the command from running off the screen
        characterTuple = (self.name, \
        self.maxHealth, \
        self.maxNanites, \
        self.primaryStats['Strength'], \
        self.primaryStats['Perception'], \
        self.primaryStats['Dexterity'], \
        self.primaryStats['Fortitude'], \
        self.primaryStats['Charisma'], \
        self.primaryStats['Intelligence'], \
        self.primaryStats['Luck'], \
        self.saves['Reflex'], \
        self.saves['Will'], \
        self.saves['Shock'], \
        self.level, \
        self.cxClass, \
        self.species, \
        self.description, \
        self.money, \
        self.owner_id,\
        self.secondaryStats['Carry Ability'],\
        self.secondaryStats['Move Speed'],\
        self.secondaryStats['Skill Gain'])
        return characterTuple