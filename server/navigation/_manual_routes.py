# Gives the initial piece of the dictionary where we have to manually enter routes and endpoints
def get_manual_routes():
    return {
        # Each dictionary key is a string for a route the user can go to
        # Each key's value is a dictionary for route information:
            # label: <string> Required; name displayed for user navigation
            # navbar: <tuple(<string>)> Required; strings must match routes; NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar
            # filepath_option: <string> The config option used by the parser to get the filepath for the rules to be displayed
            # template_to_render: <string> The template file to use for displaying the route's page
            # nav_list: <tuple(<string>)> A list of routes to be display under the key route's navbar button when displayed (basically subtopics of the route)

        '/': {
            'label': "Home",
            'navbar': ( '/newplayer', '/rules/', '/gm/' ),
            'filepath_option': None
        },
        '/rules/': {
            'label': "Rules",
            'navbar': ( '/newplayer', '/gm/' ),
            'filepath_option': None,
            'nav_list': (
                '/rules/glossary',
                '/rules/combat',
                '/rules/levelup',
                '/rules/conditions',
                '/rules/cloaking',
                '/rules/engineers'
            )
        },
        '/items/': {
            'label': "Items",
            'navbar': ( '/newplayer', '/rules/', '/gm/' ),
            'filepath_option': None
        },
        '/gm/': {
            'label': "For GMs",
            'navbar': ( '/rules/', '/gm/' ),
            'filepath_option': None,
            'nav_list': (
                '/gm/designhowto',
                '/gm/monsterweaponshowto',
                '/gm/monsterarmorhowto'
            )
        },
        '/gm/designhowto': {
            'label': "Designing Campaigns",
            'navbar': ( '/', ),
            'template_to_render': 'creation_manuals/design_how_to.html',
            'nav_list': None
        },
        '/gm/monsterweaponshowto': {
            'label': "Designing Enemy Weapons",
            'navbar': ( '/', ),
            'template_to_render': 'creation_manuals/monster_weapon_how_to.html',
            'nav_list': None
        },
        '/gm/monsterarmorhowto': {
            'label': "Designing Enemy Armor",
            'navbar': ( '/', ),
            'template_to_render': 'creation_manuals/monster_armor_how_to.html',
            'nav_list': None
        },
        '/files': {
            'label': "Printable Sheets",
            'navbar': ( '/', ),
            'template_to_render': 'utility/game/files.html',
            'nav_list': None
        }
    }
