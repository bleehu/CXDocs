#For more info on blueprints, http://flask.pocoo.org/docs/0.12/blueprints/#blueprints

import enemies
import enemy_abilities
import enemy_armor
import enemies_common
import enemy_routes
import enemy_weapons

import os

import security

from flask import Blueprint, render_template, request, redirect, session, escape, flash
#we use this to prevent nasty ../home/.bashrc overwrite attacks etc.
#only currently used in /newmonsterpic route
from werkzeug.utils import secure_filename 

enemy_blueprint = Blueprint('enemy_blueprint', __name__, template_folder='templates')

global log
global config

def initialize_enemies(newconfig, newlog):
    enemies_common.set_config(newconfig)
    global log
    log = newlog
    global config
    config = newconfig


@enemy_blueprint.route("/monster")
def show_monsters():
    if not security.check_auth(session):
        return redirect("/")
    munsters = enemies.get_monsters(session)
    return render_template("monsters.html", monsters = munsters, session=session)

@enemy_blueprint.route("/monsterstats")
def show_monsters_stats():
    if not security.check_auth(session):
        return redirect("/")
    munsters = enemies.get_monsters(session)
    abilities = enemy_abilities.get_monster_abilities_all()
    armor = enemy_armor.get_monster_armor_all()
    weapons = enemy_weapons.get_monster_weapons_all()
    stats = {"levelcount":{}, "noabilities":0, "noweapons":0, "noarmor":0, "hasnothingcount":0, "monsters":len(munsters), "private":0, "public":0}
    stats['armor'] = {'count':len(armor), 'contributors':{}}
    stats['weapons'] = {'count':len(weapons), 'contributors':{}}
    stats['abilities'] = {'count':len(abilities), 'contributors': {}}
    stats['contributors'] = {}
    stats['nakedMonsters'] = []
    stats['roles'] = {}
    for monster in munsters:
        hasAbs = True
        hasWep = True
        hasArm = True
        if len(monster['abilities']) == 0:
            stats['noabilities'] += 1
            hasAbs = False
        if len(monster['weapons']) == 0:
            stats['noweapons'] += 1
            hasWep = False
        if len(monster['armor']) == 0:
            stats['noarmor'] += 1
            hasArm = False
        if not (hasAbs or hasArm or hasWep):
            stats['hasnothingcount'] += 1
            stats['nakedMonsters'].append(monster)
        if monster['level'] not in stats['levelcount'].keys():
            stats['levelcount'][monster['level']] = 1
        else:
            stats['levelcount'][monster['level']] += 1
        if monster['author'] not in stats['contributors'].keys():
            stats['contributors'][monster['author']] = 1
        else:
            stats['contributors'][monster['author']] += 1
        if monster['role'] not in stats['roles'].keys():
            stats['roles'][monster['role']] = 1
        else:
            stats['roles'][monster['role']] += 1
        if monster['public'] == 't':
        	stats['public'] = 1 + stats['public']
        else:
        	stats['private'] = 1 + stats['private']
    stats['weapons']['types'] = {}
    for weapon in weapons:
          if weapon['type'] not in stats['weapons']['types'].keys():
            stats['weapons']['types'][weapon['type']] = 1
          else:
            stats['weapons']['types'][weapon['type']] += 1
          if weapon['author'] not in stats['weapons']['contributors'].keys():
            stats['weapons']['contributors'][weapon['author']] = 1
          else:
            stats['weapons']['contributors'][weapon['author']] += 1
    stats['abilities']['types'] = {}
    for ability in abilities:
        if ability['type'] not in stats['abilities']['types'].keys():
            stats['abilities']['types'][ability['type']] = 1
        else:
            stats['abilities']['types'][ability['type']] += 1
        if ability['author'] not in stats['abilities']['contributors'].keys():
            stats['abilities']['contributors'][ability['author']] = 1
        else:
            stats['abilities']['contributors'][ability['author']] += 1
    stats['armor']['types'] = {}
    for suit in armor:
          if suit['author'] not in stats['armor']['contributors'].keys():
            stats['armor']['contributors'][suit['author']] = 1
          else:
            stats['armor']['contributors'][suit['author']] += 1
          if suit['type'] not in stats['armor']['types'].keys():
            stats['armor']['types'][ suit['type']] = 1
          else:
            stats['armor']['types'][suit['type']] += 1
    return render_template("monster_meta.html", monsters=munsters, stats=stats, session=session)

@enemy_blueprint.route("/monstereditor")
def show_monster_editor():
    if not security.check_auth(session):
        return redirect("/")
    monsters = enemies.get_monsters(session)
    return render_template("monster_smith.html", session=session, monsters=monsters)

