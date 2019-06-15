from .. import guestbook
from flask import request, session
import psycopg2

global user_user #the postgres user that has permission to look at the table of users
global user_password # the password for the postgres user that looks up users
global log

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

def get_login_db_connection():
    global user_user
    global user_password
    connection = psycopg2.connect("dbname=mydb user=%s password=%s host=localhost" % (user_user, user_password))
    return connection


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

def get_user_pkid(session):
    if 'username' not in session.keys():
        return None
    username = session['username']
    connection = get_login_db_connection()
    my_cursor = connection.cursor()
    my_cursor.execute("SELECT pk_id FROM users WHERE username = '%s';" % username)
    line = my_cursor.fetchall()[0]
    return int(line[0])

def initialize(new_user, new_password, new_log):
    global user_user
    user_user = new_user
    global user_password
    user_password = new_password
    global log
    log = new_log
