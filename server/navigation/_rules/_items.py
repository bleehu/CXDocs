# Need to manually create a dictionary to link the config filepaths to routes with labels and nav lists we want associated with each other.
# (Having to manage this is why the module is broken down into these files.)

_items_navbar = ('/rules/overview', '/rules/', '/weapons/', '/items/misc')
_items_nav_list = (
    '/weapons/melee',
    '/weapons/pistols',
    '/weapons/smgs',
    '/weapons/carbines',
    '/weapons/longrifles',
    '/weapons/machineguns',
    '/weapons/attachments',
    '/weapons/armor',
    '/items/misc'
)

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
            _items_navbar,
            _items_nav_list
        ),
        'pistols_filepath': (
            "Pistols",
            '/weapons/pistols',
            _items_navbar,
            _items_nav_list
        ),
        'smgs_filepath': (
            "SMGs",
            '/weapons/smgs',
            _items_navbar,
            _items_nav_list
        ),
        'carbines_filepath': (
            "Carbines",
            '/weapons/carbines',
            _items_navbar,
            _items_nav_list
        ),
        'long_rifles_filepath': (
            "Long Rifles",
            '/weapons/longrifles',
            _items_navbar,
            _items_nav_list
        ),
        'machineguns_filepath': (
            "Heavy Guns",
            '/weapons/machineguns',
            _items_navbar,
            _items_nav_list
        ),
        'weapon_attachments_filepath': (
            "Weapon Attachments",
            '/weapons/attachments',
            _items_navbar,
            _items_nav_list
        ),
        'armor_filepath': (
            "Armor",
            '/weapons/armor',
            _items_navbar,
            _items_nav_list
        ),
        'items_filepath': (
            "Items",
            '/items/misc',
            _items_navbar,
            _items_nav_list
        )
    }
