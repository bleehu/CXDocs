import character
import character_database
import feats
import skills
from ..security import security
from ..cxExceptions import cxExceptions
import pdb
from flask import Blueprint, render_template, request, redirect, session, escape, flash

character_blueprint = Blueprint('character_blueprint', __name__, template_folder='templates')

global log

def initialize_characters(config, newlog):
    app.character_db = character_database.character_database(config)
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
    users_pk_id = security.get_user_pkid(session)
    new_character = app.character_db.create_blank_character(users_pk_id)
    new_character_id = new_character.pk_id
    #go to edit new character
    return redirect("/modifycharacter/%s" % new_character_id)

""" Attempt to show the user all of their characters.
    if the user isn't logged in, then we reroute them to the index page.
    if there's an error loading their characters, we provide feedback of the 
        error and reroute to the index page
    if the user doesn't have any characters, we reroute them to the character
        creation page
    if the user has characters and is logged in, we show the characters page. """
@character_blueprint.route("/character/mine")
def show_my_characters():
    if not security.check_auth(session):
        flash("You must be signed in to see your characters.")
        return redirect("/")
    users_pk_id = security.get_user_pkid(session)
    my_characters = None
    try:
        my_characters = app.character_db.get_users_characters(users_pk_id)
    except cxException as e:
        e.provideFeedback()
        return redirect("/")
    if (len(my_characters) < 1):
        flash("You don't have any characters yet. Would you like to make one?")
        return redirect("/character/new")
    return render_template("characters/character_select.html", characters=my_characters)

"""Attempt to show the character with the passed id.
    if the user is not logged in, reroutes to index
    if the user does not own the character...?
    if there is a cxError, provides feedback and routes to index."""
@character_blueprint.route("/showcharacter/<int:pk_id>")
def show_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    try:
        pc = characters.get_character(pk_id)
    except cxException as e:
        e.provideFeedback()
        return redirect("/")
    return render_template('characters/characterviewer.html', session=session, pc=pc)

""" Delete Character endpoint  """
@character_blueprint.route("/character/modify/<int:pk_id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def REST_character(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to delete a character!")
        return redirect("/")
    try:
        if request.method == "GET":
            return get_character(pk_id)
        elif request.method == "POST":
            return update_character(pk_id, request)
        elif request.method == "PUT":
            return create_character()
        elif request.method == 'DELETE':
            return delete_character(pk_id)
    except cxException as e:
        e.provideFeedback()
        return redirect("/")

""" Show all player characters for community and display metadata to see if one
class is getting much more play than another. """
@character_blueprint.route("/playercharacters")
def show_player_characters():
    pcs = app.character_db.get_characters()
    return render_template("characters/player_characters.html", pcs = pcs)

""" Use the character creation page to update an existing character. """
@character_blueprint.route("/modifycharacter/<int:pk_id>")
def char_modify(pk_id):
    #check to make sure the user is logged in.
    if not security.check_auth(session):
        flash("You must be logged in to do that.")
        return redirect("/")
    #check to make sure the character exists
    my_character = app.character_db.get_character(pk_id)
    if my_character is None:
        flash("You cannot update a character that isn't yours!")
        return redirect("/")
    user_id = security.get_user_pkid(session)
    all_feats = feats.get_feats()
    #check to make sure the user updating the character actually owns that character.
    if my_character['owner'] != user_id:
        flash("You cannot modify a character that isn't yours!")
        log.error("Intruder! %s attempted to update a character other than their own! un: %s IP: %s char_id: %s" \
            % (session['displayname'], request.remote_addr, pk_id_int))
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
    character = app.character_db.get_character(skill['fk_owner_id'])
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


""" pk_id here is the pk_id of the skill to update. """
@character_blueprint.route("/skills/modify/<pk_id>", methods=['POST'])
def update_skill(pk_id):
    #check if the user is logged in
    if not security.check_auth(session):
        flash("You can't do that without logging in")
        return redirect("/")
    #check if what the user sent was actually an integer
    try:
        sani_skill_pk_id = int(pk_id)
    except:
        flash("There was an error figuring out which character to delete this skill from.")
        log.error("There was an error modifying skill from: %s skill pk_id." % pk_id)
        return redirect("/")
    #check if the integer they sent was a skill that exists
    skill = skills.get_skill(sani_skill_pk_id)
    if skill is None:
        flash("That skill doesn't seem to exist")
        log.warn("%s attempted to modify a skill that doesn't exist. skill id: %s" % (session['username'], pk_id))
        return redirect("/characters/mine")
    character = app.character_db.get_character(skill['fk_owner_id'])
    if character is None:
        flash("That Character doesn't seem to exist.")
        log.warn("%s attempted to modify a skill belonging to a character that \
            doesn't exist. Character id %s." % (session['username'], pk_id))
        return redirect("/characters/mine")
    #check if the integer they sent was a character that they own
    user_id = security.get_user_pkid(session)
    if user_id != character['owner']:
        flash("You don't own that character!")
        log.warn("%s attempted to modify a skill to a character that they don't \
            own! Character id: %s" % (session['username'], pk_id))
        return redirect("/")
    #looks good. Update that skill.
    new_skill_name = request.form['skillName']
    new_skill_points = int(request.form['skillPoints'])
    #we can ommit the owner here; update_skill() doesn't use it.
    newskill = {'pk_id':sani_skill_pk_id, 'name':new_skill_name, 'points':new_skill_points}
    result = skills.update_skill(newskill)
    if result is None:
        log.warn("There was an error updating skill with pk_id %s" % pk_id)
        flash("there was an error updating the skill")
    return redirect("/modifycharacter/%s" % character['pk_id'])

def update_character(pk_id, request):
    user_id = security.get_user_pkid(session)
    new_character = cx_character(request.form, user_id)
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

def delete_character(pk_id):
    user_id = security.get_user_pkid(session)
    deleted_character = app.character_db.get_character(pk_id_int)
    if user_id != deleted_character.owner_id:
        #todo: we should log this 
        flash("you cannot delete a character that's not yours!")
        return redirect("/show/character")
    app.character_db.delete_character(pk_id_int)
    flash("Deleted Character successfully.")
    return redirect("/character/mine")