class Gate:
	def __init__(self, value=False, name=''):
		self._name = name
		self._value = value

	def __bool__(self): return self._value
	
	def __repr__(self):
		if self._value: return 'on'
		return 'off'
	
	def toggle(self): self._value = not self._value

	@property
	def value(self): return self._value

	@value.setter
	def value(self, new_value):
		if type(new_value) != bool:
			raise ValueError(f'new_value must be a bool')
		self._value = new_value

	@property
	def name(self): return self._name