@enemy_blueprint.route("/monsterupdate/<pk_id>")
def show_monster_updater(pk_id):
    if not security.check_auth(session):
        return redirect("/")
    monsters = enemies.get_monsters(session)
    myMonster = None
    for monster in monsters:
        if monster['pk_id'] == int(pk_id):
            myMonster = monster
    if myMonster == None:
        flash('Could not find the enemy you wanted to update!')
        return redirect('monsters.html')
    return render_template("monster_update.html", session=session, monsters=monsters, pk_id=pk_id, myMonster=myMonster)
    
@enemy_blueprint.route("/monsterweaponupdate/<pk_id>")
def show_monster_weapon_updater(pk_id):
    if not security.check_auth(session):
        return redirect("/")
    monsters = enemies.get_monsters(session)
    weapons = enemy_weapons.get_monster_weapons_all()
    myWeapon = None
    for weapon in weapons:
        if weapon['pk_id'] == int(pk_id):
            myWeapon = weapon
    if myWeapon == None:
        flash("Could not find the weapon you wanted to update!")
        return redirect("/monstersweapons")
    return render_template("monster_weapon_update.html", session=session, monsters=monsters, weapons=weapons, pk_id=pk_id, myWeapon=myWeapon)

@enemy_blueprint.route("/monsterarmorupdate/<pk_id>")
def show_monster_armor_updater(pk_id):
    if not security.check_auth(session):
        return redirect("/")
    monsters = enemies.get_monsters(session)
    armors = enemy_armor.get_monster_armor_all()
    myArmor = None
    for armor in armors:
        if armor['pk_id'] == int(pk_id):
            myArmor = armor
    if myArmor == None:
        flash("Could not find the armor you wanted to update!")
        return redirect("/monstersarmors")
    return render_template("monster_armor_update.html", monsters=monsters, session=session, pk_id=pk_id, myArmor=myArmor, armors=armors)

