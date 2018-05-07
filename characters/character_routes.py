import characters
import characters_common
import pdb
import security
import pdb
from flask import Blueprint, render_template, request, redirect, session, escape, flash

character_blueprint = Blueprint('character_blueprint', __name__, template_folder='templates')

global log

def initialize_characters(config, newlog):
    characters_common.set_config(config)
    global log
    log = newlog

""" Load the web form to create a new character. """
#the character creation API endpoint
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
    pk_id = security.get_user_pkid(session)
    characters.insert_character(new_character, pk_id)
    flash("Created a new character!")
    return redirect("/character/create")

#show the character creation menu
@character_blueprint.route("/character/create")
def show_character_creator():
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    return render_template("character_creator.html")

""" Display a specific character without modifying it. """
@character_blueprint.route("/show/character")
def show_char_select():
    if 'username' not in session.keys():
    return render_template("character_creator.html") #NOTE! Template does not exist yet!
    #Template to be written by Wildlovelies on 2/4/2018

@character_blueprint.route("/showcharacter/<pk_id>")
def show_char_select(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    pc = characters.get_character(pk_id)
    if 'character' in session.keys():
        pc = characters.get_character(pk_id)
    return render_template('characterviewer.html', session=session, pc=pc)

""" Delete Character endpoint  """
@character_blueprint.route("/character/modify/<pk_id>", methods=['DELETE'])
def delete_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to delete a character!")
        return redirect("/")
    pk_id_int = -1
    try:
        pk_id_int = int(pk_id)
    except:
        flash("That's not a character id, stupid.")
        return redirect("/")
    user_id = security.get_user_pkid(session)
    deleted_character = characters.get_character(pk_id_int)
    if user_id != deleted_character['owner']:
        flash("you cannot delete a character that's not yours!")
        return redirect("/show/character")
    characters.delete_character(pk_id_int)
    flash("Deleted Character successfully.")

""" Endpoint for updating an existing character. Attempting to emulate a 
RESTful API endpoint where the route is the same to add new, update existing,
delete existing or view existing character. """
@character_blueprint.route("/character/modify/<pk_id>", methods=['PUT'])
def update_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to update your character.")
        return redirect("/")
    pk_id_int = -1
    try:
        pk_id_int = int(pk_id)
    user_id = security.get_user_pkid(session)
    new_character = characters.validate_character(request.form, user)
    modified_character = characters.get_character(pk_id_int)
    if user_id != modified_character['owner']:
        flash("You cannot modify a character that's not yours!")
        return redirect("/show/character")
    characters.update_character(new_character,pk_id_int)
    flash("Successfully updated character.")

""" Show all player characters for community and display metadata to see if one 
class is getting much more play than another. """
#show all of the player characters. For game designers to get a feel for the distribution. 
@character_blueprint.route("/playercharacters")
def show_player_characters():
    #SELECT name, level, race, class, users.displayname FROM characters JOIN users ON characters.owner_fk = users.pk ORDER BY displayname, level, name;
    pcs = characters.get_characters()
    return render_template("player_characters.html", pcs = pcs)

""" If a User has more than one character, then they should be able to select one character that they are using at a time.
Dynamic pages will be able to do things like display only weapons and armor that character can use. """
#API endpoint to select a character
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

""" Use the character creation page to update an existing character. """
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
