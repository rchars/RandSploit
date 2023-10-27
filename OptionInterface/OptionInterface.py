class OptionInterface:
	def __init__(self, name, descr, value, required):
		self.name = name
		self.descr = descr
		# self._value = value
		self.value = value
		self.required = required

	# @property
	# def value(self):
	# 	return self._value
	
	# @value.setter
	# def set_value(self, new_value):
	# 	self.value = new_value