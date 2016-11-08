import csv
from flask import Flask, render_template, request, redirect
import json
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
	feats = []
	with open("docs/feats.csv") as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',',quotechar='"')
		for line in csv_reader:
			feats.append(line)
	return feats
	
def get_guns():
	goons = None
	with open("docs/guns1.json") as gunfile:
		goons = json.loads(gunfile.read())
	return goons

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/levelup")
def levelUp():
	levels = get_levels()
	return render_template('levelup.html', levels=levels)
	
@app.route("/guns")
def guns():
	return render_template('guns.html', guns=[])
	
@app.route("/armor")
def armor():
	return render_template('armor.html', armors=[])

@app.route("/items")
def show_items():
	return render_template('items.html', items=[])

@app.route("/feats")
def show_feats():
	feats = get_feats()
	return render_template("feats.html", feats=feats)
	
@app.route("/weaponsmith")
def show_weaponsmith():
	guns = get_guns()
	return render_template("weaponsmith.html", guns=guns)

@app.route("/addgun", methods=['POST'])
def make_gun():
	gun = {}
	gun['name'] = request.form['gunname']
	gun['range'] = request.form['range']
	gun['damage'] = request.form['gunDamage']
	gun['type'] = request.form['gunType']
	gun['clip'] = request.form['clip']
	gun['toMiss'] = request.form['toMiss']
	gun['effect'] = request.form['effect']
	gun['cost'] = request.form['cost']
	guns = get_guns()
	guns.append(gun)
	json_string = json.dumps(guns)
	with open("docs/guns1.json", 'w') as gunfile:
		gunfile.write(json_string)
	return redirect("weaponsmith")

if __name__ == "__main__":
    app.run(host = "localhost")