
class Mission():
	
	def __init__(self, pk, name, level, description):
		self.name = name
		self.level = level
		self.pk = pk
		self.description = description

	def __repr__(self):
		return '<Mission %r>' % self.name