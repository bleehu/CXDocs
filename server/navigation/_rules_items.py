# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)
def get_path_dict():
    return {
        # Paths should match options in the Parser section of the config file
        # Each path key must have a tuple containing values IN THE FOLLOWING ORDER:
            # a label string (this will be seen by users (keep it brief))
            # a route string (this is where the link will take a user to; include full route for now with all slashes)
            # a navbar tuple (NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar)

            # (optional) 4th value: a nav_list tuple, listing the options that would appear under its navbar label (usually to very specific pages)

        'melee_weapons_filepath': (
            "Melee Weapons",
            '/items/meleeweapons',
            ('/rules/overview')
        ),
        'pistols_filepath': (
            "Pistols",
            '/items/pistols',
            ('/rules/overview')
        ),
        'smgs_filepath': (
            "SMGs",
            '/items/smgs',
            ('/rules/overview')
        ),
        'carbines_filepath': (
            "Carbines",
            '/items/carbines',
            ('/rules/overview')
        ),
        'long_rifles_filepath': (
            "Long Rifles",
            '/items/longrifles',
            ('/rules/overview')
        ),
        'machineguns_filepath': (
            "Heavy Guns",
            '/items/machineguns',
            ('/rules/overview')
        ),
        'weapon_attachments_filepath': (
            "Weapon Attachments",
            '/items/weaponattachments',
            ('/rules/overview')
        ),
        'armor_filepath': (
            "Armor",
            '/items/armor',
            ('/rules/overview')
        ),
        'items_filepath': (
            "Misc",
            'items/misc',
            ('/rules/overview')
        )
    }
