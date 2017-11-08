# CXDocs
Compound X rules displayed as web pages. Written in Python 2.7, served with Flask and bootstraped with bootswatch.

to set up, 
1) $git clone https://github.com/bleehu/CXDocs.git
2) $sudo pip install flask 
3) $sudo pip install flask_sqlalchemy
4) $sudo apt-get install python-psycopg2

to test, use:
$python start.py
then in a web browser, go to localhost:5000/levelup

For LAN, use:
$python start.py -i local.ip.goes.here
to find your local ip address on linux, use ifconfig. 
to find your local ip address on windows, use ipconfig in bash

For WWW use:
CXDocs is being tested on an AWS instance behind an NGinX SSL proxy. There are still some improvements that should be made in order to keep it safe. 

## Setting up postgres for bestiary
you will need Postgres 9.5.x 
###On Ubuntu 16.04  
Postgres should be already installed. To check, try typing into the console: psql --version
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
To add to this project, check out these links:
Flask:
http://flask.pocoo.org/docs/0.11/tutorial/
Jinja:
http://jinja.pocoo.org/docs/dev/
Compound X:
https://github.com/trowl223/Compound_X/tree/master/play
for style example, use:
http://bootswatch.com/cyborg/
