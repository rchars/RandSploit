from abc import ABC, abstractmethod


class __RegisterData:
	def __init__(self, value='', description='', validator=None):
		self.value = value
		self.description = description
		self.validator = validator

class RegisterManager:
	__data = {}

	def add_register(self, name, **optional):
		if not name:
			raise ValueError('Need a name')
		elif name in self.__data.keys():
			raise ValueError(f'Register with name \'{name}\' already exist')
		self.__data[name] = __RegisterData(optional)
	
	def update_value(self, name, new_value):
		register = self.get_by_name(name)
		if callable(register.validator):
			register.validator(new_value)
		register.value = new_value

	def get_by_name(self, name):
		return self.__data[name]

class ModuleInterface(ABC):
	def __init__(self, name):
		self.name = name
		self.registers = RegisterManager()

	@abstractmethod
	def execute(self):
		pass