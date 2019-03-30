import _manual_routes, _rules

_nav_dict = {}  # ONLY ACCESS IN THIS MODULE

def create_dict(options_list):
    length_before_docs = 0

    if len(_nav_dict) == 0:
        _nav_dict.update(_manual_routes.get_manual_routes())
        length_before_docs = len(_nav_dict)

    if len(_nav_dict) > 0:
        rules_dict = _rules.generate_all_routes_dict(options_list)

        if rules_dict != None and len(rules_dict) > 0:
            _nav_dict.update(rules_dict)

        if len(_nav_dict) == length_before_docs:
            print("Looked for documents, but didn't find any. See config/README.md to configure rules docs.")

    else:
        print("Error: _nav_dict not created.")

### Validators ###
def page_exists(endpoint):
    if endpoint in _nav_dict:
        return True
    else:
        return False

def page_has_filepath(endpoint):
    if (page_exists(endpoint)
        and 'filepath_option' in _nav_dict[endpoint]
        and _nav_dict[endpoint]['filepath_option'] != None
    ):
        return True
    else:
        return False

def page_has_template(endpoint):
    if (page_exists(endpoint)
        and 'template_to_render' in _nav_dict[endpoint]
        and _nav_dict[endpoint]['template_to_render'] != None
    ):
        return True
    else:
        return False

### Getters ###
def get_filepath_for_endpoint(endpoint):
    return _nav_dict[endpoint]['filepath_option']

def get_template_for_endpoint(endpoint):
    return _nav_dict[endpoint]['template_to_render']

### Generators ###
def generate_navbar_options_for_page(endpoint):
    nav_results = []

    for route in _nav_dict[endpoint]['navbar']:
        if route in _nav_dict:
            nav_results.append( (_nav_dict[route]['label'], route) )
        else:
            print(sorted(_nav_dict.keys()))
            raise Exception("Endpoint not found in navigation dictionary! %s" % route)
    return nav_results

def generate_nav_lists_for_page(endpoint):
    list_results = []
    i = 0

    for route in _nav_dict[endpoint]['navbar']:
        list_results.append([])

        if 'nav_list' in _nav_dict[route] and _nav_dict[route]['nav_list'] != None:
            for item in _nav_dict[route]['nav_list']:
                list_results[i].append( (_nav_dict[item]['label'], item) )

        i += 1

    return list_results
