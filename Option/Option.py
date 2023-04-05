import OptionInterface.OptionInterface as oi


class DefaultOpt(oi.OptionInterface):
	def __init__(self, name, value='', descr='', required=False):
		super().__init__(name, value, descr, required)


class ValidatedOpt(oi.OptionInterface):
	def __init__(self, name, value, descr, validator):
		if callable(validator):
			def set_value(new_value): validator(new_value)
			self.set_value = set_value
		super().__init__(name, value, descr)
