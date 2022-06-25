from abc import ABC, abstractmethod


class Register:
	def __init__(self, description, value, validator):
		self.description = description
		self.value = value
		self.validator = validator


# def write_reg_values(self, name, new_value):
# 	validator = state.globals.ACTIVE_MODULE_REGS[name].validator
# 	if validator:
# 		validator(new_value)
# 	state.globals.ACTIVE_MODULE_REGS[name] = new_value


class ModuleInterface(ABC):
	def __init__(self, name):
		self.registers = {}
		self.name = name
	
	@abstractmethod
	def execute(self):
		pass

	def add_reg(self, name, description='', value='', validator=None):
		self.registers[name] = Register(description, value, validator)

	def get_reg(self, name):
		return self.registers[name]