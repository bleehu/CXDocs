import character_database
from ..security import security
import pdb

class cx_character:

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
        self.name = line[0]
        self.maxHealth = int(line[1])
        self.maxNanites = int(line[2])
        self.primaryStats = {}
        self.primaryStats['Strength'] = int(line[3])
        self.primaryStats['Perception'] = int(line[4])
        self.primaryStats['Fortitude'] = int(line[5])
        self.primaryStats['Charisma'] = int(line[6])
        self.primaryStats['Intelligence'] = int(line[7])
        self.primaryStats['Dexterity'] = int(line[8])
        self.primaryStats['Luck'] = int(line[9])
        self.level = int(line[10])
        self.saves = {}
        self.saves['Shock'] = int(line[11])
        self.saves['Will'] = int(line[12])
        self.saves['Reflex'] = int(line[13])
        self.saves['Awareness'] = int(line[14])
        self.description = line[15]
        self.species = line[16]
        self.cxClass = line[17]
        self.owner_id = int(line[18])
        self.money = int(line[19])
        self.created_at = line[20]
        self.pk_id = int(line[21])
        self.secondaryStats = {}
        self.secondaryStats['Carry Ability'] = int(line[22])
        self.secondaryStats['Move Speed'] = int(line[23])
        self.secondaryStats['Skill Gain'] = int(line[24])
        return newCharacter

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