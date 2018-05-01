import guestbook
from flask import request, session

global log

def initialize(newLog):
    global log
    log = newLog


""" we call this any time someone checks out a page on the site that should be off-limits to someone who
        hasn't logged in. If they aren't logged in, it returns false, if they are, it returns true."""
def check_auth(session):
    if 'username' not in session.keys():
        log.error("Anonymous attempt to access %s! user_agent:%s, remoteIP:%s" % (request.path, request.user_agent.string, request.remote_addr))
        return False
    blacklisted_UA = ['zgrab', 'vas', 'burp']
    for ua in blacklisted_UA:
        if ua in request.user_agent.string.lower():
            return False
    if 'displayname' in session.keys():
        guestbook.sign_guestbook(session['displayname'])
    return True

""" we use this when we use player input to check postgres for a search. For instance, we don't want 
           badguys trying to log in with SQL injection - that could lead to damage to login data."""
def sql_escape(dirty):
    #string.replace(new, old)
    sani = dirty.replace('*','')
    sani = sani.replace('=','')
    sani = sani.replace('>','')
    sani = sani.replace('<','')
    sani = sani.replace(';','')
    sani = sani.replace("'","''")
    #sani = sani.replace("\\", "\\") #need a way to sanitize backslashes for escape characters
    return sani