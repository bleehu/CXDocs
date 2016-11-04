from flask import Flask, render_template
import pdb
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/levelup")
def levelUp():
	pdb.set_trace()
	levels = list(range(1,20))
	return render_template('levelup.html', levels=levels)

if __name__ == "__main__":
    app.run()