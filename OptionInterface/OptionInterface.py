class OptionInterface:
	def __init__(self, name, descr='', value=''):
		self.name = name
		self.descr = descr
		self.value = value

	def set_value(self, new_value):
		self.value = new_value
