import characters
import ConfigParser
#these imports are for python files we wrote ourselves.
import docs_parser #our custom plaintext parser for reading CX rules straight from the repo

from enemies.enemy_routes import enemy_blueprint, initialize_enemies
from characters.character_routes import character_blueprint, initialize_characters
from navigation import nav_dict as nav  # Module created by AK to allow dynamic front-end navigation

#flask is a python webserver built on Werkzeug. This is what is in charge of our
#main web app. It's how we respond to HTTP requests, etc.
from flask import Flask, render_template, make_response, request, redirect, session, escape, flash, abort

import guestbook #our custom guestbook for showing who all is on at once.
import json #sometimes we load or save things in json. This helps with that.
from mission import Mission #Mission is a custom data typ that we made to organize mission info on the backend.
import pdb  #Python Debuger is what I use to fix borked code. It should not be called in production EVER!
#but it's very helpful when being run locally.

import psycopg2 #psycopg2 lets us make posgres SQL calls from python. That lets us store things in databases
import os   #we need os to read and write files as well as to make our filepaths relative.
import logging #When we aren't running locally, we need the server to log what's happening so we can see any
#intrusions or help debug why it's breaking if it does so. This module handles that beautifully.
from auth.auth import AuthServer
from security import security #our custom code that handles common security tasks like SQL sanitization
import xml.etree.ElementTree #Sometimes we write or read things in XML. This does that well.
from werkzeug.utils import secure_filename
from cxExceptions import cxExceptions

