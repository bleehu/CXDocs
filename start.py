from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/levelup")
def levelUp():
	return render_template('static/levelup.html', entries=entries)

if __name__ == "__main__":
    app.run()