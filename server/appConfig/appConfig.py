from ..cxExceptions.cxExceptions import CXException
import ConfigParser
from ..navigation import nav_dict as nav  # Module created by AK to allow dynamic front-end navigation
import os

def get_app_config(filepath, log):
    return app_config_object(filepath, log)

class app_config_object:

    def __init__(self, config_abs_filepath, log):
        if not os.path.exists(config_abs_filepath):
            raise ConfigFileMissingException()
        self.raw_parser = ConfigParser.RawConfigParser()
        self.raw_parser.read('config/cxDocs.cfg')
        self.log = log
        # Create the routes dictionary so we can use the nav module
        if self.raw_parser.has_section('Parser'):
            nav.create_dict(self.raw_parser.options('Parser'))
        else:
            self.warn_no_parser()

    def warn_no_parser(self):
        print "Config file has no [Parser] section; Cannot load rules documents."
        print "Have you tried running the generate_config.py helper script?"
        print "See config/README.md for more help configuring your parser."
        self.log.warn("Parser Section not configured; cannot load rules documents on index page.")
        self.log.warn("Maybe run the generate_config.py helper script? Maybe read config/README.md for help configuring parser?")

    def has_section(self, section):
        return self.raw_parser.has_section(section)

    def has_option(self, section, option):
        return self.raw_parser.has_option(section, option)

    def get(self, section, option):
        return self.raw_parser.get(section, option)

    def auth_config_map(self, unpw_tuple):
        returnMe = {"username":unpw_tuple[0],
            "password":unpw_tuple[1]}
        if self.has_section("Auth"):
            if self.has_option("Auth", "port"):
                returnMe['port'] = self.get('Auth', 'port')
            if self.has_option("Auth", "db_name"):
                returnMe['name'] = self.get('Auth', 'db_name')
            if self.has_option("Auth", "host"):
                returnMe['host'] = self.get('Auth', 'host')
            if self.has_option("Auth", "max_tries"):
                returnMe["max_tries"] = self.get("Auth", "max_tries")
            if self.has_option("Auth", "max_tries_minutes"):
                returnMe['max_tries_minutes'] = self.get("Auth", "max_tries_minutes")
        return returnMe

class ConfigFileMissingException(CXException):
    LOG_MESSAGE = "ERROR!: The config file is missing! Run $python \
        generate_config.py ?"

    def __init__(self):
        self.message = self.LOG_MESSAGE

    def log(self):
        log.warn(LOG_MESSAGE)

    def printToConsole(self):
        print(self.message)

    # we inherit the flash method being a pass; we can't flash if we don't have the config to boot the app.

class ConfigOptionMissingException(CXException):
    LOG_MESSAGE = "ERROR!: Someone is trying to log in, but cxDocs wasn't started \
        with login configured. Missing the %s parameter."
    ADVICE = """If you'd like to enable login, you'll need to set up your postgres user database 
    then run: $python start.py -u databaseUsername -p databasePassword 
    Use $python start.py -h for more help. And check cxDocs.log for more helpful error messages."""

    def __init__(self, missingOption):
        self.message = self.LOG_MESSAGE % missingOption

    def printToConsole(self):
        print(self.message)
        print(self.ADVICE)

    def log(self):
        log.warn(self.message)
        log.info(self.ADVICE)

    def flash(self):
        flash("Sorry, It looks like the admin hasn't set the login database up yet. Check logs?")