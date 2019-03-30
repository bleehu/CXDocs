# Gets the rules routes together
import _beginner_resources, _gm_resources, _main_routes
from _rules import _gameplay, _characters, _items

# Aggregates dicts from files where paths are explicitly defined (call .get_dict() from imported files)
def get_all_dicts():
    all_dicts = {}

    all_dicts.update(_main_routes.get_dict())
    all_dicts.update(_gm_resources.get_dict())
    all_dicts.update(_gameplay.get_dict())

    return all_dicts

# Aggregates dicts generated from cfg filepath options (call .get_filepath_dict() from imported files)
def generate_doc_paths_dict_from_cfg_options(options_list):
    doc_paths_dict = {}

    gameplay_dict = _generate_paths_dict_from_filepaths(options_list, _gameplay.get_filepath_dict(), 'gameplay')
    if gameplay_dict != None and len(gameplay_dict) > 0:
        doc_paths_dict.update(gameplay_dict)

    item_dict = _generate_paths_dict_from_filepaths(options_list, _items.get_filepath_dict(), 'items')
    if item_dict != None and len(item_dict) > 0:
        doc_paths_dict.update(item_dict)

    character_dict = _generate_paths_dict_from_filepaths(options_list, _characters.get_filepath_dict(), 'characters')
    if character_dict != None and len(character_dict) > 0:
        doc_paths_dict.update(character_dict)

    beginner_dict = _generate_paths_dict_from_filepaths(options_list, _beginner_resources.get_filepath_dict(), 'beginner')
    if beginner_dict != None and len(beginner_dict) > 0:
        doc_paths_dict.update(beginner_dict)

    return doc_paths_dict

# Returns a dictionary with paths as keys, unless no values match, then returns None
def _generate_paths_dict_from_filepaths(options_list, filepath_dict, category):
    dict_length = len(filepath_dict)

    paths_dict = {}

    for filepath in filepath_dict:
        if filepath in options_list:
            # Add route to dict, generating its dict values based on file's filepath dict
            paths_dict[filepath_dict[filepath][1]] = {
                'label': filepath_dict[filepath][0],
                'filepath_option': filepath,
                'navbar': filepath_dict[filepath][2],
                'nav_list': None if len(filepath_dict[filepath]) <= 3 else filepath_dict[filepath][3]
            }

            dict_length -= 1

    if dict_length > 0:
        print("Warning: Discrepancy between {} rules filepaths and config options.".format(category))

    if len(paths_dict) < 1:
        print("Looked for {} rules documents, but didn't find any. See config/README.md to configure rules docs.".format(category))
        return None

    return paths_dict
