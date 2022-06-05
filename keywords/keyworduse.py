import interfaces.keywordinterface
import state.globals
import importlib


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('USE')
		self.__module_paths = (
			state.globals.USER_MODULES_PATH,
			state.globals.MODULES_PATH
		)
		self.__complete_buff = ''
		self.__exectue_buff = False
		
	def __get_inst(mod_path):
		try:
			mod = importlib.import_module(mod_path.resolve())
			mod_inst = mod.Module()
			mod.resgisters
			mod.execute
			mod.name
		except AttributeError as module_err:
			mod_inst = module_err
		finally:
			del sys.modules[mod_path.stem]
		return mod_inst
		
		
	def __iterate_sources(self, action):
		mod_counter = 0
		while mod_counter < 2:
			for mod_path in self.__module_paths[mod_counter].iterdir():
				if mod_path.name.startswith('_'):
					continue
				mod_inst = __get_inst(mod_path)
				action(mod_inst)
			else:
				mod_counter += 1
				
	def complete(self):
		def action(mod_inst):
			if type(mod_inst) == str:
				self.__complete_buff = ''
			elif mod_inst.startswith(state.globals.KEYWORD_CMD[0]):
				self.__complete_buff += f'{mod_inst.name} '
		self.__iterate_sources(action)
		return self.__complete_buff
		
		
	def execute(self):
		if state.globals.KEYWORD_CMD_LEN > 0:
			def action(mod_inst):
				if type(mod_inst) == str:
					print(mod_inst)
				else:
					if mod_inst.name == state.globals.KEYWORD_CMD[0]:
						state.globals.ACTIVE_MODULE = mod_inst
						self.__execute_buff = True
					else:
						self.__execute_buff = False
			self.__iterate_sources(action)
			if not self.__execute_buff:
				print(f'No such module as \'{state.globals.KEYWORD_CMD[0]}\'')
		else:
			print('Need module name')
