import ConfigParser
import os
import pdb

if not os.path.exists('config'):
    os.mkdir('config')
config = ConfigParser.RawConfigParser()

config.add_section('Enemies')
config.add_section('Characters')
config.add_section('WhosHere')
config.add_section('Parser')
config.set('Enemies', 'pics_file_path', os.path.abspath('static/images/monsters/bypk_id'))
config.set('Enemies', 'enemies_psql_user', 'searcher')
config.set('Enemies', 'enemies_psql_db', 'mydb')
config.set('Characters', 'characters_psql_user', 'searcher')
config.set('Characters', 'characters_psql_db', 'mydb')
config.set('WhosHere', 'Seconds_away', 60)
config.set('WhosHere', 'Seconds_out', 3600)

print "Please enter the absolute filepath of your copy of the compound x repo, or 'N' if you don't have it: "
response = raw_input("i.e. /blah/blah/Compound_X")
pwd = response.strip()
if pwd != 'N':
	config.set('Parser', 'races_filepath', "%s/01_01_Basic_Rules.txt" % pwd)
	config.set('Parser', 'classes_filepath', "%s/CharacterCreation/02_Classes.txt" % pwd)
	config.set('Parser', 'feats_filepath', "%s/CharacterCreation/03_Feats.txt" % pwd)
	config.set('Parser', 'level_up_filepath', "%s/01_06_Leveling_Up.txt" % pwd)
	config.set('Parser', 'melee_weapons_filepath', "%s/Items/04_01_Melee_&_Thrown_Weapons.txt" % pwd)
	config.set('Parser', 'pistols_filepath', "%s/Items/04_02_Pistols.txt" % pwd)
	config.set('Parser', 'smgs_filepath', "%s/Items/04_03_SMGs_&_Shotguns.txt" % pwd)
	config.set('Parser', 'carbines_filepath', "%s/Items/04_04_Carbines_AssaultRifles_&_BattleRifles.txt" % pwd)
	config.set('Parser', 'long_rifles_filepath', "%s/Items/04_05_Long_Rifles_&_DMRs.txt" % pwd)
	config.set('Parser', 'machineguns_filepath', "%s/Items/04_06_MachineGuns_HeavyWeps_&_RocketLaunchers.txt" % pwd)
	config.set('Parser', 'weapon_attachments_filepath', "%s/Items/04_00_WeaponAttachments.txt" % pwd)
	config.set('Parser', 'armor_filepath', "%s/Items/05_Armors.txt" % pwd)
	config.set('Parser', 'skills_filepath', "%s/CharacterCreation/06_Skills.txt" % pwd)
	config.set('Parser', 'items_filepath', "%s/Items/07_Items.txt" % pwd)
	config.set('Parser', 'basic_rules_filepath', "%s/01_01_Basic_Rules.txt" % pwd)
	config.set('Parser', 'combat_rules_filepath', "%s/01_02_Combat_Rules.txt" % pwd)
	config.set('Parser', 'conditions_filepath', "%s/01_05_Conditions.txt" % pwd)
	config.set('Parser', 'glossary_filepath', "%s/03_Glossary_of_Terms.txt" % pwd)
	config.set('Parser', 'cloaking_filepath', "%s/01_07_Cloaking_Rules.txt" % pwd)
	config.set('Parser', 'new_player_walkthrough_filepath', "%s/00_New_Player_Walkthrough.txt" % pwd)
	config.set('Parser', 'Engineer_filepath', "%s/CharacterCreation/Class-Specific Documentation/Engineer Processes.txt" % pwd)

"""races_filepath: /home/bleehu/1_compound_x/Compound_X/01_01_Basic_Rules.txt
classes_filepath: /home/bleehu/1_compound_x/Compound_X/CharacterCreation/02_Classes.txt
feats_filepath: /home/bleehu/1_compound_x/Compound_X/CharacterCreation/03_Feats.txt
level_up_filepath: /home/bleehu/1_compound_x/Compound_X/01_06_Leveling_Up.txt
melee_weapons_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_01_Melee_&_Thrown_Weapons.txt
pistols_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_02_Pistols.txt
smgs_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_03_SMGs_&_Shotguns.txt
carbines_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_04_Carbines_AssaultRifles_&_BattleRifles.txt
long_rifles_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_05_Long_Rifles_&_DMRs.txt
machineguns_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_06_MachineGuns_HeavyWeps_&_RocketLaunchers.txt
#explosives_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_01_Melee_&_Thrown_Weapons.txt
weapon_attachments_filepath: /home/bleehu/1_compound_x/Compound_X/Items/04_00_WeaponAttachments.txt
armor_filepath: /home/bleehu/1_compound_x/Compound_X/Items/05_Armors.txt
skills_filepath: /home/bleehu/1_compound_x/Compound_X/CharacterCreation/06_Skills.txt
items_filepath: /home/bleehu/1_compound_x/Compound_X/Items/07_Items.txt
basic_rules_filepath: /home/bleehu/1_compound_x/Compound_X/01_01_Basic_Rules.txt
combat_rules_filepath: /home/bleehu/1_compound_x/Compound_X/01_02_Combat_Rules.txt
conditions_filepath: /home/bleehu/1_compound_x/Compound_X/01_05_Conditions.txt
glossary_filepath: /home/bleehu/1_compound_x/Compound_X/03_Glossary_of_Terms.txt
cloaking_filepath: /home/bleehu/1_compound_x/Compound_X/01_07_Cloaking_Rules.txt
new_player_walkthrough_filepath: /home/bleehu/1_compound_x/Compound_X/00_New_Player_Walkthrough.txt
Engineer_filepath: /home/bleehu/1_compound_x/Compound_X/CharacterCreation/Class-Specific Documentation/Engineer Processes.txt"""


with open('config/cxDocs.cfg', 'wb') as configfile:
    config.write(configfile)