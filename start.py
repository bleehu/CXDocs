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

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/levelup")
def levelUp():
	levels = get_levels()
	return render_template('levelup.html', levels=levels)

if __name__ == "__main__":
    app.run()