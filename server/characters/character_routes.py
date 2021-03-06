import characters
import characters_common
import feats
import json
import skills
import pdb
from ..security import security
import pdb
from flask import Blueprint, render_template, request, redirect, session, escape, flash

character_blueprint = Blueprint('character_blueprint', __name__, template_folder='templates')

global log

def initialize_characters(config, newlog):
    characters_common.set_config(config)
    skills.initialize_skills(newlog)
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
    return render_template("characters/character_select.html", characters=my_characters)

@character_blueprint.route("/showcharacter/<pk_id>")
def show_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    pc = characters.get_character(pk_id)
    if 'character' in session.keys():
        pc = characters.get_character(pk_id)
    return render_template('characters/characterviewer.html', session=session, pc=pc)

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
@character_blueprint.route("/character/modify/<int:pk_id>", methods=['POST'])
def update_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to update your character.")
        return redirect("/")
    user_id = security.get_user_pkid(session)
    new_character = characters.validate_character(request.form, user_id)
    if not new_character:
        flash("Something is wrong with your character; we couldn't update it.")
        return redirect("/modified_character")
    modified_character = characters.get_character(pk_id)
    if not owns_character(modified_character, session):
        return redirect("/")
    characters.update_character(new_character,pk_id)
    flash("Successfully updated character.")
    return redirect("/modifycharacter/%s" % pk_id)

""" Show all player characters for community and display metadata to see if one
class is getting much more play than another. """
#show all of the player characters. For game designers to get a feel for the distribution.
@character_blueprint.route("/playercharacters")
def show_player_characters():
    pcs = characters.get_characters()
    return render_template("characters/player_characters.html", pcs = pcs)

""" Use the character creation page to update an existing character. """
@character_blueprint.route("/modifycharacter/<int:pk>")
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
    all_feats = feats.get_feats()
    #check to make sure the user updating the character actually owns that character.
    if not owns_character(my_character, session):
        return redirect("/character/mine")
    return render_template("characters/character_creator.html", character=my_character, feats=all_feats)

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

@character_blueprint.route("/character_skills/<int:character_pk_id>", methods=['GET'])
def character_skills_endpoint(character_pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    my_character = characters.get_character(character_pk_id)
    if not owns_character(my_character, session):
        flash("You don't own that character")
        return redirect("/character/mine")
    my_characters_skills = skills.get_characters_skills(my_character['pk_id'])
    return json.dumps(my_characters_skills, indent=4, sort_keys=True, default=str)

@character_blueprint.route("/skill/<int:pk_id>", methods=['GET','POST', 'PUT', 'DELETE'])
def skill_REST(pk_id):
    #check if the user is logged in
    if not security.check_auth(session):
        flash("You can't do that without logging in")
        return redirect("/")
    #perform the appropriate operation on a skill
    if request.method == 'GET':
        return get_skill(pk_id)
    elif request.method == 'POST':
        return create_skill(pk_id)
    elif request.method == 'PUT':
        return update_skill(pk_id)
    elif request.method == 'DELETE':
        return delete_skill(pk_id)

def create_skill(pk_id):
    #check if the integer they sent was a character that exists
    character = characters.get_character(pk_id)
    if character is None:
        flash("That Character doesn't seem to exist.")
        log.warn("%s attempted to give a skill to a character that doesn't exist. \
            Character id %s." % (session['username'], pk_id))
        return redirect("/characters/mine")
    #check if the integer they sent was a character that they own
    user_id = security.get_user_pkid(session)
    if not owns_character(character, session):
        return redirect("/")
    #looks good. make a new skill and send its ID back to 'em.
    new_skill_pk_id = skills.get_newest_skill(pk_id)
    return str(new_skill_pk_id)

""" The pk_id here is for the skill that you wish to delete. Note that is a different
    convention from the creation of a skill above. """
def delete_skill(pk_id):
    #check if the integer they sent was a skill that exists
    skill = skills.get_skill(pk_id)
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
    if not owns_character(character, session):
        return redirect("/")
    #looks good. delete that skill.
    skills.delete_skill(pk_id)
    return "200 OK"


""" pk_id here is the pk_id of the skill to update. """
def update_skill(pk_id):
    #check if the integer they sent was a skill that exists
    skill = skills.get_skill(pk_id)
    if skill is None:
        flash("That skill doesn't seem to exist")
        log.warn("%s attempted to modify a skill that doesn't exist. skill id: %s" % (session['username'], pk_id))
        return redirect("/characters/mine")
    character = characters.get_character(skill['fk_owner_id'])
    if character is None:
        flash("That Character doesn't seem to exist.")
        log.warn("%s attempted to modify a skill belonging to a character that \
            doesn't exist. Character id %s." % (session['username'], pk_id))
        return redirect("/characters/mine")
    if not owns_character(character, session):
        return redirect("/")
    #looks good. Update that skill.
    new_skill_name = request.form['skillName']
    new_skill_points = int(request.form['skillPoints'])
    #we can ommit the owner here; update_skill() doesn't use it.
    newskill = {'pk_id':pk_id, 'name':new_skill_name, 'points':new_skill_points}
    result = skills.update_skill(newskill)
    if result is None:
        log.warn("There was an error updating skill with pk_id %s" % pk_id)
        flash("there was an error updating the skill")
    return redirect("/modifycharacter/%s" % character['pk_id'])

""" checks to see if the user owns the character who they're trying to modify"""
def owns_character(character, session):
    #check if the integer they sent was a character that they own
    user_id = security.get_user_pkid(session)
    if user_id != character['owner']:
        flash("You don't own that character!")
        log.warn("%s attempted to modify a character that they don't \
            own! Character id: %s" % (session['username'], pk_id))
        return False
    return True