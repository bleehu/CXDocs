import argparse #we use the argparse module for passing command-line arguments on startup.
import pdb #the python debugger is helpful during development, but shouldn't be in production.
import re #regular expressions
import os #os handles files

from _switcher import process_line

def parse_file(filepath):
    if not os.path.isfile(filepath):
        print "ERROR!: %s isn't a file!" % filepath
        return None

    tokens = []

    with open(filepath) as docfile:
        index = 0
        tokens_index = 0
        curr_token = None

        lines = docfile.readlines() # creates list of strings, each line is an item
        print('open')

        while index < len(lines):
            # print('LOG:::INDEX:::line: ', index, lines[index])
            try:
                lines[index].encode('ascii') #check to make sure there are no illegal characters
                curr_line = lines[index].rstrip()

                # print('go to process')

                curr_token = process_line(curr_token, curr_line)

                # Append top headings to tokens list (for in-page jumping); others are children
                if curr_token is not None and not hasattr(curr_token, 'incomplete'):
                    if curr_token.type == 'chapter' or curr_token.type == 'section':
                        tokens.append(curr_token)
                    else:
                        tokens[-1].children.append(curr_token)

            except Exception as error:
                if 'reason' not in dir(error):
                    error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.message)}
                else:
                    error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.reason)}

            index += 1

    def print_tokens(tList, child=0):
        for el in tList:
            indent = [' '] * (child * 4)
            print('{}TOKEN: {};\t\tlength: {};\t\tchildren: {}\n{}"{}"'.format(''.join(indent), el.type, len(el.content), len(el.children), ''.join(indent), el.content[:(90 - len(indent))]))

            if len(el.children) > 0:
                print_tokens(el.children, child + 1)

    print('\n\n=============== PRINT TOKENS ===============')
    print_tokens(tokens)

    return tokens
