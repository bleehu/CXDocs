# Config Files

Put helpful configurations here. To generate a new config file, run the python 
2.7 script called "generate_config.py" in the main directory. The command to run
the script should just be `$python generate_config.py`. Some command-line input
will be required.

## Auth Section

The essentials of the auth section should be completely filled out by the 
gen_config.py script. If not, you can set it manually. See below for an example. 
The auth section should point to the SQL server that has the usernames and 
passwords set up. PostgreSQL is free and works fine if you'd like to build one 
yourself. *Make sure not to commit any passwords or secrets in code!*

```
[Auth]
db_name = mydb
port = 5432
host = localhost
```

max_tries: an integer positing how many tries someone can get wrong in max_tries_minutes before the app locks them out.

max_tries_minutes: an integer establishing how many minutes that someone will have max_tries to sign in with the correct username and password before the app locks them out.

The default is 3 tries in 30 minutes.

## Enemies Section

enemies_psql_db: The name of the database that contains the data about enemies for the bestiary. Default is mydb.

enemies_psql_user: The user that the application uses to get/update the enemy database. Default is searcher.

enemies_psql_pass: The password for the user that inspects the enemies in your database.

pics_file_path: the file path in which to store pictures uploaded to the server of monsters.

## Parser Section

races_filepath: (optional) absolute filepath to the 01_Races.txt plaintext document from the compound_x repo

classes_filepath: (optional)  absolute filepath to the 02_Classes.txt plaintext document from the compound_x repo

feats_filepath: (optional) absolute filepath to the 03_Feats.txt plaintext document from the compound_x repo

level_up_filepath: (optional) absolute filepath to the 01_06_leveling_up.txt plaintext rules document from the compound_x repo

melee_weapons_filepath: (optional) absolute filepath to the 04_01_Melee_et_Thrown_Weapons.txt document from the compound_x repo

pistols_filepath: (optional) absolute filepath to the 04_02_Pistols.txt document from the compound_x repo

smgs_filepath: (optional) absolute filepath to the 04_03_SMGs_et_Shotguns.txt document from the compound_x repo

carbines_filepath: (optional) absolute filepath to the 04_04_Carbines_AssaultRifles_et_BattleRifles.txt document from the compound_x repo

long_rifles_filepath: (optional) absolute filepath to the 04_05_Long_Rifles_et_DMRs.txt document from the compound_x repo

machineguns_filepath: (optional) absolute filepath to the 04_06_MachineGuns_HeavyWeps_et_RocketLaunchers.txt document from the compound_x repo

explosives_filepath: (optional) the absolute (full) filepath to the explosives document. This document should conform to the plaintext standards outlined in the CX design team's design repo.

weapon_attachments_filepath: (optional) absolute filepath to the 04_00_WeaponAttachments.txt plaintext document from the compound_x repo

armor_filepath: (optional) absolute filepath to the 05_ArmourList.txt plaintext document from the compound_x repo

skills_filepath: (optional) absolute filepath to the 06_Skills.txt plaintext document from the compound_x repo

items_filepath: (optional) absolute filepath to the 07_Items.txt plaintext document from the compound_x repo

basic_rules_filepath: (optional) absolute filepath to the Basic Rules.txt plaintext document from the compound_x repo

combat_rules_filepath: (optional) absolute filepath to the 01_02_Combat_Rules.txt plaintext document in teh compound_x repo

conditions_filepath: (optional) absolute filepath to the conditions 01_05_Conditions.txt plaintext file

glossary_filepath: (optional) absolute filepath to the 03_Glossary_of_Terms.txt file

cloaking_filepath: (option) absolute filepath to the cloaking rules file

new_player_walkthrough_filepath: (optional) absolute filepath to the new player walkthrough rule page

engineer_filepath: (optional) absolute filepath to the Engineer Processes.txt plaintext document from the compound_x repo

medic_filepath: (optional) absolute filepath to the Medic Procedures.txt plaintext document from the compound_x repo



## WhosHere Section

seconds_away: Don't forget to capitalize the S! This is how many seconds the 'Who's Here' feature should wait before marking someone as being 'away'

seconds_out: The number of seconds before the Who's Here function should forget someone had logged in.
