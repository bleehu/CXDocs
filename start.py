import csv
from flask import Flask, render_template
import pdb
app = Flask(__name__)
app.config.from_object(__name__)

def get_levels():
	levels = []
	with open('docs/levels.csv', 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for line in csv_reader:
			levels.append(line)
	return levels
	
def get_feats():
	with open("docs/feats.csv") as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',',quotechar='"')
		for line in csv_reader:
			feats.append(line)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/levelup")
def levelUp():
	levels = get_levels()
	return render_template('levelup.html', levels=levels)
	
@app.route("/guns")
def levelUp():
	return render_template('guns.html', guns=[])
	
@app.route("/armor")
def levelUp():
	levels = get_levels()
	return render_template('armor.html', armors=[])

	
@app.route("/feats")
def feats():
	feats = get_feats()
	return render_template("feats.html", feats=feats)

if __name__ == "__main__":
    app.run(host = "192.168.0.186")