
import ConfigParser
from flask import Flask, render_template, request, redirect, session, escape, flash
import os
import pdb
import security
from start import hello, borked_it, missed_it, get_args

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # 1024 bytes x 1024 is a MB. Prevents people from uploading 40 GB pictures
app.config.from_object(__name__)

@app.route("/")
def welcome():
    return hello()




# the main method. This is where the calling starts.
if __name__ == "__main__":
    host = "localhost" #default to local only when running.
    
    global config
    config = ConfigParser.RawConfigParser()
    config.read('config/cxDocs.cfg')
    
    args = get_args()
    if args.i:  # if given a -i ip.ip.ip.address, open that on LAN, so friends can visit your site.
        host = args.i
    local_dir = os.path.dirname(__file__) #get local directory, so we know where we are saving files.
    
    app.secret_key = '$En3K9lEj8GK!*v9VtqJ' #todo: generate this dynamically
    
    app.run(host = host, threaded=True)