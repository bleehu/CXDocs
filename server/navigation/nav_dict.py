import _routes_aggregator

_nav_dict = {}  # ONLY ACCESS IN THIS MODULE

def create_dict(options_list):
    length_before_docs = 0

    if len(_nav_dict) == 0:
        _nav_dict.update(_routes_aggregator.get_all_dicts())
        length_before_docs = len(_nav_dict)

    if len(_nav_dict) > 0:
        doc_paths = _routes_aggregator.generate_doc_paths_dict_from_cfg_options(options_list)

        if doc_paths != None and len(doc_paths) > 0:
            _nav_dict.update(doc_paths)

        if len(_nav_dict) == length_before_docs:
            print("Looked for documents, but didn't find any. See config/README.md to configure rules docs.")

    else:
        print("Error: _nav_dict not created.")

### Validators ###
def page_exists(path):
    if path in _nav_dict:
        return True
    else:
        return False

def page_has_filepath(path):
    if (page_exists(path)
        and 'filepath_option' in _nav_dict[path]
        and _nav_dict[path]['filepath_option'] != None
    ):
        return True
    else:
        return False

def page_has_template(path):
    if (page_exists(path)
        and 'template_to_render' in _nav_dict[path]
        and _nav_dict[path]['template_to_render'] != None
    ):
        return True
    else:
        return False

### Getters ###
def get_filepath_for_page(path):
    return _nav_dict[path]['filepath_option']

def get_template_for_page(path):
    return _nav_dict[path]['template_to_render']

### Generators ###
def generate_navbar_options_for_page(path):
    nav_results = []

    for route in _nav_dict[endpoint]['navbar']:
        if route in _nav_dict:
            nav_results.append( (_nav_dict[route]['label'], route) )
        else:
            print(sorted(_nav_dict.keys()))
            raise Exception("Endpoint not found in navigation dictionary! %s" % route)
    return nav_results

def generate_nav_lists_for_page(path):
    list_results = []
    i = 0

    for route in _nav_dict[path]['navbar']:
        list_results.append([])

        if 'nav_list' in _nav_dict[route] and _nav_dict[route]['nav_list'] != None:
            for item in _nav_dict[route]['nav_list']:
                list_results[i].append( (_nav_dict[item]['label'], item) )

        i += 1

    return list_results
