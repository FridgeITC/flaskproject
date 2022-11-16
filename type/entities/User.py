class User(object):	
	def __init__(self, id, email):
		self.id = id
		self.email = email

	def __str__(self):
		return "User(id='%s')" % self.id