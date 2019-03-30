# Gives the initial piece of the dictionary where we have to manually enter paths
def get_dict():
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
            'navbar': ( '/rules/overview', '/rules/', '/gm/' ),
            'template_to_render': 'home.html',
            'filepath_option': None,
            'nav_list': None
        },
        '/rules/': {
            'label': "Rules",
            'navbar': ( '/newplayer', '/rules/combat', '/weapons/', '/rules/glossary', ),
            'template_to_render': 'home.html',
            'filepath_option': None,
            'nav_list': (
                '/rules/glossary',
                '/rules/combat',
                '/rules/conditions',
                '/rules/cloaking'
            )
        },
        '/gm/': {
            'label': "For GMs",
            'navbar': ( '/rules/', '/rules/glossary', '/gm/' ),
            'filepath_option': None,
            'nav_list': (
                '/gm/designhowto',
                '/gm/monsterweaponshowto',
                '/gm/monsterarmorhowto'
            )
        },
        '/weapons/': {
            'label': "Weapons",
            'navbar': ( '/newplayer', '/rules/', '/items/misc' ),
            'template_to_render': 'home.html',
            'filepath_option': None,
            'nav_list': (
                '/weapons/melee',
                '/weapons/pistols',
                '/weapons/smgs',
                '/weapons/carbines',
                '/weapons/longrifles',
                '/weapons/machineguns',
                '/weapons/attachments',
                '/weapons/armor'
            )
        },
        '/files': {
            'label': "Printable Sheets",
            'navbar': ('/rules/overview', '/races', '/classes', '/files'),
            'template_to_render': 'utility/game/files.html',
            'nav_list': None
        }
    }
