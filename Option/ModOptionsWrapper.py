import Option.Option


class ModOptionsWrapper:
	def __init__(self, mod_inst):
		# to zadziała na 100
		self.mod_inst = mod_inst
		self.mod_opts = list()
		for obj in vars(self.mod_inst).values():
			if not isinstance(obj, Option.Option):
				continue
			self.mod_opts.append(obj)

	def __getitem__(self, opt_name):
		for opt in self.mod_opts:
			if opt.name == opt_name:
				return opt
		else:
			raise ValueError(f'No such option as \'{opt_name}\'')

	def __setitem__(self, opt_name, new_value):
		opt = self.__getitem__(opt_name)
		if callable(opt.validator):
			new_value = opt.validator(new_value)
		opt.value = new_value
