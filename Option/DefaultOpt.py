import OptionInterface.OptionInterface as oi


class Opt(oi.OptionInterface):
	def __init__(self, name, value='', descr='', required=True):
		super().__init__(name, descr, value, required)
