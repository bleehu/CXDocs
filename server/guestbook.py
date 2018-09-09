import time
import pdb

global guestbook
global initialized
initialized = False
global away #seconds to wait until marking someone as away
global out #seconds to wait until signing someone out

def initialize(away_seconds, out_seconds):
    global guestbook 
    guestbook = {}
    global away
    away = away_seconds
    global out
    out = out_seconds
    global initialized
    initialized = True

def sign_guestbook(username):
    if not initialized:
        raise Exception('Attempted to sign Guestbook before Guestbook was initialized!')
    if username not in list(guestbook.keys()):
        guestbook[username] = {}
    guestbook[username]['time'] = time.time()

def get_guestbook():
    if not initialized:
        raise Exception('Attempted to sign Guestbook before Guestbook was initialized!')
    new_book = {}
    return_book = {}
    global guestbook
    global away
    global out
    for signature in list(guestbook.keys()):
        difference = time.time() - guestbook[signature]['time']
        if difference < out:
            new_book[signature] = {}
            return_book[signature] = {}
            new_book[signature]['time'] = guestbook[signature]['time']
            return_book[signature]['time'] = guestbook[signature]['time']
            if int(difference) < int(away):
                new_book[signature]['status'] = 'in'
                return_book[signature]['status'] = 'in'
            else:
                new_book[signature]['status'] = 'away'
                return_book[signature]['status'] = 'away'
    guestbook = new_book
    return return_book