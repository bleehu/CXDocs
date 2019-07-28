import re

_re_str = r'('                                  # G0 START - Create group 0
_re_str += r'^( {4}|\t)'                        # Check for paragraphs (4 spaces or a tab) at start of line
_re_str += r'|^\s*('                            # G1 START - Check for other patterns at start of line that don't rely on whitespace
_re_str += r'\={30}|\={5}|\={2}'                # Headings patterns (chapter, section, subsection)
_re_str += r'|[\*-]\s'                          # Unordered List item
_re_str += r'|\*{1,2}'                          # Footnotes (footnote or long_footnote)
_re_str += r'|\+'                               # Table corner
_re_str += r'|\|'                               # Table data row
_re_str += r')'                                 # G1 END - Close group looking at start of line
_re_str += r'|((?<=^\d)|(?<=^\d\d))\.(?=\s)'   # Ordered List patterns (lookbehind has strict rules; lists shouldn't go over 99 anyway)
_re_str += r'|\:$|\:\s'                         # Colon patterns (topic and definition)
_re_str += r')'                                 # G0 END - Close group 0

TOKENS_REGEX = re.compile(_re_str)      # Regex pattern used exclusively for finding patterns which indicate what tokens need to be made

T_SWITCHER = {
    'PATTERN_TO_TYPE': {
        '==============================': 'chapter',
        '=====': 'section',
        '==': 'subsection',
        ':': 'topic',
        '    ': 'paragraph',
        '\t': 'paragraph',
        '* ': 'unordered_list',
        '- ': 'unordered_list',
        '*': 'footnote',
        # '**': 'long_footnote',
        '**': 'footnote',
        ': ': 'definition_list',
        '+': 'table',
        '|': 'table_row',
        '.': 'ordered_list',
    },

    'TYPE_TO_TAG': {
        'chapter': 'h2',
        'section': 'h3',
        'subsection': 'h4',
        'topic': 'h5',
        'paragraph': 'p',
        'unordered_list': 'ul',
        'footnote': 'aside',
        # 'long_footnote': 'aside',
        'definition_list': 'dl',
        'table': 'table',
        'table_row': 'tr',
        'table_data': 'td',
        'ordered_list': 'ol',
        'list_item': 'li'
    },

    'IS_TYPE_MULTILINE': {
        'chapter': True,
        'section': False,
        'subsection': False,
        'topic': False,
        'paragraph': True,
        'unordered_list': True,
        'footnote': True,           # Assume true (because long can exist)
        'definition_list': False,
        'table': True,
        'table_row': False,
        'table_data': False,
        'ordered_list': True,
        'list_item': False
    }
}

class Token:
    _id_count = 0

    def __init__(self, tkn_type, content=''):
        # print('CREATE {}: {}'.format(tkn_type, content))
        self.type = tkn_type
        self.tag = T_SWITCHER['TYPE_TO_TAG'].get(tkn_type)
        self.content = content
        self.children = []  # List of tokens

        if tkn_type == 'chapter' or tkn_type == 'section':
            self.id = '#' + str(Token._id_count)
            # print("ID'd: {}".format(self.id))
            Token._id_count += 1

        if T_SWITCHER['IS_TYPE_MULTILINE'].get(tkn_type):
            print('{} is multiline'.format(self.type))
            self.incomplete = True

        # print("SUCCESS!")

    def append_child(self, token):
        self.children.append(token)

    def close(self):
        # print('CLOSE TOKEN')
        if hasattr(self, 'incomplete'):
            del self.incomplete

    # Add text to token,
    def add_content(self, text):
        if not self.is_complete():
            if self.content == '' or self.content[-1] == '-':   # (Checking for connecting punctuation (to be improved))
                self.content += text
            else:
                self.content += ' ' + text

    def is_complete(self):
        return not hasattr(self, 'incomplete')

    # Check content for adding to or completing token; return token (self)
    def update(text_line):
        self.add_content(text_line)

def create_token(tkn_type, content):
    # Add content
    if tkn_type == 'ordered_list' or tkn_type == 'unordered_list':
        # List items will be children of a list group's token
        new_token = Token(tkn_type)
        new_token.children.append(Token('list_item', content))
    else:
        new_token = Token(tkn_type, content)

        # For definition item, add definition as child to term
        if tkn_type == 'definition_list':
            new_token.children.append(Token(tkn_type, extract_content_from_line(text_line.lstrip(), content + ': ')))

    print('NEW {}'.format(new_token.type))
    return new_token

def extract_content_from_line(text, match, tkn_type):
    if tkn_type == 'section' or tkn_type == 'subsection':
        content_list = text.split(match, 2)
    else:
        content_list = text.split(match, 1)

    if tkn_type == 'ordered_list':
        content_list.pop(0)     # Pop number from ordered item
    else:
        content_list.remove('')

    print('extract {}'.format(content_list))

    return content_list[0].strip()

def update_table(table_token, content):
    table_token.children.add_content(content)
    return table_token;

def process_line(token, text_line):
    # Blank line means closing latest token or doing nothing
    if len(text_line.lstrip()) == 0:
        if token != None and not token.is_complete():
            token.close()
            return token
        return None

    # Proceed to processing text

    # GET MATCH; DETERMINE TYPE
    match = re.search(TOKENS_REGEX, text_line)
    print('MATCH::: <{}>'.format(match))

    if match != None:
        match = match.group(0)


    if match == None or (token != None and token.type == 'paragraph' and not token.is_complete()):
        # print('No match; token: {}'.format(token.type))
        # No match or in the middle of a paragraph means raw content; add it to latest token if allowed
        if token != None and not token.is_complete():
            print('Adding content... {}'.format(text_line.lstrip()))
            token.add_content(text_line.lstrip())
            return token
        else:
            return None     # Exit if latest token is complete and there's no match to process a new token
    else:
        # Get a type if there's a match
        tkn_type = T_SWITCHER['PATTERN_TO_TYPE'].get(match)
        # print('TYPE GOT: {}'.format(tkn_type))

    # PARSE CONTENT

    content = ''

    if tkn_type == 'chapter' and token != None:
        # Close latest token if matched as chapter and is open
        if token.type == 'chapter' and not token.is_complete():
            token.close()
            return token
    elif tkn_type != 'chapter' and tkn_type != 'table':
        # Parse content based on type (new chapter and table tokens will not have content on creation (or between rows))
        content = extract_content_from_line(text_line, match, tkn_type)
        # print('Extracted: {}'.format(content))

    # USE CONTENT (CREATION or add to table)
    # Update table if we're currently on one
    if (tkn_type == 'table_row' or tkn_type == 'table') and token != None:
        if token.type == 'table':
            return update_table(token, content)

    # Add list item if latest token is incomplete list group
    ul_or_ol = 'ordered_list'   # Conditional substring for both unordered and ordered lists ("_list" would also get definition lists)
    if ul_or_ol in tkn_type and ul_or_ol in token.type and not token.is_complete():
        token.children.append(Token('list_item', content))
        return token

    # Last option: create a token
    return create_token(tkn_type, content)
