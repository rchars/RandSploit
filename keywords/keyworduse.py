import interfaces.keywordinterface
import state.globals
import importlib
import sys


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('USE')

	def complete(self):
		def action(mod):
			print(f'{mod.name}')
		self.__process_module(action)

	def execute(self):
		def action(mod):
			state.globals.ACTIVE_MODULE = mod
		self.__process_module(action)

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
	
	# THERE
	def __process_module(self, action):
		search_locations = (state.globals.MODULES_PATH, state.globals.USER_MODULES_PATH)
		location_index = 0
		while location_index < 2:
			for mod_path in search_locations[location_index].iterdir():
				if mod_path.name.startswith('_'): 
					continue
				restult = self.__validate_modules(mod_path)
				if result:
					action(result)
					return None
			else:
				location_index += 1
