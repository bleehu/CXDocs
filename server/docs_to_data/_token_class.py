try:
    from urllib.parse import quote_plus # Look for Py3.0 version
except ImportError:
    from urllib import quote_plus   # Fall back to Py2.7 version

from json import dumps

class Token:
    TYPE_TO_TAG = {
        'chapter': 'h2',
        'section': 'h3',
        'subsection': 'h4',
        'topic': 'h5',
        'paragraph': 'p',
        'unordered_list': 'ul',
        'footnote': 'aside',
        'definition_list': 'dl',
        'table': 'table',
        'table_row': 'tr',
        'table_data': 'td',
        'ordered_list': 'ol',
        'list_item': 'li'
    }

    IS_TYPE_MULTILINE = {
        'chapter': True,
        'section': False,
        'subsection': False,
        'topic': False,
        'paragraph': True,
        'unordered_list': True,
        'footnote': True,
        'definition_list': False,
        'table': True,
        'table_row': False,
        'table_data': False,
        'ordered_list': True,
        'list_item': False
    }

    _id_count = 0

    def __init__(self, tkn_type, content=''):
        self.type = tkn_type
        self.tag = self.TYPE_TO_TAG.get(tkn_type)
        self.content = content
        self.children = []  # List of tokens

        if tkn_type == 'section':
            self.generate_ID()

        if self.IS_TYPE_MULTILINE.get(tkn_type):
            self.incomplete = True

    def generate_ID(self):
        self.id = '#{}_{}'.format(self._id_count, quote_plus(self.content))
        Token._id_count += 1

    def close(self):
        if hasattr(self, 'incomplete'):
            del self.incomplete

    def add_content(self, text):
        if self.is_not_complete():
            if self.content == '' \
            or self.content.endswith('-'): # (Check for connecting punctuation (to be improved))
                self.content += text
            else:
                self.content += ' ' + text

    def is_not_complete(self):
        return hasattr(self, 'incomplete')

    def to_JSON(self):
        return dumps(self, default = lambda o: o.__dict__)

def reset_token_id_count():
    Token._id_count = 0