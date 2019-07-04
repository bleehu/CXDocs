import re

_re_str = r'('                                  # G0 START by creating group 0
_re_str += r'^(  {4}|\t)'                       # Check for paragraphs (4 spaces or a tab) at start of line
_re_str += r'|^\s*('                            # G1 START - Check for other patterns at start of line that don't rely on whitespace
_re_str += r'\={30}|\={5}|\={2}'                # Headings patterns (chapter, section, subsection) (repetitive equals: 30, 4, and 2)
_re_str += r'|[\*-]\s'                          # Unordered List item
_re_str += r'|\*{1,2}'                          # Footnotes (footnote or long_footnote)
_re_str += r'|\+'                               # Table corner
_re_str += r')'                                 # G1 END - Close group looking at start of line
_re_str += r'|\s*((?<=\d)|(?<=\d\d))\.(?=\s)'   # Ordered List patterns (lookahead has strict rules; lists shouldn't go over 99 anyway)
_re_str += r'|\:$|\:\s'                         # Colon patterns (topic and definition)
_re_str += r')'                                 # G0 END by closing group 0

TOKENS_REGEX = re.compile(_re_str)      # Regex pattern used exclusively for finding patterns which indicate what tokens need to be made

T_SWITCHER = {
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
    '+-': 'table',
    '.': 'ordered_list',

    'TAGS': {
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
        'ordered_list': 'ul'
    }
}

class Token:
    _id_count = 0
    # _special_chars = ('=', '*', '-', ':', '|', '+')  # Tuple for use in checking characters

    def __init__(self, tag, content):
        self.tag = tag
        self.content = ''
        self.children = []  # List of tokens
        if tag == 'h2' or tag =='h3':
            self.id = '#' + content.title().replace(' ', '') + str(_id_count)
            _id_count += 1
        self.incomplete = True  # self.new --> del self.new

    def append_child(self, token):
        self.children.append(token)

    # def create_token(self, tlist):
    #     tnew = Token
    #     tlist.append()

    def complete_token(self):
        del self.incomplete

    def add_content(self, text):
        if self.content == '':
            self.content += text
        else:
            self.content += ' ' + text

    def is_complete(self):
        return not hasattr(self, 'incomplete')

def parse_line(line, tList):
    line_processed = False

    # First traverse tree till we're at an incomplete Token (if one exists) or empty list
    if len(tList) > 0:
        if tList[-1].is_complete():
            print('traverse')
            line_processed = parse_line(line, tList[-1].children)

    # Proceed with processing line if it hasn't been yet
    if not line_processed:
        # try:
        # Use regex to interpret what line will be used for
        matches = re.search(TOKENS_REGEX, line)
        # print('matches: ', matches)

        # Check if we're working with partial or complete Token (if complete, compare to tag)

        # If regex doesn't match, it's either content or a blank line (or something else)
        if matches == None and len(tList) > 0:
            if not tList[-1].is_complete():
                if line.strip() != '':
                    print('Add content (incomplete): ', line)
                    tList[-1].add_content(line) # Add content to last Token if not finished
                else:
                    print('Finish token (blank): ', line)
                    tList[-1].complete_token()  # Mark token as finished if blank line

                line_processed = True   # Line is processed if we started with incomplete token

            print('no match, no processing')
            # Blank or content line is not processed if token is already complete (need exception for multiple blank lines (end of function?))

        # We have a match (use switcher)
        elif matches != None:
            print('MATCH: ', matches.group(0))
            token = T_SWITCHER.get(matches.group(0))
            tag = T_SWITCHER['TAGS'].get(token)

            # if not tList[-1].is_complete()


    return line_processed

def _create_chapter(content):
    return Token('h2', content)

def _create_section(t):
    return t

def _create_subsection(t):
    return t

def _create_topic(t):
    return t

def _create_paragraph(t):
    return t

def _create_paragraph(t):
    return t

def _create_unordered_list(t):
    return t

def _create_unordered_list(t):
    return t

def _create_footnote(t):
    return t

def _create_long_footnote(t):
    return t

def _create_definition_list(t):
    return t

def _create_table(t):
    return t

def _create_ordered_list(t):
    return t


def get_creator(match):
    _switcher = {
        '==============================': _create_chapter,
        '=====': _create_section,
        '==': _create_subsection,
        ':': _create_topic,
        '    ': _create_paragraph,
        '\t': _create_paragraph,
        '* ': _create_unordered_list,
        '- ': _create_unordered_list,
        '*': _create_footnote,
        '**': _create_long_footnote,
        ': ': _create_definition_list,
        '+': _create_table,
        '.': _create_ordered_list
    }

    return _switcher.get(match)
