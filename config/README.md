#Config Files
Put helpful configurations here. To generate a new config file, run the python 2.7 script called "generate_config.py" in the main directory.

##Enemies Section
enemies_psql_db: The name of the database that contains the data about enemies for the bestiary. Default is mydb.
enemies_psql_user: The user that the application uses to get/update the enemy database. Default is searcher.
pics_file_path: the file path in which to store pictures uploaded to the server of monsters.

##Parser Section
races_filepath: (optional) absolute filepath to the 01_Races.txt plaintext document from the compound_x repo
classes_filepath: (optional)  absolute filepath to the 02_Classes.txt plaintext document from the compound_x repo
feats_filepath: (optional) absolute filepath to the 03_Feats.txt plaintext document from the compound_x repo
weapon_attachments_filepath: (optional) absolute filepath to the 04_00_WeaponAttachments.txt plaintext document from the compound_x repo
armor_filepath: (optional) absolute filepath to the 05_ArmourList.txt plaintext document from the compound_x repo
skills_filepath: (optional) absolute filepath to the 06_Skills.txt plaintext document from the compound_x repo
items_filepath: (optional) absolute filepath to the 07_Items.txt plaintext document from the compound_x repo
basic_rules_filepath: (optional) absolute filepath to the Basic Rules.txt plaintext document from the compound_x repo
Engineer_filepath: (optional) absolute filepath to the Engineer Processes.txt plaintext document from the compound_x repo
Medic_filepath: (optional) absolute filepath to the Medic Proceedures.txt plaintext document from the compound_x repo