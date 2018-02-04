import characters
import characters_common
import security
from flask import Blueprint, render_template, request, redirect, session, escape, flash

character_blueprint = Blueprint('character_blueprint', __name__, template_folder='templates')

global log

def initialize_characters(config, newlog):
    characters_common.set_config(config)
    global log
    log = newlog

@character_blueprint.route("/show/character")
def show_char_select():
    if 'username' not in session.keys():
        return redirect("/")
    chars = characters.get_characters()
    pc = None
    if 'character' in session.keys():
        pc = characters.get_character(pk_id)
    return render_template('character_select.html', characters=chars, session=session, character=pc)

@character_blueprint.route("/playercharacters")
def show_player_characters():
    #SELECT name, level, race, class, users.displayname FROM characters JOIN users ON characters.owner_fk = users.pk ORDER BY displayname, level, name;
    pcs = characters.get_characters()
    return render_template("player_characters.html", pcs = pcs)
    
@character_blueprint.route("/select/character", methods=['POST'])
def char_select():
    if not security.check_auth(session):
        return redirect("/")
    character_blob = character.get_characters(session)
    select_pk = int(request.form['pk'])
    for player_character in character_blob['characters']:
        if player_character.pk == select_pk:
            session['character'] = str(player_character)
    return redirect("/show/character")

@character_blueprint.route("/modify/character/<pk>")
def char_modify(pk):
    if 'username' not in session.keys():
        return redirect("/")
    to_mod = None
    char_blob = character.get_characters(session)
    if int(pk) not in char_blob['pk_list']:
        return redirect("/show/character")
    for pc in char_blob['characters']:
        if pc.pk == int(pk):
            to_mod = pc
            return render_template("character_modify.html", session=session, character=to_mod)
