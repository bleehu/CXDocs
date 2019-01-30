global config

def initialize_nav(newconfig):
    global config
    config = newconfig

# Reads the config document to build a list of endpoints linked to document filepaths and labels for UI
# Returns a dictionary with endpoints as keys, unless no documents are found, then returns None
def get_rules_docs():
    rulesDocs = {}

    if config.has_option('Parser', 'basic_rules_filepath'):
        rulesDocs['/rules/overview'] = {
            'cfgOptionForFilePath': 'basic_rules_filepath',
            'label': "Overview"
        }

    if config.has_option('Parser', 'combat_rules_filepath'):
        rulesDocs['/rules/combat'] = {
            'cfgOptionForFilePath': 'combat_rules_filepath',
            'label': "Combat"
        }

    if config.has_option('Parser', 'conditions_filepath'):
        rulesDocs['/rules/conditions'] = {
            'cfgOptionForFilePath': 'conditions_filepath',
            'label': "Ailments"
        }

    if config.has_option('Parser', 'level_up_filepath'):
        rulesDocs['/rules/levelup'] = {
            'cfgOptionForFilePath': 'level_up_filepath',
            'label': "Leveling Up"
        }

    if config.has_option('Parser', 'cloaking_filepath'):
        rulesDocs['/rules/cloaking'] = {
            'cfgOptionForFilePath': 'cloaking_filepath',
            'label': "Cloaking"
        }

    if config.has_option('Parser', 'glossary_filepath'):
        rulesDocs['/rules/glossary'] = {
            'cfgOptionForFilePath': 'glossary_filepath',
            'label': "Glossary"
        }

    if len(rulesDocs) < 1:
        log.warn("Looked for Rules documents, but didn't find any. See config/README.md to configure rules docs.")
        return None

    return rulesDocs

# Reads the config document to build a list of endpoints linked to document filepaths and labels for UI
# Returns a dictionary with endpoints as keys, unless no documents are found, then returns None
def get_item_docs():
    itemDocs = {}

    if config.has_option('Parser', 'melee_weapons_filepath'):
        itemDocs['/items/meleeWeapons'] = {
            'cfgOptionForFilePath': 'melee_weapons_filepath',
            'label': "Melee Weapons"
        }

    if config.has_option('Parser', 'pistols_filepath'):
        itemDocs['/items/pistols'] = {
            'cfgOptionForFilePath': 'pistols_filepath',
            'label': "Pistols"
        }

    if config.has_option('Parser', 'smgs_filepath'):
        itemDocs['/items/smgs'] = {
            'cfgOptionForFilePath': 'smgs_filepath',
            'label': "SMGs"
        }

    if config.has_option('Parser', 'carbines_filepath'):
        itemDocs['/items/carbines'] = {
            'cfgOptionForFilePath': 'carbines_filepath',
            'label': "Carbines"
        }

    if config.has_option('Parser', 'long_rifles_filepath'):
        itemDocs['/items/longRifles'] = {
            'cfgOptionForFilePath': 'long_rifles_filepath',
            'label': "Long Rifles"
        }

    if config.has_option('Parser', 'machineguns_filepath'):
        itemDocs['/items/machineguns'] = {
            'cfgOptionForFilePath': 'machineguns_filepath',
            'label': "Heavy Guns"
        }

    if config.has_option('Parser', 'weapon_attachments_filepath'):
        itemDocs['/items/weaponAttachments'] = {
            'cfgOptionForFilePath': 'weapon_attachments_filepath',
            'label': "Weapon Attachments"
        }

    if config.has_option('Parser', 'armor_filepath'):
        itemDocs['/items/armor'] = {
            'cfgOptionForFilePath': 'armor_filepath',
            'label': "Armor"
        }

    if config.has_option('Parser', 'items_filepath'):
        itemDocs['/items/misc'] = {
            'cfgOptionForFilePath': 'items_filepath',
            'label': "Misc"
        }

    if len(itemDocs) < 1:
        log.warn("Looked for Item documents, but didn't find any. See config/README.md to configure rules docs.")
        return None

    return itemDocs

