# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)

_rules_navbar = ('/rules/overview', '/rules/', '/rules/checks', '/rules/glossary')

def get_dict():
    return {
        '/rules/checks': {
            'label': "Rolling Checks",
            'navbar': _rules_navbar,
            'template_to_render': 'home.html',
            'filepath_option': None,
            'nav_list': None
        }
    }

def get_filepath_dict():
    return {
        # Paths should match options in the Parser section of the config file
        # Each path key must have a tuple containing values IN THE FOLLOWING ORDER:
            # a label string (this will be seen by users (keep it brief))
            # a route string (this is where the link will take a user to; include full route for now with all slashes)
            # a navbar tuple (NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar)

            # (optional) 4th value: a nav_list tuple, listing the options that would appear under its navbar label (usually to very specific pages)

        'combat_rules_filepath': (
            "Combat",
            '/rules/combat',
            _rules_navbar
        ),
        'conditions_filepath': (
            "Ailments",
            '/rules/conditions',
            _rules_navbar
        ),
        'cloaking_filepath': (
            "Cloaking",
            '/rules/cloaking',
            _rules_navbar
        ),
        'glossary_filepath': (
            "Glossary",
            '/rules/glossary',
            _rules_navbar
        )
    }
