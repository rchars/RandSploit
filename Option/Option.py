import OptionInterface.OptionInterface as oi


class DefaultOpt(oi.OptionInterface):
	def __init__(self, name, value='', descr='', required=False):
		super().__init__(name, value, descr, required)


class ValidatedOpt(oi.OptionInterface):
	def __init__(self, name, value='', descr='', required=False, validator=str):
		if not callable(validator):
			raise TypeError('Validator must be callable')
		elif value:
			self._value = validator(value)
		else:
			self._value = ''
		self.validator = validator
		super().__init__(name, self._value, descr, required)

	@property
	def value(self):
		return self.validator(self._value)

	@value.setter
	def value(self, new_value):
		if new_value:
			self._value = self.validator(new_value)
		else:
			self._value = ''
