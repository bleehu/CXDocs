# CXDocs
Compound X rules displayed as web pages. Written in Python, served with Flask and bootstraped with bootswatch.

to set up, 
1) $git clone https://github.com/bleehu/CXDocs.git
2) $sudo pip install flask 

to test, use:
$python start.py
then in a web browser, go to localhost:5000/levelup

For LAN, use:
$python start.py -i local.ip.goes.here
to find your local ip address on linux, use ifconfig. 
to find your local ip address on windows, use ipconfig in bash

For WWW use:
No F---ing way. It's not even close to being secure or ready yet. Don't go there.
When we *are* ready, use an apache server and make sure to configure 
it for HTTPS using openssl TLS 1.2 minimum. Also check to see if nginx is free.

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
