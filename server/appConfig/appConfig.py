from ..cxExceptions import cxExceptions
import ConfigParser
from ..navigation import nav_dict as nav  # Module created by AK to allow dynamic front-end navigation

def get_app_config(filepath, log):
    return app_config_object(filepath, log)

class app_config_object:

    def __init__(self, config_abs_filepath, log):
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
        if self.has_section("auth"):
            if self.has_option("auth", "port"):
                returnMe['port'] = self.get('auth', 'port')
            if self.has_option("auth", "db_name"):
                returnMe['name'] = self.get('auth', 'db_name')
            if self.has_option("auth", "host"):
                returnMe['host'] = self.get('auth', 'host')
        return returnMe