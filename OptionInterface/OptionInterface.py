class OptionInterface:
	def __init__(self, name, descr, value, required):
		self.name = name
		self.descr = descr
		self.value = value
		self.required = required
