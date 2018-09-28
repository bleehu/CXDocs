# CXDocs
Compound X rules displayed as web pages. Written in Python 2.7, served with Flask and bootstraped with bootswatch.

# set up
## Python module instalation
### On Ubuntu 16.04 
1) $sudo apt-get install python
2) $sudo apt-get install build-essentials
2) $sudo apt-get install python-pip
4) $pip install --upgrade pip
1) $git clone https://github.com/bleehu/CXDocs.git
2) $sudo pip install flask 
3) $sudo pip install pipenv
4) $pipenv install -r travis/requirements.txt

### On Windows
1) Install Python https://www.python.org/
2) Add Python and Python Scripts to Path https://stackoverflow.com/questions/21372637/installing-python-2-7-on-windows-8
3) Use pip to install flask and psycopg2 (it was added to command prompt with python scripts)
4) resolve local host and open port 5000 ???

### Helpful hints on windows
1) Use the windows Command Prompt
2) cd is change directory, dir is list contents of a directory
3) use cd /d G:\ to change to g drive if need be


to test navigate to the root directory and, use:

`$export FLASK_APP=sever/app.py` or on Windows: `$set FLASK_APP=server/app.py`
`$export FLASK_ENV=development` or on Windows: `$set FLASK_ENV=development`
`$flask run`


then in a web browser, go to localhost:5000/levelup

For sharing dev over LAN (for one house), use:

`$python start.py -i local.ip.goes.here`

to find your local ip address on linux, use ifconfig in a terminal. 

to find your local ip address on windows, use ipconfig in bash.

For WWW use:

CXDocs is being tested on an AWS instance behind an NGinX SSL proxy. There are 
still some improvements that should be made in order to keep it safe. Feel free 
to contact bleehu@uw.edu for information about how to stand up your own public 
instance of CX Docs.


## Setting up configs

Compound X comes with a handy little script for generating appropriate config 
files that help it do things like save pictures for the monster bestiary, etc. 
Generating a config is as easy as running 

`$python generate_config.py`

That should write a file in /config/cxDocs.cfg which will have useful options 
set which are detailed in /config/Readme.md

## Setting up postgres database for login, bestiary, and character creation

you will need Postgres 9.5.x 

### On Ubuntu 16.04  

Postgres should be already installed. To check, try typing into the console: 

`psql --version`

If it's not installed

`sudo apt-get install postgresql` 

`sudo apt-get install postgresql-client-common`

and

`sudo apt-get install postgresql-client-9.5`

### On Windows

Windows doesn't come with postgres standard. It's almost like they didn't expect 
you to run a webserver off of your office box. 

To download Postgres, go here: https://www.postgresql.org/download/windows/

Not really sure how to set the database up after that, but we'll work on it!

Likely on Windows, you'll want to use the (PGAdmin III GUI)[https://www.pgadmin.org/download/] 
to work with the database rather than the Command Line Interface that the penguins 
using linux will use. 

There should be documentation on how to use pgAdmin3 to restore a database 
(in this direction.)[https://www.pgadmin.org/docs/pgadmin3/1.22/restore.html] 
but most of our devs use linux, and we haven't figured out how to do this on
Windows for sure yet.

### To initialize the database (Linux/Ubuntu)

To start with, you'll need to add an entry to postgres's authentication config
file. It _usually_ lives at `/etc/postgresql/10/main/pg_hba.conf` but your version
number may vary. The file is always called `pg_hba.conf` though. You'll need 
`sudo` to modify it. Read the comments in the file; they're brief and helpful, 
and as they direct, add an entry at the bottom for 
```local all yourusername ident
local dbname searcher password
local dbname validator password```

You will need to configure postgres to accept CXDocs to login with a username and 
password. To do this, you'll need to edit /etc/postgresql/9.5/main/pg_hba.conf 
and add something like 
to the file. 

Once you've modified the pg_hba.conf file, you'll need to restart postgres with the new configs.

`$ sudo service postgresql restart`

## To configure the db

Before CXDocs is able to log in, you will need to also create the appropriate 
user on your particular database and declare it's password. Details on how to 
do that here:

`https://www.postgresql.org/docs/9.5/static/auth-methods.html#AUTH-PASSWORD`



### On both

Once you have postgres installed and configured to let you log in, use the 
default database config from /config/default_db.db using the pg_restore command


# What's in this Direcory and why is it here?

## Pipfile

The Pipfile helps pipenv track what version of python modules it needs to run
our application. It's also helpful for telling TravisCI what to install before
starting testing.

## Pipfile.lock

A [lock file](https://askubuntu.com/questions/530598/what-is-the-purpose-of-lock-file)
for your pipfile. It also holds security hashes to make sure that someone isn't
poisoning your python libraries.

## Readme.md

A markdown file that shows easy-to-read instructions for using and contributing
to CXDocs. Readme files are displayed on github direcory pages automatically,
and markedown readme files are prettier than text files. What you're reading
right now is the readme file.

## The generate_config.py script

A helpful little script that writes a valid config file for you. It makes 
setting up a new instance of CXDocs much quicker.

## The Server directory

We put the code for the CXDocs web application in here.

## The Travis directory

We put the tests that travis runs in here. It is helpful for making sure what 
we write doesn't break anything.

## The .travis.yml file

This hidden file tells TravisCI what to do with our repo in order to run its
tests.

# Documentation
We use a couple of different technologies in this project. You can find documentation on them here.
* Flask: http://flask.pocoo.org/docs/0.11/tutorial/
* Jinja: http://jinja.pocoo.org/docs/dev/
* Compound X: https://github.com/trowl223/Compound_X/tree/master/play
* for style example, use: http://bootswatch.com/cyborg/
