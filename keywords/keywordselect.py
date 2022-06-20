import interfaces.keywordinterface
import state.globals
import importlib.util


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('SELECT')

	def __get_inst(self, mod_path):
		spec = importlib.util.spec_from_file_location(mod_path.stem + '.Module', mod_path)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		return mod.Module()

	def complete(self):
		ret_list = []
		for mod_path in state.globals.MODULE_MANAGER:
			mod_inst = self.__get_inst(mod_path)
			try:
				if not state.globals.KEYWORD_CMD and mod_inst.name not in ret_list or mod_inst.name.upper().startswith(state.globals.KEYWORD_CMD[0]):
					ret_list.append(mod_inst.name)
			except AttributeError:
				continue
		return ret_list

	def execute(self):
		if state.globals.KEYWORD_CMD_LEN <= 0:
			raise ValueError('Need module name')
		req_module_name = state.globals.KEYWORD_CMD[0]
		for mod_path in state.globals.MODULE_MANAGER:
			try:
				mod_inst = self.__get_inst(mod_path)
			except AttributeError:
				continue
			except ImportError:
				continue
			if req_module_name == mod_inst.name:
				state.globals.ACTIVE_MODULE = mod_inst
				break
		else:
			raise ValueError(f'No module named \'{req_module_name}\'')