def get_env_vars():
    username = os.environ.get('FLASK_USER')
    password = os.environ.get('FLASK_PASS')
    ip_address = os.environ.get('FLASK_IP')
    if not username and not password:
        print("Warning!!!")
        print("The login username/password has not been set.")
        print("Some site functionality will be limited.")
        print(" Try $export FLASK_USER=blah and $export FLASK_PASS=blah")
        #logging has not been configured at this point.
    if not ip_address:
        print("Warning!!! IP Address has not been set! This application will only be available on the local host!")
        print("Try $export FLASK_IP=##.##.##.##")
    return (username, password, ip_address)

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # 1024 bytes x 1024 is a MB. Prevents people from uploading 40 GB pictures
    app.config.from_object(__name__)
    #Flask supports a concept called "blueprints" which are like addons or plugins for your web application.
    #in this case, we are using blueprints to separate our enemy forge application and our character creator into separate files.
    #these two lines activate our character creator and enemy creator "plugins."
    app.register_blueprint(enemy_blueprint)
    app.register_blueprint(character_blueprint)

    #both flask and werkzeug (what flask is built on) output their information to a log called "log." by declaring it here,
    global log
    #we can use python's logging library to easily put more helpful information into the server log to help make our admin's
    #lives much easier.
    local_dir = os.path.dirname(__file__) #get local directory, so we know where we are saving files.
    log_filename = os.path.join(local_dir,"cxDocs.log") #save a log of web traffic in case something goes wrong.
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    log = logging.getLogger("cxDocs:")

    #whos_on is a list of tuples with displaynames and last-action timestamps that we use to show who's currently using this
    #web application. This helps for things like making sure we don't take the app down for maintainence while someone is working.
    global whos_on

    global config
    config = ConfigParser.RawConfigParser()
    config.read('config/cxDocs.cfg')

    # Create the routes dictionary so we can use the nav module
    if config.has_section('Parser'):
        nav.create_dict(config.options('Parser'))
    else:
        print "Config file has no [Parser] section; Cannot load rules documents."
        print "Have you tried running the generate_config.py helper script?"
        print "See config/README.md for more help configuring your parser."
        log.warn("Parser Section not configured; cannot load rules documents on index page.")
        log.warn("Maybe run the generate_config.py helper script? Maybe read config/README.md for help configuring parser?")

    """ CXDoc's main function is to display the rules of Compound X. This helper method uses our plain text parser
     to show rules documents in a way that is easy to read. Since its reading text, we can configure the app to read
     straight out of a local git repo, so updating all of the rules is as easy as running `$git pull` on the server.

    config_option: a string containing the name of the flag in the config/cxDocs.cfg file to look up the plain text
    file for. E.X. "Items_filepath". See config/README.md for more info.

     Returns the flask template of the rules page requested if configured correctly. If it detects an error, flashes
     an error message and redirects to the home page. """
    def parser_page(page):
        if nav.page_exists(page) and nav.page_has_filepath(page):
            rule_filepath = config.get('Parser', nav.get_filepath_for_endpoint(page))

            if not os.path.isfile(rule_filepath):
                log.error("Rule document missing: %s." % rule_filepath)
                log.error("Maybe check to see if cxDocs.cfg is configured correctly?")
                flash("That rule document is missing from the server. Please contact your administrator.")
                return redirect("/")
            #the cxdocs parser returns html-like list of tokens to display. This should be passed to the JINJA template below
            tokens = docs_parser.parse(rule_filepath)
            return render_template("utility/site/parser.html", elements = tokens, \
                navOptions = nav.generate_navbar_options_for_page(page))
        else:
            log.error("Missing config/cxDocs.cfg section Parser or missing option %s in that section." % config_option)
            flash("That feature isn't configured.")
            return redirect("/")

    """handles the display of the main page for the site. """
    @app.route('/') #tells flask what url to trigger this behavior for. In this case, the main page of the site.
    def hello():            #tells flask what method to use when you hit a particular route. Same as regular python function definition.
        session['X-CSRF'] = "foxtrot"   #set a session token. This helps prevent session takeover hacks.
        pc = None   #player character defaults to None if user isn't logged in.

        if 'character' in session.keys():   #if player is logged in and has picked a character, we load that character from the session string
            pc = characters.get_character(session['character'])
        gb = guestbook.get_guestbook()
        return render_template('home.html', \
            session = session, \
            character = pc, \
            navOptions = nav.generate_navbar_options_for_page('/'), \
            navLists = nav.generate_nav_lists_for_page('/'), \
            guestbook = gb) #the flask method render_template() shows a jinja template
        #jinja templates are kept in the /templates/ directory. Save them as .html files, but secretly, they use jinja to generate web pages
        #dynamically.

    """ The /whoshere endpoint shows a .json blob of how many users are logged into the site. This is called by the javascript from repo/static/whoshere.js
        to show the guestbook.  """
    @app.route("/whoshere")
    def whosHereAPI():
        gbook = json.dumps(guestbook.get_guestbook())
        return gbook

    # General route structure and method for displaying rules and related data/info
    @app.route('/rules/')
    @app.route('/gm/')
    @app.route('/items/')
    @app.route('/<topic>')
    @app.route('/<topic>/<subtopic>')
    def rules_pages(topic=None, subtopic=None):
        endpoint = '/' + (topic or request.path[1:])

        if subtopic != None:
            endpoint += '/' + subtopic

        # Checks route for appropriate template to use: parser, unique, home, or error if doesn't exist
        if nav.page_has_filepath(endpoint) == True:
            return parser_page(endpoint)
        elif nav.page_has_template(endpoint) == True:
            return render_template(nav.get_template_for_endpoint(endpoint), navOptions = nav.generate_navbar_options_for_page(endpoint))
        elif nav.page_exists(endpoint) == True:
            return render_template('home.html', navOptions = nav.generate_navbar_options_for_page(endpoint))
        else:
            abort(404)

    @app.route("/docs/trees")
    def docs_skill_trees():
        return render_template("skills/skilltrees.html")

    @app.route("/files")
    def show_files():
        return render_template("utility/game/files.html")

    @app.route("/missions")
    def show_missions():
        missions = get_missions()
        return render_template("missions/missions.html", missions = missions)

    @app.route("/missionfiles")
    def show_mission_files():
        return render_template("missions/mission_files.html")

    """ the /login route expects the POST request from the login form in the repo/templates/index.html file. It expects
        strings from the "uname" and "password" fields.

        If the login information is correct, it signs the guestbook and adds the user's username, displayname
        and role to flask's session object. Then it returns to the index/login page, which should now show the user as
        logged in.

        If the login info isn't correct,
        or has been tampered with, then it logs the attempt and redirects back to the index/login page. """
    @app.route("/login", methods=['POST'])
    def login():
        form = request.form
        uname = escape(form['uname'])
        passwerd = escape(form['password'])
        if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
            session.pop('X-CSRF', None)
        else:
            resp = make_response(render_template("errors/501.html"), 403)
            log.error("An attacker removed their CSRF token! uname:%s, pass:%s, user_agent:%s, remoteIP:%s" \
                % (uname, passwerd, request.user_agent.string, request.remote_addr))
            return resp
        try:
            user = app.authServer.login(uname, passwerd, request)
        except cxExceptions.CXException as exception:
            exception.provideFeedback()
            return redirect("/")
        session['username'] = user.username
        session['displayname'] = user.displayname
        session['role'] = user.role
        guestbook.sign_guestbook(user.displayname)
        return redirect("/")

    """ Logs the user out. Doesn't terminate the session, only empties the session of its info. """
    @app.route("/logout", methods=['POST'])
    def logout():
        form = request.form
        if 'X-CSRF' in form.keys() and form['X-CSRF'] == session['X-CSRF']:
            app.authServer.logout(session)
        return redirect("/")

    @app.route("/npcgen", methods=['GET'])
    def npcgen():
        return render_template("utility/game/npcgen.html")

    """Most legitimate web scrapers check a text file in /robots.txt to see
        where they should be allowed to look. This is how google, bing and bindu
        catalogue pages available to search. By default, we tell these robots to
        leave us alone."""
    @app.route('/robots.txt')
    def roblocker():
        return "User-agent: *\nDisallow: /"

    @app.route("/gamelogs")
    def gamelogs():
        return render_template("gamelogs.html")

    """ set generic handlers for common errors."""
    @app.errorhandler(500) #an HTTP 500 is given when there's a server error, for instance if  there's a Nonetype error in python.
    def borked_it(error):
        uname = "Anonymous"
        if 'username' in session.keys():
            uname = session['username']
        log.error("%s got a 500 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
        return render_template("errors/501.html", error=error)

    @app.errorhandler(404) # an HTTP 404 Not Found happens if the user searches for a url which doesn't exist. like /fuzzyunicorns
    def missed_it(error):
        uname = "Anonymous"
        if 'username' in session.keys():
            uname = session['username']
        log.warn("%s got a 404 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
        return render_template("errors/404.html", error=error)

    host = "localhost" #default to local only when running.

    seconds_away = 60
    seconds_out = 3600
    if config.has_option('WhosHere', 'Seconds_away'):
        seconds_away = config.get('WhosHere', 'Seconds_away')
    if config.has_option('WhosHere', 'Seconds_out'):
        seconds_out = config.get('WhosHere', 'Seconds_out')
    guestbook.initialize(seconds_away, seconds_out)

    initialize_enemies(config, log)
    initialize_characters(config, log)
    cxExceptions.initialize(log)
    (username, password, host) = get_env_vars()
    app.config['username'] = username
    app.config['password'] = password
    app.config['ip_address'] = host

    security.initialize(username, password, log)
    authConfigMap = auth_config_seam((username, password),config)
    app.authServer = AuthServer(authConfigMap, log)

    app.secret_key = '$En3K9lEj8GK!*v9VtqJ' #todo: generate this dynamically

    return app

"""This is ugly code.

    In a subsequent cleaning pull, I'm going to abstract and DRY out our
    configuration process so that we only rely on the 3rd party ConfigParser
    in one file. This pull is only for eliminating None returns..."""
def auth_config_seam(unpw_tuple, config):
    returnMe = {"username":unpw_tuple[0],
        "password":unpw_tuple[1]}
    if config.has_section("auth"):
        if config.has_option("auth", "port"):
            returnMe['port'] = config.get('auth', 'port')
        if config.has_option("auth", "db_name"):
            returnMe['name'] = config.get('auth', 'db_name')
        if config.has_option("auth", "host"):
            returnMe['host'] = config.get('auth', 'host')
    return returnMe

if __name__ == "__main__":

    app = create_app

    app.run(host = host, threaded=True)
