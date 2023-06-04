import OptionInterface.OptionInterface as oi


class Opt(oi.OptionInterface):
	def __init__(self, name, value='', descr='', required=True, validator=str):
		if not callable(validator):
			raise TypeError('Validator must be callable')
		self.validator = validator
		self._value = value
		super().__init__(name, descr, self._value, required)

	@property
	def value(self):
		if self._value != '':
			return self.validator(self._value)
		return ''

	@value.setter
	def value(self, new_value):
		if new_value == '':
			self._value = ''
		else:
			self._value = self.validator(new_value)
