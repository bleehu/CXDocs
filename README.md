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
4) $sudo apt-get install python-psycopg2

### On Windows
1) Install Python https://www.python.org/
2) Add Python and Python Scripts to Path https://stackoverflow.com/questions/21372637/installing-python-2-7-on-windows-8
3) Use pip to install flask and psycopg2 (it was added to command prompt with python scripts)
4) resolve local host and open port 5000 ???

### Helpful hints on windows
1) Use the windows Command Prompt
2) cd is change directory, dir is list contents of a directory
3) use cd /d G:\ to change to g drive if need be


to test, use:
`$python start.py`
then in a web browser, go to localhost:5000/levelup

For LAN, use:
`$python start.py -i local.ip.goes.here`
to find your local ip address on linux, use ifconfig in a terminal. 
to find your local ip address on windows, use ipconfig in bash.

For WWW use:
CXDocs is being tested on an AWS instance behind an NGinX SSL proxy. There are still some improvements that should be made in order to keep it safe. Feel free to contact bleehu@uw.edu for information about how to stand up your own public instance of CX Docs.


##Setting up configs
Compound X comes with a handy little script for generating appropriate config files that help it do things like save pictures for the monster bestiary, etc. Generating a config is as easy as running 
`$python generate_config.py`
That should write a file in /config/cxDocs.cfg which will have useful options set which are detailed in /config/Readme.md

## Setting up postgres for bestiary
you will need Postgres 9.5.x 
###On Ubuntu 16.04  
Postgres should be already installed. To check, try typing into the console: psql --version
If it's not installed, try 
`sudo apt-get install postgresql-client-common`
and
`sudo apt-get install postgresql-client-9.5`

You will need to configure postres to accept CXDocs to login with a username and password. To do this, you'll need to edit /etc/postgresql/9.5/main/pg_hba.conf and add something like 
`local mydb searcher password`
to the file. 
Before CXDocs is able to log in, you will need to also create the appropriate user on your particular database and declare it's password. Details on how to do that here:
`https://www.postgresql.org/docs/9.5/static/auth-methods.html#AUTH-PASSWORD`
###On Windows
Windows doesn't come with postgres standard. It's almost like they didn't expect you to run a webserver off of your office box. 
To download Postgres, go here: https://www.postgresql.org/download/windows/
Not really sure how to set the database up after that, but we'll work on it!
###On both
Once you have postgres installed and configured to let you log in, use the default database config from /config/default_db.db using the pg_restore command



# Documentation
We use a couple of different technologies in this project. You can find documentation on them here.
* Flask: http://flask.pocoo.org/docs/0.11/tutorial/
* Jinja: http://jinja.pocoo.org/docs/dev/
* Compound X: https://github.com/trowl223/Compound_X/tree/master/play
* for style example, use: http://bootswatch.com/cyborg/
