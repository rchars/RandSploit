import interfaces.keywordinterface
import importlib.machinery
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('USE')

	def __get_mod(self, mod_path):
		return importlib.machinery.SourceFileLoader(mod_path.name, str(mod_path.absolute())).load_module()
	
	def __validate_module(self, mod):
		mod_inst = mod.Module()
		if not callable(mod_inst.execute) or type(mod_inst.registers) != dict or type(mod_inst.name) != str:
			raise TypeError
		return mod_inst
		
	def complete(self):
		matching_modules = []
		try:
			mod_name = state.globals.KEYWORD_CMD[0]
		except IndexError:
			mod_name = ''
		for mod_path in state.globals.MODULE_MANAGER:
			try:
				mod = self.__get_mod(mod_path)
				mod_inst = self.__validate_module(mod)
			except(TypeError, AttributeError, NameError):
				continue
			inst_name = mod_inst.name
			if inst_name.startswith(mod_name) and inst_name not in matching_modules:
				matching_modules.append(inst_name)
		return matching_modules
	
	def execute(self):
		def load_next_module(mod_name):
			state.globals.ACTIVE_MODULE_REGS = {}
			for mod_path in state.globals.MODULE_MANAGER:
				try:
					mod = self.__get_mod(mod_path)
					mod_inst = self.__validate_module(mod)
				except TypeError:
					continue
				if mod_inst.name == mod_name:
					state.globals.PROMPT_STR = f'[{mod_name}]{state.globals.DEFAULT_PROMPT_STR}'
					state.globals.ACTIVE_MODULE = mod_inst
					break
			else:
				raise ValueError(f'No such module as \'{mod_name}\'')
		
		if state.globals.KEYWORD_CMD_LEN < 1:
			raise ValueError('Need a module name')
		mod_name = state.globals.KEYWORD_CMD[0]
		try:
			try:
				current_mod_name = state.globals.ACTIVE_MODULE.name
			except AttributeError:
				load_next_module(mod_name)
			else:
				if current_mod_name != mod_name:
					load_next_module(mod_name)
		except Exception as module_load_err:
			return f'Cannot load module \'{mod_name}\': {module_load_err}'
		return ''