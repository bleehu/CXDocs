import characters_common
import security
from flask import Blueprint, render_template, request, redirect, session, escape, flash

character_blueprint = Blueprint('character_blueprint', __name__, template_folder='templates')

global log

def initialize_characters(config, newlog):
    characters_common.set_config(config)
    global log
    log = newlog

