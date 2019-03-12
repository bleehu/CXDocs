from ..cxExceptions import cxExceptions
from ..security.security import sql_escape
from ..database import database

class User:

    def __init__(self, params_tuple):
        self.pk_id = int(params_tuple[0])
        self.username = params_tuple[1]
        self.displayname = params_tuple[2]
        self.realname = params_tuple[3]
        self.password = params_tuple[4]
        self.role = params_tuple[5]

class AuthServer:

    def __init__(self, config, log):
        if 'username' not in config:
            raise cxExceptions.ConfigOptionMissingError("login database username")
        if 'password' not in config:
            raise cxExceptions.ConfigOptionMissingError("login database password")
        if 'db_name' not in config:
            raise cxExceptions.ConfigOptionMissingError("name of login database")
        if 'db_host' not in config:
            config['db_host'] = "localhost"
        if 'max_tries' in config:
            self.max_tries = int(config['max_tries'])
        else:
            self.max_tries = 3
        if 'max_tries_minutes' in config:
            self.max_tries_minutes = int(config['max_tries_minutes'])
        else:
            self.max_tries_minutes = 30
        self.my_db = database.CXDatabase(config)
        self.log = log

    def login(self, username, password, request):
        saniUser = sql_escape(username)
        saniPass = sql_escape(password)
        self.logRateLimitedAction(saniUser, saniPass, request.remote_addr)
        if self.overRateLimit(saniUser, saniPass, request.remote_addr):
            actionString = "login(%s, %s)" % (saniUser, saniPass)
            raise cxExceptions.RateLimitExceededError(saniUser, actionString, 3, 30, request.remote_addr)
        queryString = "SELECT pk_id, username, displayname, realname, password, role  \
            FROM users WHERE username LIKE '%s';" % saniUser
        results = self.my_db.fetch_all(queryString)
        for result in results:
            if password == result[4]:
                self.log.info('logged in: %s. Password matches.' % saniUser )
                newUser = User(result)
                return newUser
        userPassTuple = (username, password)
        raise cxExceptions.NoUserFoundError(userPassTuple, request)

    def logout(self, session):
        self.log.info("%s logged out." % session['username'])
        session.clear()

    def logRateLimitedAction(self, username, password, ipAddress):
        insertString = "INSERT INTO login_audit_log (username, password, ip_address) \
            VALUES ('%s', '%s', '%s');" % (username, password, ipAddress)
        self.my_db.update(insertString)

    def overRateLimit(self, username, password, ipAddress):
        #check the number of attempts in the last half hour
        logins = self.my_db.fetch_all("SELECT * FROM login_audit_log \
            WHERE age(log_time) < '%s minutes' AND \
            ip_address LIKE '%s' AND \
            'username' LIKE '%s';" % \
            (self.max_tries_minutes, ipAddress, username))
        return len(logins) > self.max_tries