
import argparse #we use the argparse module for passing command-line arguments on startup.
import pdb


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("p", metavar="filepath/to/doc.txt", help="relative or absolute filepath to the document you'd like to test parsing on.")
    args = parser.parse_args()
    return args

def parse(filepath):
    tokens = []
    with open(filepath) as docfile:
        index = 0
        lines = docfile.readlines()
        while index < len(lines):
            #decide which kind of token we are looking at
            try:
                lines[index].encode('ascii')
                if lines[index].strip() == '': #if the next line is blank
                    pass
                elif lines[index][0:4] == '    ' or lines[index][0] == '\t': #if the next line is an indented paragraph
                    index = append_paragraph(lines, index, tokens)
                elif lines[index].strip() == '==============================': # if the next line is a Heading
                    index = append_Heading(lines, index, tokens)
                elif lines[index][0:4].strip() == '====' and lines[index].strip()[-4:] == '====': #if the next line is a sub Heading
                    append_subHeading(lines, index, tokens)
                elif lines[index].strip()[0:2] == '==' and lines[index].strip()[-2:] == '==':
                    append_Section(lines, index, tokens)
                elif lines[index].strip()[-1] == ':':
                    append_subsection(lines, index, tokens)
                elif lines[index].strip()[0:2] == '* ' or lines[index][0:2] =='- ':
                    index = append_unordered_list(lines, index, tokens)
                elif lines[index].count(':') == 1 and lines[index + 1].count(':') == 1:
                    index = append_definition_list(lines, index, tokens)
                else: #if we have no idea what it is
                    #dump text as normal
                    new_token = {'type':'unknown', 'content':lines[index]}
                    tokens.append(new_token)
            except Exception as error:
                error_token = {'type':'error', 'content':'There was an error on line %s: %s' % (index, error.reason)}
                tokens.append(error_token)
            index = index + 1 
    return tokens

def append_Heading(lines, index, tokens):
    index = index + 1
    new_token = {'type':'h1', 'content':lines[index]}
    tokens.append(new_token)
    return index + 1

def append_subHeading(lines, index, tokens):
    new_token = {'type':'h2', 'content':lines[index].strip()[5:-5]}
    tokens.append(new_token)

def append_Section(lines, index, tokens):
    new_token = {'type':'h3', 'content':lines[index].strip()[2:-3]}
    tokens.append(new_token)

def append_subsection(lines, index, tokens):
    new_token = {'type':'h4', 'content':lines[index][0:-1]}
    tokens.append(new_token)

def append_paragraph(lines, index, tokens):
    new_paragraph = {'type':'p','content':lines[index].strip().encode('ascii')}
    index = index + 1
    while index < len(lines) and lines[index].strip() != '':
        lines[index].encode('ascii')
        new_paragraph['content'] = '%s %s' % (new_paragraph['content'], lines[index].strip())
        index = index + 1
    tokens.append(new_paragraph)
    return index

def append_unordered_list(lines, index, tokens):
    new_list = {'type': 'ul', 'content':[]}
    while lines[index][0:2] == '* ' or lines[index][0:2] == '- ':
        new_list['content'].append(lines[index][2:])
        index = index + 1 
    tokens.append(new_list)
    return index

def append_definition_list(lines, index, tokens):
    new_list = {'type':'dl', 'content':[]}
    while lines[index].count(':') == 1:
        (term, definition) = lines[index].split(':')
        new_list['content'].append((term, definition))
        index = index + 1
    tokens.append(new_list)
    return index

if __name__ == "__main__":
    args = get_args()
    all_the_tokens = parse(args.p)
    for token in all_the_tokens:
        print token