# Reads the config document to build a list of endpoints linked to document filepaths and labels for UI
# Returns a dictionary with endpoints as keys, unless no documents are found, then returns None
def get_character_docs():
    characterDocs = {}

    if config.has_option('Parser', 'new_player_walkthrough_filepath'):
        characterDocs['/newplayer'] = {
            'cfgOptionForFilePath': 'new_player_walkthrough_filepath',
            'label': "New Players",
            'navList': (
                '/rules/overview',
                '/races',
                '/classes',
                '/files'
            )
        }

    if config.has_option('Parser', 'races_filepath'):
        characterDocs['/races'] = {
            'cfgOptionForFilePath': 'races_filepath',
            'label': "Races"
        }

    if config.has_option('Parser', 'classes_filepath'):
        characterDocs['/classes'] = {
            'cfgOptionForFilePath': 'classes_filepath',
            'label': "Classes"
        }

    if config.has_option('Parser', 'feats_filepath'):
        characterDocs['/feats'] = {
            'cfgOptionForFilePath': 'feats_filepath',
            'label': "Feats"
        }

    if config.has_option('Parser', 'skills_filepath'):
        characterDocs['/skills'] = {
            'cfgOptionForFilePath': 'skills_filepath',
            'label': "Skills"
        }

    if config.has_option('Parser', 'engineer_filepath'):
        characterDocs['/rules/engineers'] = {
            'cfgOptionForFilePath': 'engineer_filepath',
            'label': "Engineer Processes"
        }

    if len(characterDocs) < 1:
        log.warn("Looked for Character documents, but didn't find any. See config/README.md to configure rules docs.")
        return None

    return characterDocs

# Generates the allRoutes dictionary using the above functions
def create_routes_dict():
    routesDict = {
        '/': {
            'cfgOptionForFilePath': None,
            'label': "Home",
            'navbar': ( '/newplayer', '/rules/', '/gm/' )
        },
        '/rules/': {
            'cfgOptionForFilePath': None,
            'label': "Rules",
            'navbar': ( '/newplayer', '/gm/' ),
            'navList': (
                '/rules/glossary',
                '/rules/combat',
                '/rules/levelup',
                '/rules/conditions',
                '/rules/cloaking',
                '/rules/engineers'
            )
        },
        '/items/': {
            'cfgOptionForFilePath': None,
            'label': "Items",
            'navbar': ( '/newplayer', '/rules/', '/gm/' )
        },
        '/gm/': {
            'cfgOptionForFilePath': None,
            'label': "For GMs",
            'navbar': ( '/rules/', '/gm/' ),
            'navList': (
                '/gm/designhowto',
                '/gm/monsterweaponshowto',
                '/gm/monsterarmorhowto'
            )
        },
        '/gm/designhowto': {
            'templateToRender': 'creation_manuals/design_how_to.html',
            'label': "Designing Campaigns",
            'navbar': ( '/', ),
            'navList': None
        },
        '/gm/monsterweaponshowto': {
            'templateToRender': 'creation_manuals/monster_weapon_how_to.html',
            'label': "Designing Enemy Weapons",
            'navbar': ( '/', ),
            'navList': None
        },
        '/gm/monsterarmorhowto': {
            'templateToRender': 'creation_manuals/monster_armor_how_to.html',
            'label': "Designing Enemy Armor",
            'navbar': ( '/', ),
            'navList': None
        },
        '/files': {
            'templateToRender': 'utility/game/files.html',
            'label': "Printable Sheets",
            'navbar': ( '/', ),
            'navList': None,
        }

    }

    lengthBeforeDocs = len(routesDict)

    rules_dict = get_rules_docs()
    if rules_dict != None and len(rules_dict) > 0:
        routesDict.update(rules_dict)

    item_dict = get_item_docs()
    if item_dict != None and len(item_dict) > 0:
        routesDict.update(item_dict)

    character_dict = get_character_docs()
    if character_dict != None and len(character_dict) > 0:
        routesDict.update(character_dict)

    if len(routesDict) == lengthBeforeDocs:
        log.warn("Looked for documents, but didn't find any. See config/README.md to configure rules docs.")

    return routesDict

def generate_navbar_options_for_page(navbar, allRoutes):
    navResults = []

    for route in navbar:
        navResults.append( (allRoutes[route]['label'], route) )

    return navResults

def generate_navLists_for_page(navbar, allRoutes):
    listResults = []
    i = 0

    for route in navbar:
        listResults.append([])

        for endpoint in allRoutes[route]['navList']:
            listResults[i].append( (allRoutes[endpoint]['label'], endpoint) )

        i += 1

    return listResults
