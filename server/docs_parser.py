
import argparse #we use the argparse module for passing command-line arguments on startup.
import pdb #the python debugger is helpful during development, but shouldn't be in production.
import re #regular expressions
import os #os handles files

#this variable keeps a unique ID number for each token. 
global new_id

""" This helper method reads arguments from the command line. That way, you can use the document parser without needing to build the full CXDocs stack.
    usage: $python docs_parser docs/example.txt  """
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("p", metavar="filepath/to/doc.txt", help="relative or absolute filepath to the document you'd like to test parsing on.")
    args = parser.parse_args()
    return args

"""
This method adds a token to the end of the list of tokens which is being built up. This method also increments the new_id number, so that each
token has an awareness of its own index. This token id number is used for things like linking the table of contents or having a unique ID for 
javascript methods. 

tokens: the list of all of the tokens which the parser is accumulating in order. When parsing is complete, this list will be sent to the parsing
    JINJA template in repo/templates/parser.html

new_token: the new token to be added to the end of the list of all tokens parsed from this document. 
"""
def append_token(tokens, new_token):
    global new_id
    new_token['id'] = new_id
    new_id = new_id + 1
    tokens.append(new_token)

""" This function runs through a plain text document in the style esablished at github.com/bleehu/CX_Design_Guide/devProcesses/plaintext_style_guide.text 
    and returns an ordered list of tokens which can be interpreted by the repo/templates/parser.html JINJA template to be rendered as a web page. That way
    we can dynamically show Compound X Docs rules as colorful web pages without our developers needing to write each rule in html. 

    filepath: the absolute filepath to the document that should be parsed. EX: /home/blah/docs/compound_x/Items/07_items.txt 

    returns list of tokens. Tokens are listed as maps with the following keys:
    * type: the type of element, usually in terms of html
    * content: the text within the html element, usually used like innerHTML javascript property.
    * id: the unique integer indentifer of this element. 
    Returns None if the passed filepath isn't a valid file
    """
def parse(filepath):
    if not os.path.isfile(filepath):
        print("ERROR!: %s isn't a file!" % filepath)
        return None
    tokens = []
    with open(filepath) as docfile:
        global new_id
        new_id = 0
        index = 0
        lines = docfile.readlines()
        while index < len(lines):
            #decide which kind of token we are looking at
            try:
                lines[index].encode('ascii') #check to make sure there are no illegal characters
                if lines[index].strip() == '': #if the next line is blank
                    pass
                elif lines[index][0:4] == '    ' or lines[index][0] == '\t': #if the next line is an indented paragraph
                    index = append_paragraph(lines, index, tokens)
                elif lines[index].strip() == '=============================='\
                    and index + 2 < len(lines)\
                     and lines[index + 2].strip() == '==============================': # if the next line is a Heading
                    index = append_Heading(lines, index, tokens)
                elif lines[index][0:4].strip() == '====' and lines[index].strip()[-4:] == '====': #if the next line is a sub Heading
                    append_subHeading(lines, index, tokens)
                elif lines[index].strip()[0:2] == '==' and lines[index].strip()[-2:] == '==':
                    append_Section(lines, index, tokens)
                elif lines[index].strip()[-1] == ':':
                    append_subsection(lines, index, tokens)
                elif re.match('^\d+\. ', lines[index]) != None:
                    index = append_numbered_list(lines, index, tokens)
                elif lines[index].strip()[0:2] == '* ' or lines[index][0:2] =='- ':
                    index = append_unordered_list(lines, index, tokens)
                elif lines[index].strip()[0] == "*":
                    index = append_footnote(lines, index, tokens)
                elif lines[index].count(':') == 1 and lines[index + 1].count(':') == 1:
                    index = append_definition_list(lines, index, tokens)
                elif len(lines) > index + 1 and lines[index].strip()[:2] == '+-'\
                 and lines[index + 1].strip()[0] == '|':
                    index = append_table(lines, index, tokens) 
                else: #if we have no idea what it is
                    #dump text as normal
                    new_token = {'type':'unknown', 'content':lines[index]}
                    append_token(tokens, new_token)
            except Exception as error:
                if 'reason' not in dir(error):
                    error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.message)}
                else:
                    error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.reason)}
                append_token(tokens, error_token)
            index = index + 1 
    return tokens

def append_Heading(lines, index, tokens):
    index = index + 1
    new_token = {'type':'h1', 'content':lines[index]}
    append_token(tokens, new_token)
    return index + 1

def append_subHeading(lines, index, tokens):
    new_token = {'type':'h2', 'content':lines[index].strip()[5:-5]}
    append_token(tokens, new_token)

def append_Section(lines, index, tokens):
    new_token = {'type':'h3', 'content':lines[index].strip()[2:-3]}
    append_token(tokens, new_token)

def append_subsection(lines, index, tokens):
    new_token = {'type':'h4', 'content':lines[index][0:-1]}
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

if __name__ == "__main__":
    args = get_args()
    all_the_tokens = parse(args.p)
    for token in all_the_tokens:
        print(token)