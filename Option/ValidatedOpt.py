import OptionInterface.OptionInterface as oi


class Opt(oi.OptionInterface):
	def __init__(self, name, value='', descr='', required=True, validator=str, *args, **kwargs):
		if not callable(validator):
			raise TypeError('Validator must be callable')
		self.validator = validator
		self._value = value
		super().__init__(name, descr, self._value, required, *args, **kwargs)

	@property
	def value(self): return self._value

	@value.setter
	def value(self, new_value):
		if new_value == '':
			self._value = ''
		else:
			self._value = self.validator(new_value)
