import characters
import ConfigParser
import csv #sometimes we save or read stuff in .csv format. This helps with that a lot.
#these imports are for python files we wrote ourselves. 
import docs_parser #our custom plaintext parser for reading CX rules straight from the repo

from enemies.enemy_routes import enemy_blueprint, initialize_enemies
from characters.character_routes import character_blueprint, initialize_characters

#flask is a python webserver built on Werkzeug. This is what is in charge of our 
#main web app. It's how we respond to HTTP requests, etc.
from flask import Flask, render_template, request, redirect, session, escape, flash

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
    #we can use python's logging library to easily put more helpful information into the server log to help make our admin's
    #lives much easier.
    global log
    #whos_on is a list of tuples with displaynames and last-action timestamps that we use to show who's currently using this
    #web application. This helps for things like making sure we don't take the app down for maintainence while someone is working.
    global whos_on

    """depricated. """
    def get_levels():
        levels = []
        with open('docs/levels.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line in csv_reader:
                levels.append(line)
        return levels

    """ depricated. Used to show dungeons that were actively being run."""
    def get_missions():
        connection = psycopg2.connect("dbname=mydb user=searcher password=allDatSQL")
        myCursor = connection.cursor()
        myCursor.execute("SELECT * FROM missions ORDER BY level;")
        missions = []
        results = myCursor.fetchall()
        for miss in results:
            pk = int(miss[0])
            name = miss[1]
            description = miss[2]
            level = int(miss[3])
            new_mission = Mission(pk, name, level, description)
            missions.append(new_mission)
        return missions

    """ CXDoc's main function is to display the rules of Compound X. This helper method uses our plain text parser
     to show rules documents in a way that is easy to read. Since its reading text, we can configure the app to read
     straight out of a local git repo, so updating all of the rules is as easy as running `$git pull` on the server.

    config_option: a string containing the name of the flag in the config/cxDocs.cfg file to look up the plain text
    file for. E.X. "Items_filepath". See config/README.md for more info.

     Returns the flask template of the rules page requested if configured correctly. If it detects an error, flashes
     an error message and redirects to the home page. """
    def parser_page(config_option):
        if config.has_section('Parser') and config.has_option('Parser', config_option):
            rule_filepath = config.get('Parser', config_option)
            if not os.path.isfile(rule_filepath):
                log.error("Rule document missing: %s." % rule_filepath)
                log.error("Maybe check to see if cxDocs.cfg is configured correctly?")
                flash("That rule document is missing from the server. Please contact your administrator.")
                return redirect("/")
            #the cxdocs parser returns html-like list of tokens to display. This should be passed to the JINJA template below
            tokens = docs_parser.parse(rule_filepath)
            return render_template("parser.html", elements = tokens)
        else:
            log.error("Missing config/cxDocs.cfg section Parser or missing option %s in that section." % config_option)
            flash("That feature isn't configured.")
            return redirect("/")

    """ reads the config document to build a list of names of rules documents and their filepath.

    returns a list of tuples, where the first field is the name of the document and the second is the
        filepath to the document. Assumed to be the rules for the game Compound X from github.bleehu/Compound_X"""
    def get_rules_docs():
            rulesDocs = []
            if config.has_option('Parser', 'basic_rules_filepath'):
                rulesDocs.append(('Basic Rules','/docs/basic'))

            if config.has_option('Parser', 'combat_rules_filepath'):
                rulesDocs.append(('Combat Rules','/docs/combat'))

            if config.has_option('Parser', 'damage_types_filepath'):
                rulesDocs.append(('Damage Types and Armors','/docs/damagetypes'))

            if config.has_option('Parser', 'conditions_filepath'):
                rulesDocs.append(('Conditions','/docs/conditions'))

            if config.has_option('Parser', 'level_up_filepath'):
                rulesDocs.append(('Level Up Rules', '/docs/levelup'))

            if config.has_option('Parser', 'cloaking_rules_filepath'):
                rulesDocs.append(('Cloaking Rules','/docs/cloaking'))

            if config.has_option('Parser', 'glossary_filepath'):
                rulesDocs.append(('Glossary of Terms','/docs/glossary'))

            if len(rulesDocs) < 1:
                log.warn("Looked for Rules documents, but didn't find any. See config/README.md to configure rules docs.")
                return None
            return rulesDocs

    def get_items_docs():
        itemsDocs = []
        if config.has_option('Parser', 'melee_weapons_filepath'):
            itemsDocs.append(('Melee Weapons','/docs/meleeWeapons'))

        if config.has_option('Parser', 'pistols_filepath'):
            itemsDocs.append(('Pistols','/docs/pistols'))

        if config.has_option('Parser', 'smgs_filepath'):
            itemsDocs.append(('Submachine Guns','/docs/smgs'))

        if config.has_option('Parser', 'carbines_filepath'):
            itemsDocs.append(('Carbines and Assault Rifles','/docs/carbines'))

        if config.has_option('Parser', 'long_rifles_filepath'):
            itemsDocs.append(('Long Rifles and DMRs','/docs/longRifles'))

        if config.has_option('Parser', 'machineguns_filepath'):
            itemsDocs.append(('Machine Guns and Rocket Launchers','/docs/machineguns'))

        if config.has_option('Parser', 'explosives_filepath'):
            itemsDocs.append(('Explosives', '/docs/explosives'))

        if config.has_option('Parser', 'weapon_attachments_filepath'):
            itemsDocs.append(('Weapon Attachments','/docs/weaponAttachments'))

        if config.has_option('Parser', 'armor_filepath'):
            itemsDocs.append(('Armor','/docs/armor'))

        if config.has_option('Parser', 'items_filepath'):
            itemsDocs.append(('Items','/docs/items'))

        if len(itemsDocs) < 1:
            log.warn("Looked for Item documents, but didn't find any. See config/README.md to configure rules docs.")
            return None
        return itemsDocs

    def get_character_docs():
        character_docs = []
        if config.has_option('Parser', 'new_player_walkthrough_filepath'):
            character_docs.append(('New Player Walkthrough','/docs/newplayer'))

        if config.has_option('Parser', 'races_filepath'):
            character_docs.append(('Races','/docs/races'))

        if config.has_option('Parser', 'classes_filepath'):
            character_docs.append(('Classes','/docs/classes'))

        if config.has_option('Parser', 'feats_filepath'):
            character_docs.append(('Feats','/docs/feats'))

        if config.has_option('Parser', 'skills_filepath'):
            character_docs.append(('Skill','/docs/skills'))

        if config.has_option('Parser', 'Engineer_filepath'):
            character_docs.append(('Engineer Processes','/docs/engineers'))

        if config.has_option('Parser', 'Medic_filepath'):
            character_docs.append(('Medic Procedures','/docs/medics'))
        if len(character_docs) < 1:
            log.warn("Looked for Character documents, but didn't find any. See config/README.md to configure rules docs.")
            return None
        return character_docs

    """handles the display of the main page for the site. """
    @app.route("/") #tells flask what url to trigger this behavior for. In this case, the main page of the site.
    def hello():            #tells flask what method to use when you hit a particular route. Same as regular python function definition.
        session['X-CSRF'] = "foxtrot"   #set a session token. This helps prevent session takeover hacks. 
        pc = None   #player character defaults to None if user isn't logged in.
        docs = None
        rulesDocs = None
        itemsDocs = None
        character_docs = None
        if config.has_section('Parser'):
            rulesDocs = get_rules_docs()
            itemsDocs =  get_items_docs()
            character_docs = get_character_docs()
        else:
            print "Config file has no [Parser] section; Cannot load rules documents."
            print "Have you tried running the generate_config.py helper script?"
            print "See config/README.md for more help configuring your parser."
            log.warn("Parser Section not configured; cannot load rules documents on index page.")
            log.warn("Maybe run the generate_config.py helper script? Maybe read config/README.md for help configuring parser?")

        if 'character' in session.keys():   #if player is logged in and has picked a character, we load that character from the session string
            pc = characters.get_character(session['character']) 
        gb = guestbook.get_guestbook()
        return render_template('index.html', \
            session=session, \
            character=pc, \
            rulesDocs=rulesDocs, \
            itemsDocs= itemsDocs, \
            character_docs=character_docs, \
            guestbook = gb) #the flask method render_template() shows a jinja template 
        #jinja templates are kept in the /templates/ directory. Save them as .html files, but secretly, they use jinja to generate web pages
        #dynamically. 

    """ The /whoshere endpoint shows a .json blob of how many users are logged into the site. This is called by the javascript from repo/static/whoshere.js
        to show the guestbook.  """
    @app.route("/whoshere")
    def whosHereAPI():
        gbook = json.dumps(guestbook.get_guestbook())
        return gbook

    #begin parser pages

    @app.route("/docs/classes")
    def docs_classes():
        return parser_page('classes_filepath')

    @app.route("/docs/races")
    def docs_races():
        return parser_page('races_filepath')

    @app.route("/docs/items")
    def docs_items():
        return parser_page('items_filepath')

    @app.route("/docs/feats")
    def docs_feats():
        return parser_page('feats_filepath')

    @app.route("/docs/levelup")
    def docs_levelup():
        return parser_page('level_up_filepath')

    @app.route("/docs/meleeWeapons")
    def docs_melee():
        return parser_page('melee_weapons_filepath')

    @app.route("/docs/pistols")
    def docs_pistols():
        return parser_page('pistols_filepath')

    @app.route("/docs/smgs")
    def docs_smgs():
        return parser_page('smgs_filepath')

    @app.route("/docs/carbines")
    def docs_carbines():
        return parser_page('carbines_filepath')

    @app.route("/docs/longRifles")
    def docs_long_rifles():
        return parser_page('long_rifles_filepath')

    @app.route("/docs/machineguns")
    def docs_machineguns():
        return parser_page('machineguns_filepath')

    @app.route("/docs/explosives")
    def docs_explosives():
        return parser_page('explosives_filepath')

    @app.route("/docs/weaponAttachments")
    def docs_wep_attachments():
        return parser_page('weapon_attachments_filepath')

    @app.route("/docs/armor")
    def docs_armor():
        return parser_page('armor_filepath')

    @app.route("/docs/skills")
    def docs_skills():
        return parser_page('skills_filepath')

    @app.route("/docs/basic")
    def docs_basic():
        return parser_page('basic_rules_filepath')

    @app.route("/docs/medics")
    def docs_medics():
        return parser_page('Medic_filepath')

    @app.route("/docs/engineers")
    def docs_engineers():
        return parser_page('Engineer_filepath')

    @app.route("/docs/combat")
    def docs_combat():
        return parser_page('combat_rules_filepath')

    @app.route("/docs/conditions")
    def docs_conditions():
        return parser_page('conditions_filepath')

    @app.route("/docs/damagetypes")
    def docs_damage():
        return parser_page('damage_types_filepath')

    @app.route("/docs/cloaking")
    def docs_cloaking():
        return parser_page('cloaking_rules_filepath')

    @app.route("/docs/glossary")
    def docs_glossary():
        return parser_page('glossary_filepath')

    @app.route("/docs/newplayer")
    def docs_new_walkthrough():
        return parser_page('new_player_walkthrough_filepath')

    #End parser pages

    @app.route("/docs/trees")
    def docs_skill_trees():
        return render_template("skilltrees.html")
        
    @app.route("/files")
    def show_files():
        return render_template("files.html")

    @app.route("/missions")
    def show_missions():
        missions = get_missions()
        return render_template("missions.html", missions = missions)
        
    @app.route("/missionfiles")
    def show_mission_files():
        return render_template("mission_files.html")

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
            resp = make_response(render_template("501.html"), 403)
            log.error("An attacker removed their CSRF token! uname:%s, pass:%s, user_agent:%s, remoteIP:%s" % (uname, passwerd, request.user_agent.string, request.remote_addr))
            return resp
        try:
            user = self.authServer.login(uname, passwerd, request.remote_addr)
        except cxExceptions.CxException as exception:
            exception.provideFeedback()
            return redirect("/")
        session['username'] = uname
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
        return render_template("npcgen.html")

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

    @app.route("/designhowto")
    def show_design_howto():
        return render_template("design_how_to.html")

    @app.route("/monsterweaponshowto")
    def show_monster_weapons_howto():
        return render_template("monster_weapon_how_to.html")

    @app.route("/monsterarmorhowto")
    def show_monster_armor_howto():
        return render_template("monster_armor_how_to.html")

    """ set generic handlers for common errors."""
    @app.errorhandler(500) #an HTTP 500 is given when there's a server error, for instance if  there's a Nonetype error in python. 
    def borked_it(error):
        uname = "Anonymous"
        if 'username' in session.keys():
            uname = session['username']
        log.error("%s got a 500 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
        return render_template("501.html", error=error)
        
    @app.errorhandler(404) # an HTTP 404 Not Found happens if the user searches for a url which doesn't exist. like /fuzzyunicorns
    def missed_it(error):
        uname = "Anonymous"
        if 'username' in session.keys():
            uname = session['username']
        log.warn("%s got a 404 looking for %s. User Agent: %s, remote IP: %s" % (uname, request.path, request.user_agent.string, request.remote_addr))
        return render_template("404.html", error=error)

    host = "localhost" #default to local only when running.
    
    global config
    config = ConfigParser.RawConfigParser()
    config.read('config/cxDocs.cfg')
    
    seconds_away = 60
    seconds_out = 3600
    if config.has_option('WhosHere', 'Seconds_away'):
        seconds_away = config.get('WhosHere', 'Seconds_away')
    if config.has_option('WhosHere', 'Seconds_out'):
        seconds_out = config.get('WhosHere', 'Seconds_out')
    guestbook.initialize(seconds_away, seconds_out)

    local_dir = os.path.dirname(__file__) #get local directory, so we know where we are saving files.
    log_filename = os.path.join(local_dir,"cxDocs.log") #save a log of web traffic in case something goes wrong.
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    global log
    log = logging.getLogger("cxDocs:")
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
