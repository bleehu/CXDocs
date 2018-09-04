# Compound X Docs Server

## What is all of this stuff?

Here's a quick rundown on what's all in this directory.


### app.py

app.py is a special python file that the Flask python tool recognizes as holding
the definition for our web app. It holds the routes to each of our pages and 
API endpoints, as well as serving as our main point of entry for the code.

### enemies directory

The Enemies directory is a python module that holds the code files for the 
bestiary feature. It has the routes for making new enemies, new enemy abilities,
weapons, armor, etc. 

### characters directory

The characters directory is a python module that hodes the code files for the 
character creator feature. It has the routes for creating and viewing a user's 
characters, feats, skills, weapons, etc. 

### static directory

The [static directory](http://flask.pocoo.org/docs/1.0/quickstart/#static-files) 
is a special directory expected by Flask. It houses files that need to be served
online, but which don't change depending on user input. Flask serves them from
cache to make it faster.

### templates directory

The [templates directory](http://flask.pocoo.org/docs/1.0/quickstart/#rendering-templates) 
is another special directory expected by flask that serves all of the 
[jinja templates](http://jinja.pocoo.org/) that we use to programatically 
display our webapp's information in a browser.

### security directory

The security module is one that we wrote to help each of the other modules 
prevent common web attacks like SQL injection.

### docs_parser.py

The docs parser object is one that we wrote to quickly and prettily display 
the rules of Compound X. 

### cxDocs.log

If you've sucessfully run CXDocs, you've likely got this logfile that captures
any errors or important runtime events. 

### guestbook.py

This class is one that we wrote to let everyone know who is on the server. It
helps make users feel like part of a community, and helps admins not shut the
server down when people are in the middle of making new characters.