from flask import Flask, render_template
import pdb
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/levelup")
def levelUp():
	return render_template('levelup.html')

if __name__ == "__main__":
    app.run()