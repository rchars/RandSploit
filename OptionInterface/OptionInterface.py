class OptionInterface:
	def __init__(self, name, descr='', value='', required=False):
		self.name = name
		self.descr = descr
		self.value = value
		self.required = required

	def set_value(self, new_value):
		self.value = new_value
