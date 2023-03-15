class Option:
	def __init__(self, name, descr='', value='', validator=None):
		self.name = name
		self.descr = descr
		self.value = value
		self.validator = validator