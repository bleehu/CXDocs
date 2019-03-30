# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)
def get_filepath_dict():
    return {
        # Paths should match options in the Parser section of the config file
        # Each path key must have a tuple containing values IN THE FOLLOWING ORDER:
            # a label string (this will be seen by users (keep it brief))
            # a route string (this is where the link will take a user to; include full route for now with all slashes)
            # a navbar tuple (NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar)

            # (optional) 4th value: a nav_list tuple, listing the options that would appear under its navbar label (usually to very specific pages)

        'new_player_walkthrough_filepath': (
            "New to RPGs?",
            '/newplayer',
            ('/rules/overview', '/races', '/classes', '/files'),
            ('/rules/combat', '/files', '/rules/glossary')
        ),
        'basic_rules_filepath': (
            "Getting Started",
            '/rules/overview',
            ('/newplayer', '/races', '/classes', '/rules/glossary')
        )
    }
