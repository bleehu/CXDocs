from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://searcher:AllDatSQL@localhost/mydb'
db = SQLAlchemy(app)


class Mission(db.Model):
	pk = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	level = db.Column(db.Integer)
	description = db.Column(db.Text)
	
	def __init__(self, pk, name, level, description):
		self.name = name
		self.level = level
		self.pk = pk
		self.description = description

	def __repr__(self):
		return '<Mission %r>' % self.name