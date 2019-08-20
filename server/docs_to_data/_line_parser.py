import re

from _token_class import Token

_re_str = r'('                                  # G0 START - Create group 0
_re_str += r'^( {4}|\t)'                        # Check for paragraphs (4 spaces or a tab) at start of line
_re_str += r'|^\s*('                            # G1 START - Check for other patterns at start of line that don't rely on whitespace
_re_str += r'\={30}|\={5}|\={2}'                # Headings patterns (chapter, section, subsection)
_re_str += r'|[\*-]\s'                          # Unordered List item
_re_str += r'|\*{1,2}'                          # Footnotes (footnote or long_footnote)
_re_str += r'|\+\-'                             # Table corner
_re_str += r'|\|'                               # Table data row
_re_str += r')'                                 # G1 END - Close group looking at start of line
_re_str += r'|((?<=^\d)|(?<=^\d\d))\.(?=\s)'    # Ordered List patterns (lookbehind has strict rules; lists shouldn't go over 99 anyway)
_re_str += r'|\:$|\:\s'                         # Colon patterns (topic and definition)
_re_str += r')'                                 # G0 END - Close group 0

TOKENS_REGEX = re.compile(_re_str)      # Regex pattern used exclusively for finding patterns which indicate what tokens need to be made

PATTERN_TO_TYPE = {
    '==============================': 'chapter',
    '=====': 'section',
    '==': 'subsection',
    ':': 'topic',
    '    ': 'paragraph',
    '\t': 'paragraph',
    '* ': 'unordered_list',
    '- ': 'unordered_list',
    '*': 'footnote',
    '**': 'footnote',
    ': ': 'definition_list',
    '+-': 'table',
    '|': 'table_row',
    '.': 'ordered_list',
}

def _create_token(tkn_type, content):
    if tkn_type == 'ordered_list' or tkn_type == 'unordered_list':
        # List items will be children of a list group's token
        new_token = Token(tkn_type)
        new_token.children.append(Token('list_item', content))
    else:
        new_token = Token(tkn_type, content)

        # For definition item, add definition as child of term
        if tkn_type == 'definition_list':
            new_token.children.append(Token(tkn_type, _extract_content_from_line(text_line.lstrip(), content + ': ')))

    return new_token

def _extract_content_from_line(text, match, tkn_type):
    if tkn_type == 'section' or tkn_type == 'subsection':
        content_list = text.split(match, 2)
    else:
        content_list = text.split(match, 1)

    if tkn_type == 'ordered_list':
        content_list.pop(0)     # Pop number from ordered item
    else:
        content_list.remove('')

    return content_list[0].strip()

def _add_row_to_table_token(table_token, raw_text):
    row_token = Token('table_row')

    data_with_whitespace = raw_text.strip()[1:-1].split('|')

    for raw_data in data_with_whitespace:
        row_token.children.append(Token('table_data', raw_data.strip()))

    table_token.children.append(row_token)

    return table_token

def process_line(token, text_line):
    # Blank line means closing latest token or doing nothing
    if not text_line.lstrip():
        if token is not None and token.is_not_complete():
            token.close()
            return token
        return None

# MATCH PATTERN / DETERMINE TYPE

    match = re.search(TOKENS_REGEX, text_line)

    if match is not None:
        match = match.group(0)

    # No match or in the middle of a paragraph means raw content; add it to latest token if allowed
    if match is None or (token is not None and token.type == 'paragraph' and token.is_not_complete()):
        if token is not None and token.is_not_complete():
            token.add_content(text_line.lstrip())

            if token.type == 'chapter':
                token.generate_ID()

            return token

        else:
            return None     # Exit if latest token is complete and there's no match to process a new token
    else:
        # Get a type if there's a match
        tkn_type = PATTERN_TO_TYPE.get(match)

    # Update table if we're currently on one (otherwise these actions will be skipped and a new table will be created)
    if 'table' in tkn_type:
        if token is not None and token.type == 'table' and token.is_not_complete():
            if tkn_type == 'table':
                return token        # Leave if we're in between rows on a table
            if tkn_type == 'table_row':
                return _add_row_to_table_token(token, text_line)

# EXTRACT CONTENT

    content = ''

    if tkn_type == 'chapter' and token is not None:
        # Close latest token if matched as chapter and is open
        if token.type == 'chapter' and token.is_not_complete():
            token.close()
            return token
    elif tkn_type != 'chapter' and tkn_type != 'table':
        # Parse content based on type (new chapter and table tokens will not have content on creation (or between rows))
        content = _extract_content_from_line(text_line, match, tkn_type)

# USE CONTENT

    # Add list item if latest token is incomplete list group
    ul_or_ol = 'ordered_list'   # Conditional substring for both unordered and ordered lists ("_list" would also get definition lists)
    if ul_or_ol in tkn_type and ul_or_ol in token.type and token.is_not_complete():
        token.children.append(Token('list_item', content))
        return token

    # Last option: create a token
    return _create_token(tkn_type, content)
