# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)

_items_navbar = ('/rules/overview', '/rules/', '/weapons/', '/items/misc')

def get_filepath_dict():
    return {
        # Paths should match options in the Parser section of the config file
        # Each path key must have a tuple containing values IN THE FOLLOWING ORDER:
            # a label string (this will be seen by users (keep it brief))
            # a route string (this is where the link will take a user to; include full route for now with all slashes)
            # a navbar tuple (NO MORE THAN 4 VALUES; the order listed will be the order displayed on the navbar)

            # (optional) 4th value: a nav_list tuple, listing the options that would appear under its navbar label (usually to very specific pages)

        'melee_weapons_filepath': (
            "Melee Weapons",
            '/weapons/melee',
            _items_navbar
        ),
        'pistols_filepath': (
            "Pistols",
            '/weapons/pistols',
            _items_navbar
        ),
        'smgs_filepath': (
            "SMGs",
            '/weapons/smgs',
            _items_navbar
        ),
        'carbines_filepath': (
            "Carbines",
            '/weapons/carbines',
            _items_navbar
        ),
        'long_rifles_filepath': (
            "Long Rifles",
            '/weapons/longrifles',
            _items_navbar
        ),
        'machineguns_filepath': (
            "Heavy Guns",
            '/weapons/machineguns',
            _items_navbar
        ),
        'weapon_attachments_filepath': (
            "Weapon Attachments",
            '/weapons/attachments',
            _items_navbar
        ),
        'armor_filepath': (
            "Armor",
            '/weapons/armor',
            _items_navbar
        ),
        'items_filepath': (
            "Items",
            '/items/misc',
            _items_navbar
        )
    }
