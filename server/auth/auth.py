from ..appConfig.appConfig import ConfigOptionMissingException
from ..cxExceptions import cxExceptions
from ..security.security import sql_escape
import psycopg2

class User:

    def __init__(self, params_tuple): 
        self.pk_id = int(params_tuple[0])
        self.username = params_tuple[1]
        self.displayname = params_tuple[2]
        self.realname = params_tuple[3]
        self.password = params_tuple[4]
        self.role = params_tuple[5]

class AuthServer:

    def __init__(self, config_map, log):
        if 'username' in config_map:
            self.db_user = config_map['username']
        else:
            raise cxExceptions.ConfigOptionMissingException("login database username")
        if 'password' in config_map:
            self.db_pass = config_map['password']
        else:
            raise cxExceptions.ConfigOptionMissingException("login database password")
        if 'name' in config_map:
            self.db_name = config_map['name']
        else:
            raise cxExceptions.ConfigOptionMissingException("name of login database")
        if 'host' in config_map:
            self.db_address = config_map['host']
        else:
            #psychopg2 and most mysql drivers default to localhost.
            self.db_address = "localhost"
        if 'port' in config_map:
            self.db_port = config_map['port']
        else:
            #psychopg2 defaults to port 5432
            self.db_port = 5432
        if 'max_tries' in config_map:
            self.max_tries = int(config_map['max_tries'])
        else:
            self.max_tries = 3
        if 'max_tries_minutes' in config_map:
            self.max_tries_minutes = int(config_map['max_tries_minutes'])
        else:
            self.max_tries_minutes = 30
        self.log = log

    def login(self, username, password, request):
        saniUser = sql_escape(username)
        saniPass = sql_escape(password)
        self.logRateLimitedAction(saniUser, saniPass, request.remote_addr)
        if self.overRateLimit(saniUser, saniPass, request.remote_addr):
            actionString = "login(%s, %s)" % (saniUser, saniPass)
            raise cxExceptions.RateLimitExceededException(saniUser, actionString, 3, 30, request.remote_addr)
        queryString = "SELECT pk_id, username, displayname, realname, password, role  \
            FROM users WHERE username LIKE '%s';" % saniUser
        results = self.fetchall(queryString)
        for result in results:
            if password == result[4]:
                self.log.info('logged in: %s. Password matches.' % saniUser )
                newUser = User(result)
                return newUser
        userPassTuple = (username, password)
        raise cxExceptions.NoUserFoundException(userPassTuple, request)


    def logout(self, session):
        self.log.info("%s logged out." % session['username'])
        session.clear()

    def logRateLimitedAction(self, username, password, ipAddress):
        myCursor = self.getCursor()
        myCursor.execute("INSERT INTO login_audit_log (username, password, ip_address) \
            VALUES ('%s', '%s', '%s');" % (username, password, ipAddress))
        myCursor.connection.commit()

    def overRateLimit(self, username, password, ipAddress):
        #check the number of attempts in the last half hour
        logins = self.fetchall("SELECT * FROM login_audit_log \
            WHERE age(log_time) < '%s minutes' AND \
            ip_address LIKE '%s' AND \
            'username' LIKE '%s';" % \
            (self.max_tries_minutes, ipAddress, username))
        return len(logins) > self.max_tries

    def fetchall(self, searchString):
        myCursor = self.getCursor()
        myCursor.execute(searchString)
        returnMe = myCursor.fetchall()
        return returnMe

    def getCursor(self):
        connection = psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % \
            (self.db_name, self.db_user, self.db_pass, self.db_address, self.db_port))
        myCursor = connection.cursor()
        return myCursor
