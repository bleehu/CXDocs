# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)

_gm_navbar = ('/rules/', '/rules/glossary', '/gm/')
_gm_nav_list = ('/gm/designhowto', '/gm/monsterweaponshowto', '/gm/monsterarmorhowto')

def get_dict():
    return {
        # Paths should match options in the Parser section of the config file
        # Each path key must have a tuple containing values IN THE FOLLOWING ORDER:
            # a label string (this will be seen by users (keep it brief))
            # a route string (this is where the link will take a user to; include full route for now with all slashes)
            # a navbar tuple (NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar)

            # (optional) 4th value: a nav_list tuple, listing the options that would appear under its navbar label (usually to very specific pages)

        '/gm/designhowto': {
            'label': "Designing Campaigns",
            'navbar': _gm_navbar,
            'template_to_render': 'creation_manuals/design_how_to.html',
            'nav_list': _gm_nav_list
        },
        '/gm/monsterweaponshowto': {
            'label': "Designing Enemy Weapons",
            'navbar': _gm_navbar,
            'template_to_render': 'creation_manuals/monster_weapon_how_to.html',
            'nav_list': _gm_nav_list
        },
        '/gm/monsterarmorhowto': {
            'label': "Designing Enemy Armor",
            'navbar': _gm_navbar,
            'template_to_render': 'creation_manuals/monster_armor_how_to.html',
            'nav_list': _gm_nav_list
        },
        '/gm/npcgen': {
            'label': "NPC Generator",
            'navbar': _gm_navbar,
            'template_to_render': 'utility/game/npcgen.html',
            'nav_list': _gm_nav_list
        }
    }
