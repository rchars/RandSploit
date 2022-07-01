class Reg:
	def __init__(self, value, description, validator):
		self.description = description
		self.validator = validator
		self.value = value


class Table:
	def __init__(self):
		self.__regs = {}

	def add_reg(self, name, value='', description='', validator=None):
		err = ''
		if not name:
			err = 'Need a name'
		elif name in self.__regs.keys():
			err = f'Register with name \'{name}\' already exist'
		if err:
			raise ValueError(err)
		self.__regs[name] = Reg(value, description, validator)
	
	def update_reg(self, name, new_value=''):
		if self.__regs[name].validator:
			self.__regs[name].validator(new_value)
		self.__regs[name].value = new_value

	def get_reg(self, name):
		return self.__regs[name]
	
	def __iter__(self):
		self.__iter_regs = iter(self.__regs)
		return self
	
	def __next__(self):
		reg_name = next(self.__iter_regs)
		reg = self.__regs[reg_name]
		return (reg_name, reg.value, reg.description)


REGS = Table()


def clear_regs():
	global REGS
	REGS = Table()
