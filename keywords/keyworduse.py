import interfaces.keywordinterface
import state.globals
import importlib
import sys


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__(self, 'USE')

	def complete(self):
		def action(mod):
			print(f'{mod.name}')
		self.__proces_module(action)

	def execute(self):
		def action(mod):
			state.globals.ACTIVE_MODULE = mod
		self.__proces_module(action)

	def __validate_modules(self, mod_path):
		mod = importlib.import_module(mod_path.name, mod_path.parent)
		try:
			mod_instance = mod.Module()
			mod_instance.registers
			mod_instance.name
			buff = mod_instance
			del sys.modules[mod_instance.name]
			return buff
		except AttributeError:
			print(f'Module \'{mod.name}\' is invalid')
			return False
	
	def __proces_module(self, action):
		for mod_path in state.globals.MODULES_PATH:
			result = self.__validate_modules(mod_path)
			if not result:
				continue
			action(result)