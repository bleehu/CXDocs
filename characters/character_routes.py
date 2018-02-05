import characters
import characters_common
import pdb
import security
from flask import Blueprint, render_template, request, redirect, session, escape, flash

character_blueprint = Blueprint('character_blueprint', __name__, template_folder='templates')

global log

def initialize_characters(config, newlog):
    characters_common.set_config(config)
    global log
    log = newlog

@character_blueprint.route("/character/new", methods=['POST'])
def make_new_character():
    if not security.check_auth(session):
        flash("You must be signed in to make a new character!")
        return redirect("/")
    user = session['displayname']
    new_character = characters.validate_character(request.form, user)
    if new_character is False:
        flash("Could not add new character; Character was invalid.")
        return redirect("/character/create")
    #TODO: Insert new character
    flash("Created a new character!")
    return redirect("/character/create")

@character_blueprint.route("/character/create")
def show_character_creator():
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    return render_template("character_creator.html") #NOTE! Template does not exist yet!
    #Template to be written by Wildlovelies on 2/4/2018

@character_blueprint.route("/show/character/<pk_id>")
def show_char_select(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    pdb.set_trace()
    pc = characters.get_character(pk_id)
    if 'character' in session.keys():
        pc = characters.get_character(pk_id)
    return render_template('characterviewer.html', session=session, pc=pc)

@character_blueprint.route("/playercharacters")
def show_player_characters():
    #SELECT name, level, race, class, users.displayname FROM characters JOIN users ON characters.owner_fk = users.pk ORDER BY displayname, level, name;
    pcs = characters.get_characters()
    return render_template("player_characters.html", pcs = pcs)
    
@character_blueprint.route("/select/character", methods=['POST'])
def char_select():
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    character_blob = character.get_characters()
    select_pk = int(request.form['pk'])
    for player_character in character_blob['characters']:
        if player_character.pk == select_pk:
            session['character'] = str(player_character)
    return redirect("/show/character")

@character_blueprint.route("/modify/character/<pk>")
def char_modify(pk):
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    to_mod = None
    char_blob = character.get_characters()
    if int(pk) not in char_blob['pk_list']:
        return redirect("/show/character")
    for pc in char_blob['characters']:
        if pc.pk == int(pk):
            to_mod = pc
            return render_template("character_modify.html", session=session, character=to_mod)