@enemy_blueprint.route("/monsterabilityupdate/<pk_id>")
def show_monster_ability_updater(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to update abilities!")
        return redirect("/")
    monsters = enemies.get_monsters(session)
    abilities = enemy_abilities.get_monster_abilities_all()
    myAbility = None
    for ability in abilities:
        if ability['pk_id'] == int(pk_id):
            myAbility = ability
    if myAbility == None:
        flash("Could not find that ability!")
        return redirect("/monsterabilities")
    return render_template("monster_ability_update.html", monsters=monsters, session=session, pk_id=pk_id, myAbility=myAbility, abilities=abilities)

@enemy_blueprint.route("/monsterpic")
def show_monster_photographer():
    if not security.check_auth(session):
        flash("You must be signed in to do that!")
        log.warn("%s attempted to view monsterpic without logging in." % request.remote_addr)
        return redirect("/")
    monsters = enemies.get_monsters(session)
    return render_template("monster_photographer.html", monsters=monsters)

@enemy_blueprint.route("/newMonster", methods=['POST'])
def make_monster():
    if not security.check_auth(session):
        flash('Must be logged in to see this page')
        return redirect("/")
    user = session['displayname']
    monster = enemies.validate_monster(request.form, user)
    if not  monster:
        flash('Enemy invalid. Could not add')
        return redirect("/monstereditor")
    enemies.insert_monster(monster)
    log.info('User %s created monster: %s.', user, monster['name'])
    flash('Enemy added!')
    return redirect("/monstereditor")

@enemy_blueprint.route("/updateMonster/<pk_id>", methods=['POST'])
def update_monster(pk_id):
    if not security.check_auth(session):
        flash('must be logged in to see this page')
        return redirect('/')
    user = session['displayname']
    monster = enemies.validate_monster(request.form, user)
    if not monster:
        flash("Enemy invalid. Could not add.")
        return redirect("/monsterupdate/%s" % pk_id)
    enemies.update_monster(monster, pk_id)  
    log.info('User %s updated monster: %s.', user, monster['name'])
    flash("Enemy updated!")
    return redirect("/monster")
        
@enemy_blueprint.route("/updateMonsterWeapon/<pk_id>", methods=['POST'])
def update_monster_weapon(pk_id):
    if not security.check_auth(session):
        flash("Must be logged in to see this page.")
        return redirect("/")
    user = session['displayname']
    weapon = enemy_weapons.validate_monster_weapon(request.form, user)
    if not weapon:
        flash("Could not update weapon. Invalid input?")
        return redirect("/monsterweaponupdate/%s" % pk_id)
    enemies.update_monster_weapon(weapon, pk_id)
    log.info('User %s updated enemy weapon: %s.', user, weapon['name'])
    flash("Successfully updated enemy weapon!")
    return redirect("/monsterweapons")

@enemy_blueprint.route("/updateMonsterArmor/<pk_id>", methods=['POST'])
def update_monster_armor(pk_id):
    if not security.check_auth(session):
        flash("Must be logged in to do this.")
        return redirect("/")
    user = session['displayname']
    armor = enemy_armor.validate_monster_armor(request.form, user)
    if not armor:
        flash("Could not update Armor. Invalid input?")
        return redirect("monsterarmorupdate/%s" % pk_id)
    enemy_armor.update_monster_armor(armor, pk_id)
    log.info('User %s updated enemy Armor: %s', user, armor['name'])
    flash("Successfully updated enemy Armor!")
    return redirect("/monsterarmor")

@enemy_blueprint.route("/updateMonsterAbility/<pk_id>", methods=['POST'])
def update_monster_ability(pk_id):
    if not security.check_auth(session):
        flash("Must be logged in to do that!")
        return redirect("/")
    user = session['displayname']
    ability = enemy_abilities.validate_monster_ability(request.form, user)
    if not ability:
        flash("Could not update ability. Invalid input?")
        return redirect("monsterabilityupdate/%s" % pk_id)
    enemy_abilities.update_monster_ability(ability, pk_id)
    log.info('User %s updated enemy Ability: %s', user, ability['name'])
    flash("Successfully updated enemy Ability!")
    return redirect("/monsterabilities")

@enemy_blueprint.route("/newMonsterpic", methods=['POST'])
def make_monster_pic():
    if not security.check_auth(session):
        flash('You must be logged in to do that. This incident has been logged.')
        return redirect('/')
    user = session['displayname']
    if not config.has_section('Enemies'):
        flash("The administrator has not configured the Bestiary on this server.")
        log.warn("The Enemies Section has not been configured in /config/cxDocs.config")
        return redirect("/")
    if not config.has_option('Enemies','pics_file_path'):
        flash("The administrator has not configured the bestiary profile picture directory option.")
        log.warn("The Enemies Section doesn't have the pics_file_path option set to a valid directory.")
        return redirect("/")
    try:
        monster_id = int(request.form['monster_id'])
    except:
        flash("Could not identify which enemy you wanted to update.")
        log.error("%s attempted to update an enemy with pk_id of %s" % (user, request.form['monster_id']))
        return redirect("/monsterpic")
    #currently hardcoded to only allow .png files
    allowed_filetypes = set(['png'])
    file = request.files['monster_pic']
    if file is None:
        flash('Please select a .png file for this enemy\'s profile picture.')
        log.warn("%s tried to update %s profile picture, but forgot to select a pic."\
            % (user, monster_id))
        return redirect("/monsterpic")
    filename = secure_filename(file.filename)
    if not ('.' in filename and filename.split('.')[1].lower() in allowed_filetypes):
        flash('invalid file. This incident has been logged.')
        log.warn("%s attempted to upload an invalid file; %s" % (user, filename))
        return redirect('/monsterpic')
    pic_directory = config.get('Enemies', 'pics_file_path')
    if not os.path.isdir(pic_directory):
        log.warn("%s is attempting to update a profile pic, but the configured \
            directory doesn't exist." % user)
        log.warn("... attempting to create %s to compensate." % pic_directory)
        try:
            os.mkdir(pic_directory)
        except Exception as e:
            flash("The administrator has misconfigured the profile picture feature.")
            log.error(str(e))
            return redirect("/")
    file.save(os.path.join(pic_directory,"%s.png" % monster_id))
    flash("Enemy profile pic updated successfully!")
    return redirect("/monsterpic")

@enemy_blueprint.route("/newMonsterAbility", methods = ['POST'])
def make_monster_ability():
    if not security.check_auth(session):
        flash("Must be logged in to do that.")
        return redirect("/")
    user = session['displayname']
    ability = enemy_abilities.validate_monster_ability(request.form, user)
    if not ability:
        flash("New ability not valid. Could not add.")
        return redirect("/monsterabilityeditor")
    enemy_abilities.insert_monster_ability(ability)
    log.info('User %s created enemy Ability: %s.', user, ability['name'])
    flash("Enemy Ability Added!")
    return redirect("/monsterabilityeditor")

@enemy_blueprint.route("/newMonsterWeapon", methods = ['POST'])
def make_monster_weapon():
    if not security.check_auth(session):
        flash("Must be logged in to do that. This incident will be logged.")
        return redirect("/")
    user = session['displayname']
    weapon = enemy_weapons.validate_monster_weapon(request.form, user)
    if not weapon:
        flash("New Weapon is invalid. Could not add.")
        return redirect("/monsterweaponeditor")
    enemy_weapons.insert_monster_weapon(weapon)
    log.info('User %s created enemy Weapon: %s.', user, weapon['name'])
    flash("Enemy Weapon Added to Armory!")
    return redirect("/monsterweaponeditor")

@enemy_blueprint.route("/newMonsterArmor", methods=['Post'])
def make_monster_armor():
    if not security.check_auth(session):
        flash("Must be logged in to do that. This incident willbe logged.")
        return redirect("/")
    user = session['displayname']
    armor = enemy_armor.validate_monster_armor(request.form, user)
    if not armor:
        flash("New Armor is invalid. Could not add.")
        return redirect("/monsterarmoreditor")
    enemy_armor.insert_monster_armor(armor)
    log.info('User %s created enemy Armor: %s', user, armor['name'])
    flash("Enemy Armor Added successfully!")
    return redirect("/monsterarmoreditor")

@enemy_blueprint.route("/assignMonsterAbility", methods=['POST'])
def make_monster_ability_mapping():
    if not security.check_auth(session):
        flash("Must be logged in to do that.")
        return redirect("/")
    mapping = enemy_abilities.validate_monster_ability_map(request.form)
    if not mapping:
        flash("New mapping not valid. Could not add.")
        return redirect("/monsterabilityeditor")
    enemy_abilities.insert_monster_ability_map(mapping)
    flash("Enemy Ability Assigned!")
    return redirect("/monsterabilityeditor")

@enemy_blueprint.route("/assignMonsterWeapon", methods=['POST'])
def make_monster_weapon_mapping():
    if not security.check_auth(session):
        flash("Must be logged in to do that.")
        return redirect("/")
    mapping = enemy_weapons.validate_monster_weapon_map(request.form)
    if not mapping:
        flash("New mapping not valid. Could not add.")
        return redirect("/")
    enemy_weapons.insert_monster_weapon_map(mapping)
    flash("Weapon Assigned to Enemy Successfully!")
    return redirect("/monsterweaponeditor")

@enemy_blueprint.route("/assignMonsterArmor", methods=['POST'])
def make_monster_armor_mapping():
    if not security.check_auth(session):
        flash("Must be logged in to do that.")
        return redirect("/")
    mapping = enemy_armor.validate_monster_armor_map(request.form)
    if not mapping:
        flash("New armor assignment invalid. Could not add.")
        return redirect("/")
    enemy_armor.insert_monster_armor_map(mapping)
    flash("Armor Assignment successful!")
    return redirect("/monsterarmoreditor")

@enemy_blueprint.route("/deletemonster/<pk_id>", methods=['POST'])
def delete_monster(pk_id):
    if not security.check_auth(session):
        flash("Must be logged in to do that. This incident has been reported.")
        return redirect("/")
    monster_id = None
    try:
        monster_id = int(pk_id)
    except Exception(e):
        flash("error parsing id of monster. This incident will be logged.")
        return redirect("/monstereditor")
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE monsters SET deleted_at=now() WHERE pk_id = %s;" % monster_id)
    myCursor.close()
    connection.commit()
    
    flash('Enemy deleted!')
    return redirect("/monstereditor")

@enemy_blueprint.route("/deletemonsterability/<pk_id>", methods=['POST'])
def delete_monster_ability(pk_id):
    if not security.check_auth(session):
        flash("Must be logged in to do that. This incident will be logged.")
        return redirect("/")
    monster_ability_id = None
    try: 
        monster_ability_id = int(pk_id)
    except Exception(e):
        flash("Error Parsing ID of monster. This incident will be logged.")
        return redirect("/")
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE monsters_abilities SET deleted_at=now() WHERE pk_id = %s;" % pk_id)
    myCursor.close()
    connection.commit()
    
    flash('ability Deleted')
    return redirect("/monsterabilityeditor")

@enemy_blueprint.route("/deletemonsterweapon/<pk_id>", methods=['POST'])
def delete_monster_weapon(pk_id):
    if not security.check_auth(session):
        flash("must be logged in to do that. This incident will be reported.")
        return redirect("/")
    monster_weapon_id = None
    try:
        monster_weapon_id = int(pk_id)
    except Exception(e):
        flash("error parsing ID of monster. This incident will be logged")
        return redirect("/")
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE monsters_weapons SET deleted_at=now() WHERE pk_id = %s;" % pk_id)
    myCursor.close()
    connection.commit()
    
    flash('weapon Deleted successfuly!')
    return redirect("/monsterweaponeditor")

@enemy_blueprint.route("/deletemonsterarmor/<pk_id>", methods=['POST'])
def delete_monster_armor(pk_id):
    if not security.check_auth(session):
        flash("You must be logged in to do that. This incident will be looged.")
        return redirect("/")
    monster_armor_id = None
    try: 
        monster_armor_id = int(pk_id)
    except:
        flash("error parsing ID of monster. This incident will be logged.")
        return redirect("/")
    connection = enemies_common.db_connection()
    myCursor = connection.cursor()
    myCursor.execute("UPDATE monsters_armors SET deleted_at=now() WHERE pk_id = %s;" % pk_id)
    myCursor.close()
    connection.commit()
    
    flash('armor Deleted successfuly!')
    return redirect("/monsterarmoreditor")

@enemy_blueprint.route("/deletemonsterabilitymap", methods=['post'])
def delete_monster_ability_map():
    if not security.check_auth(session):
        flash("You must be logged in to do that. This incident has been logged.")
        return redirect("/")
    flash("Ability taken away successfully")
    enemy_abilities.delete_monster_ability_map(request.form['pk_id'])
    return redirect("/monsterabilities")

@enemy_blueprint.route("/deletemonsterweaponmap", methods=['post'])
def delete_monster_weapon_map():
    if not security.check_auth(session):
        flash("You must be logged in to do that. This incident has been logged.")
        return redirect("/")
    flash("Weapon taken away successfully")
    enemy_weapons.delete_monster_weapon_map(request.form['pk_id'])
    return redirect("/monsterweapons")

@enemy_blueprint.route("/deletemonsterarmormap", methods=['post'])
def delete_monster_armor_map():
    if not security.check_auth(session):
        flash("You must be logged in to do that. This incident has been logged.")
        return redirect("/")
    flash("Armor taken away successfully")
    enemy_armor.delete_monster_armor_map(request.form['pk_id'])
    return redirect("/monsterarmor")

@enemy_blueprint.route("/monsterabilities")
def show_monster_abilities():
    if not security.check_auth(session):
        flash("You must be logged in to see that.")
        return redirect("/")
    mAbilities = enemy_abilities.get_monster_abilities_all()
    munsters = enemies.get_monsters(session)
    for ability in mAbilities:
        maps = enemy_abilities.get_abilitys_monsters(ability['pk_id'])
        ability['maps'] = maps
    return render_template("monster_abilities.html", abilities=mAbilities, monsters=munsters)

@enemy_blueprint.route("/monsterweapons")
def show_monster_weapons():
    if not security.check_auth(session):
        flash("you must be logged in to see that.")
        return redirect("/")
    mWeapons = enemy_weapons.get_monster_weapons_all()
    munsters = enemies.get_monsters(session)
    for weapon in mWeapons:
        maps = enemy_weapons.get_weapons_monsters(weapon['pk_id'])
        weapon['maps'] = maps
    return render_template("monster_weapons.html", weapons=mWeapons, monsters=munsters)

@enemy_blueprint.route("/monsterarmor")
def show_monster_armor():
    if not security.check_auth(session):
        flash("you must be logged in to see that")
        return redirect("/")
    mArmor = enemy_armor.get_monster_armor_all()
    munsters = enemies.get_monsters(session)
    for suit in mArmor:
        maps = enemy_armor.get_armors_monsters(suit['pk_id'])
        suit['maps'] = maps
    return render_template("monster_armor.html", armor=mArmor, monsters=munsters)

@enemy_blueprint.route("/monsterabilityeditor")
def show_monster_ability_editor():
    if not security.check_auth(session):
        flash("Must be logged in to do that.")
        return redirect("/")
    mAbilities = enemy_abilities.get_monster_abilities_all()
    munsters = enemies.get_monsters(session)
    return render_template("monster_ability_smith.html", session=session, abilities=mAbilities, monsters=munsters)

@enemy_blueprint.route("/monsterweaponeditor")
def show_monster_weapon_editor():
    if not security.check_auth(session):
        flash("must be logged in to see that.")
        return redirect("/")
    mWeps = enemy_weapons.get_monster_weapons_all()
    munsters = enemies.get_monsters(session)
    return render_template("monster_weapon_smith.html", session=session, weapons=mWeps, monsters=munsters)

@enemy_blueprint.route("/monsterarmoreditor")
def show_monster_armor_editor():
    if not security.check_auth(session):
        flash("you must be logged in to see that.")
        return redirect("/")
    mArmor = enemy_armor.get_monster_armor_all()
    munsters = enemies.get_monsters(session)
    return render_template("monster_armor_smith.html", session=session, armor=mArmor, monsters=munsters)