# Gets the rules routes together
import _rules_gameplay, _rules_items, _rules_characters

def generate_all_routes_dict(options_list):
    routes_dict = {}

    gameplay_dict = _generate_routes_dict_from_options(options_list, _rules_gameplay.get_path_dict(), 'gameplay')
    if gameplay_dict != None and len(gameplay_dict) > 0:
        routes_dict.update(gameplay_dict)

    item_dict = _generate_routes_dict_from_options(options_list, _rules_items.get_path_dict(), 'items')
    if item_dict != None and len(item_dict) > 0:
        routes_dict.update(item_dict)

    character_dict = _generate_routes_dict_from_options(options_list, _rules_characters.get_path_dict(), 'characters')
    if character_dict != None and len(character_dict) > 0:
        routes_dict.update(character_dict)

    return routes_dict

# Returns a dictionary with endpoints as keys, unless no values match, then returns None
def _generate_routes_dict_from_options(options_list, path_dict, category):
    dict_length = len(path_dict)

    route_dict = {}

    for path in path_dict:
        if path in options_list:
            # Add route to dict, generating its dict values based on file's path dict
            route_dict[path_dict[path][1]] = {
                'label': path_dict[path][0],
                'filepath_option': path,
                'navbar': path_dict[path][2],
                'nav_list': None if len(path_dict[path]) <= 3 else path_dict[path][3]
            }

            dict_length -= 1

    if dict_length > 0:
        print("Warning: Discrepancy between {} rules paths and config options.".format(category))

    if len(route_dict) < 1:
        print("Looked for {} rules documents, but didn't find any. See config/README.md to configure rules docs.".format(category))
        return None

    return route_dict
