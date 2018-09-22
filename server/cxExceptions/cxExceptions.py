import logging
from Flask import session, flash

global log

"""Initialize the cxErrorHandling global variables."""
def initialize(newlog):
    global log
    log = newlog

""" Our custom exception interface. We should never throw a raw CXException, 
    rather, we use this to provide common methods for providing error handling
    feedback appropriately to the logs, to the user and to the a junior admin
    who is learning how to set up cxdocs."""
class CXException(Exception):

    def provideFeedback(self):
        self.log(log)
        self.printToConsole()
        self.flash()

    @abstractmethod
    def log(self):
        pass

    @abstractmethod
    def printToConsole():
        pass

    @abstractmethod
    def flash():
        pass

class NoMatchFoundException(CXException):
    LOG_MESSAGE = "%s failed to find a match for object %s with id %s"

    def __init__(self, user, expectedType, missingID):
        self.username = user
        self.expectedType = expectedType
        self.missingID = missingID
        self.message = self.LOG_MESSAGE % (user, expectedType, missingID)

    def printToConsole(self):
        print(self.message)

    def log(self):
        log.warn(self.message)

    def flash(self):
        flash("I couldn't find that %s in order to do that." % this.expectedType)

class NoUserFoundException(CXException):
    LOG_MESSAGE = "%s failed to log in with password %s. user_agent:%s, remoteIP:%s"

    def __init__(self, userPassTuple, request):
        self.username = userPassTuple[0]
        self.password = userPassTuple[1]
        self.remote_addr = request.remote_addr
        self.user_agent = request.user_agent.string
        self.message = self.LOG_MESSAGE % (self.username, self.password, self.user_agent, self.remote_addr)

    def printToConsole(self):
        print(self.message)

    def log(self):
        log.warn(self.message)

    def flash(self):
        flash("Sorry, I didn't find a user with that name and password.")

class PermissionViolationException(CXException):
    LOG_MESSAGE = "%s attempted an action that they didn't have permission to perform. \n \
        \tAction: %s\n\
        user:%s, user_agent:%s, remoteIP: %s"

    def __init__(self, action, request):
        self.action = action
        self.remote_addr = request.remote_addr
        self.username = session['username']
        self.user_agent = request.user_agent
        self.message = self.LOG_MESSAGE % (action, self.username, self.user_agent, self.remote_addr)

    def printToConsole(self):
        print(self.message)

    def log(self):
        log.warn(self.message)

    def flash(self):
        flash("Sorry, it looks like you don't have permission to do that.")

class ConfigOptionMissingException(CXException):
    LOG_MESSAGE = "ERROR!: Someone is trying to log in, but cxDocs wasn't started with login enabled."
    ADVICE = """If you'd like to enable login, you'll need to set up your postgres user database 
    then run: $python start.py -u databaseUsername -p databasePassword 
    Use $python start.py -h for more help. And check cxDocs.log for more helpful error messages."""

    def printToConsole(self):
        print(self.message)
        print(self.ADVICE)

    def log(self):
        log.warn(self.message)
        log.info(self.ADVICE)

    def flash(self):
        flash("Sorry, It looks like the admin hasn't set the login database up yet. Check logs?")