import argparse #we use the argparse module for passing command-line arguments on startup.
import pdb #the python debugger is helpful during development, but shouldn't be in production.
import re #regular expressions
import os #os handles files

from _switcher import get_creator, parse_line

def parse_file(filepath):
    if not os.path.isfile(filepath):
        print "ERROR!: %s isn't a file!" % filepath
        return None

    tokens = []

    with open(filepath) as docfile:
        index = 0
        lines = docfile.readlines() # creates list of strings, each line is an item
        print('open')

        while index < len(lines):
            #try:
            lines[index].encode('ascii') #check to make sure there are no illegal characters
            curr_line = lines[index].rstrip()

            if not parse_line(curr_line, tokens):
                print('Line Process Error: line index: ', index)

            index += 1


        while index < len(lines):
            #decide which kind of token we are looking at
            try:
                lines[index].encode('ascii') #check to make sure there are no illegal characters
                curr_line = lines[index].rstrip()
                # print('try')


                # match = str(re.search(TOKENS_REGEX, curr_line).group(0))
                # print('`' + match + '`')
                # print('GET: ' + get_creator(match)(match)) # lines?, index?, returns new index?? (even though it's the same data??)

            except Exception as error:
                if 'reason' not in dir(error):
                    error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.message)}
                else:
                    error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.reason)}
                append_token(tokens, error_token)

            index += 1

    # def print_tokens(tList, child=0):
    #     for el in tList:
    #         if el['type'] != 'children':
    #             indent = [' '] * (child * 2)
    #             print('{}PARSEL: {}, {}'.format(''.join(indent), el['type'], el['content'][:10]))
    #         else:
    #             print_tokens(el, child + 1)

    # print_tokens(tokens)

    return tokens

def append_heading(lines, index, tokens):
    index = index + 1
    new_token = {'type':'h2', 'content':lines[index]}
    append_token(tokens, new_token)
    return index + 1

def append_subheading(lines, index, tokens):
    new_token = {'type':'h3', 'content':lines[index].strip()[5:-5]}
    append_token(tokens, new_token)

def append_section(lines, index, tokens):
    new_token = {'type':'h4', 'content':lines[index].strip()[2:-3]}
    append_token(tokens, new_token)

def append_subsection(lines, index, tokens):
    new_token = {'type':'h5', 'content':lines[index][0:-1]}
    append_token(tokens, new_token)

def append_paragraph(lines, index, tokens):
    new_paragraph = {'type':'p','content':lines[index].strip().encode('ascii')}
    index = index + 1 #because we processed the line above
    while index < len(lines) and lines[index].strip() != '':
        try:
            lines[index].encode('ascii')
            new_paragraph['content'] = '%s %s' % (new_paragraph['content'], lines[index].strip())
        except:
            new_paragraph['content'] = '%s %s' % (new_paragraph['content'], 'ERROR ON LINE %s. COULD NOT PARSE.' % index)
        index = index + 1
    append_token(tokens, new_paragraph)
    return index

def append_footnote(lines, index, tokens):
    new_footnote = {'type':'footnote', 'content': ''}
    while index < len(lines) and lines[index].strip() != '':
        try:
            lines[index].encode('ascii')
            new_footnote['content'] = '%s %s' % (new_footnote['content'], lines[index].strip())
        except:
            new_footnote['content'] = '%s %s' % (new_footnote['content'], 'ERROR ON LINE %s. COULD NOT PARSE.' % index)
        index = index + 1
    append_token(tokens, new_footnote)
    return index

def append_unordered_list(lines, index, tokens):
    new_list = {'type': 'ul', 'content':[]}
    while index < len(lines) and (lines[index][0:2] == '* ' or lines[index][0:2] == '- '):
        new_list['content'].append(lines[index][2:])
        index = index + 1
    append_token(tokens, new_list)
    return index - 1

def append_numbered_list(lines, index, tokens):
    new_list = {'type':'ol', 'content':[]}
    regex_pattern = '^\d+\. '
    while index < len(lines) and re.match(regex_pattern,lines[index]) != None:
        match = re.match(regex_pattern,lines[index])
        new_list['content'].append(lines[index][match.end():])
        index = index + 1
    append_token(tokens, new_list)
    return index - 1

def append_definition_list(lines, index, tokens):
    new_list = {'type':'dl', 'content':[]}
    while index < len(lines) and lines[index].count(':') == 1:
        (term, definition) = lines[index].split(':')
        new_list['content'].append((term, definition))
        index = index + 1
    append_token(tokens, new_list)
    return index - 1

def append_table(lines, index, tokens):
    new_table = {'type':'table', 'content':[]}
    index = index + 1 # skip top row of table
    while index < len(lines) and \
    lines[index].strip() != '' and '|' in lines[index]:
        row = lines[index].split('|')
        new_table['content'].append(row)
        index = index + 2 # skip cross lines
    append_token(tokens, new_table)
    return index - 1

def append_token(tokens, new_token):
    # global new_id
    # new_token['id'] = new_id
    # new_id = new_id + 1
    tokens.append(new_token)

if __name__ == "__main__":
    args = get_args()
    all_the_tokens = parse(args.p)
    for token in all_the_tokens:
        print token
