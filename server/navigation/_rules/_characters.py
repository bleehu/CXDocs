# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)

_characters_navbar = ('/rules/overview', '/rules/', '/races', '/classes', '/rules/glossary')

def get_filepath_dict():
    return {
        # Paths should match options in the Parser section of the config file
        # Each path key must have a tuple containing values IN THE FOLLOWING ORDER:
            # a label string (this will be seen by users (keep it brief))
            # a route string (this is where the link will take a user to; include full route for now with all slashes)
            # a navbar tuple (NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar)

            # (optional) 4th value: a nav_list tuple, listing the options that would appear under its navbar label (usually to very specific pages)

        'races_filepath': (
            "Races",
            '/races',
            _characters_navbar
        ),
        'classes_filepath': (
            "Classes",
            '/classes',
            _characters_navbar
        ),
        'skills_filepath': (
            "Skills",
            '/skills',
            _characters_navbar
        ),
        'feats_filepath': (
            "Feats",
            '/feats',
            _characters_navbar
        ),
        'engineer_filepath': (
            "Engineer Processes",
            '/rules/engineers',
            _characters_navbar
        ),
        'level_up_filepath': (
            "Leveling Up",
            '/rules/levelup',
            _characters_navbar
        )
    }
