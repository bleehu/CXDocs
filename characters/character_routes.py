import characters
import characters_common
import feats
import skills
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
@character_blueprint.route("/character/new", methods=['GET'])
def make_new_character():
    if not security.check_auth(session):
        flash("You must be signed in to make a new character!")
        return redirect("/")
    #get user's pk_id
    users_pk_id = security.get_user_pkid(session)
    #Create a new character
    characters.create_blank_character(users_pk_id)
    #get newest character
    new_character = characters.get_users_newest_character(session)
    new_character_id = new_character['pk_id']
    #go to edit new character
    return redirect("/modifycharacter/%s" % new_character_id)

""" Show the character management page """
@character_blueprint.route("/character/mine")
def show_my_characters():
    if not security.check_auth(session):
        flash("You must be signed in to see your characters.")
        return redirect("/")
    my_characters = characters.get_users_characters(session)
    if (len(my_characters) < 1):
        flash("You don't have any characters yet. Would you like to make one?")
        return redirect("/character/new")
    return render_template("character_select.html", characters=my_characters)

@character_blueprint.route("/showcharacter/<pk_id>")
def show_character(pk_id):
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
    return redirect("/character/mine")

""" Endpoint for updating an existing character. Attempting to emulate a 
RESTful API endpoint where the route is the same to add new, update existing,
delete existing or view existing character. """
@character_blueprint.route("/character/modify/<pk_id>", methods=['POST'])
def update_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to update your character.")
        return redirect("/")
    pk_id_int = -1
    try:
        pk_id_int = int(pk_id)
    except:
        flash("That's not a primary key!")
        return redirect("/")
    user_id = security.get_user_pkid(session)
    new_character = characters.validate_character(request.form, user_id)
    if not new_character:
        flash("Something is wrong with your character; we couldn't update it.")
        return redirect("/modified_character")
    modified_character = characters.get_character(pk_id_int)
    if user_id != modified_character['owner']:
        flash("You cannot modify a character that's not yours!")
        return redirect("/show/character")
    characters.update_character(new_character,pk_id_int)
    flash("Successfully updated character.")
    return redirect("/modifycharacter/%s" % pk_id)

""" Show all player characters for community and display metadata to see if one 
class is getting much more play than another. """
#show all of the player characters. For game designers to get a feel for the distribution. 
@character_blueprint.route("/playercharacters")
def show_player_characters():
    #SELECT name, level, race, class, users.displayname FROM characters JOIN users ON characters.owner_fk = users.pk ORDER BY displayname, level, name;
    pcs = characters.get_characters()
    return render_template("player_characters.html", pcs = pcs)

""" If a User has more than one character, then they should be able to select 
one character that they are using at a time. Dynamic pages will be able to do 
things like display only weapons and armor that character can use. """

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
@character_blueprint.route("/modifycharacter/<pk>")
def char_modify(pk):
    #check to make sure the user is logged in.
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    pk_id_int = -1
    #check to make sure the pk_id the user sent is actually an integer
    try:
        pk_id_int = int(pk)
    except:
        flash("That's not a character id, stupid.")
        log.error("User %s attempted to update a character using malicious id: %s" % (session['username'], pk))
        return redirect("/")
    #check to make sure the character exists
    my_character = characters.get_character(pk_id_int)
    if my_character is None:
        flash("You cannot update a character that isn't yours!")
        return redirect("/")
    my_character['feats'] = feats.get_characters_feats(my_character['pk_id'])
    my_character['skills'] = skills.get_characters_skills(my_character['pk_id'])
    user_id = security.get_user_pkid(session)
    all_feats = feats.get_feats()
    #check to make sure the user updating the character actually owns that character.
    if my_character['owner'] != user_id:
        flash("You cannot modify a character that isn't yours!")
        log.error("Intruder! %s attempted to update a character other than their own! un: %s IP: %s char_id: %s" \
            % (session['displayname'], request.remote_addr, pk_id_int))
        return redirect("/character/mine")
    return render_template("character_creator.html", character=my_character, feats=all_feats)

@character_blueprint.route("/assignCharacterFeat", methods=['POST'])
def make_character_feat_mapping():
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    mapping = feats.validate_character_feat_map(request.form)
    if not mapping:
        flash("New feat assignment failed. Could not give feat to character.")
        return redirect("/")
    feats.insert_character_feat_map(mapping)
    flash("Gave feat to character successfully!")
    return redirect("/modifycharacter/%s" % mapping['character_id'])

""" the pk_id here is the pk_id of the character for whom the new skill will go to. """
@character_blueprint.route("/skills/new/<pk_id>", methods=['POST'])
def make_new_skill(pk_id):
    #check if the user is logged in
    if not security.check_auth(session):
        flash("You can't do that without logging in")
        return redirect("/")
    #check if what the user sent was actually an integer
    try:
        sani_character_pk_id = int(pk_id)
    except:
        flash("There was an error figuring out which character to give this skill to.")
        log.error("There was an error giving a new skill to %s character pk_id." % pk_id)
        return redirect("/")
    #check if the integer they sent was a character that exists
    character = characters.get_character(sani_character_pk_id)
    if character is None:
        flash("That Character doesn't seem to exist.")
        log.warn("%s attempted to give a skill to a character that doesn't exist. Character id %s." % (session['username'], pk_id))
        return redirect("/characters/mine")
    #check if the integer they sent was a character that they own
    user_id = security.get_user_pkid(session)
    if user_id != character['owner']:
        flash("You don't own that character!")
        log.warn("%s attempted to give a skill to a character that they don't own! Character id: %s" % (session['username'], pk_id))
        return redirect("/")
    #looks good. make a new skill and send its ID back to 'em.
    new_skill_pk_id = skills.get_newest_skill(sani_character_pk_id)
    return "%s" % new_skill_pk_id

""" The pk_id here is for the skill that you wish to delete. Note that is a different 
    convention from the creation of a skill above. """
@character_blueprint.route("/skills/delete/<pk_id>", methods=['POST'])
def delete_skill():
    #check if the user is logged in
    if not security.check_auth(session):
        flash("You can't do that without logging in")
        return redirect("/")
    #check if what the user sent was actually an integer
    try:
        sani_skill_pk_id = int(pk_id)
    except:
        flash("There was an error figuring out which character to delete this skill from.")
        log.error("There was an error deleting skill from: %s character pk_id." % pk_id)
        return redirect("/")
    #check if the integer they sent was a skill that exists
    skill = skills.get_skill(sani_skill_pk_id)
    if skill is None:
        flash("That skill doesn't seem to exist")
        log.warn("%s attempted to delete a skill that doesn't exist. skill id: %s" % (session['username'], pk_id))
        return redirect("/characters/mine")
    character = characters.get_character(skill['fk_owner_id'])
    if character is None:
        flash("That Character doesn't seem to exist.")
        log.warn("%s attempted to delete a skill to a character that doesn't exist. Character id %s." % (session['username'], pk_id))
        return redirect("/characters/mine")
    #check if the integer they sent was a character that they own
    user_id = security.get_user_pkid(session)
    if user_id != character['owner']:
        flash("You don't own that character!")
        log.warn("%s attempted to delete a skill to a character that they don't own! Character id: %s" % (session['username'], pk_id))
        return redirect("/")
    #looks good. delete that skill.
    skills.delete_skill(sani_skill_pk_id)
    return redirect("/modifycharacter/%s" % character['pk_id'])
