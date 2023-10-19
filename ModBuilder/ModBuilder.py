import OptionInterface.OptionInterface as o
import ModInterface.ModInterface as m
import Interpreter.state as state
import importlib.machinery as my
import pathlib


class _AutoModProvider:
	def __init__(self, exc_ins, search_dir, inst_name=None):
		self.search_dir = search_dir
		self.exc_ins = exc_ins
		if inst_name:
			def inst_getter(mod_name, mod_path):
				return getattr(my.SourceFileLoader(mod_name, str(mod_path)).load_module(), inst_name)
		else:
			def inst_getter(mod_name, mod_path):
				return my.SourceFileLoader(mod_name, str(mod_path)).load_module()
		self.inst_getter = inst_getter

	def __getattr__(self, mod_name):
		mod_path = pathlib.Path(f'{self.search_dir}') / pathlib.Path(f'{mod_name}.py')
		if not mod_path.is_file(): raise FileNotFoundError(f'No such {self.exc_ins} as \'{mod_name}\'')
		return self.inst_getter(mod_name, mod_path)


ModIface = m.ModInterface
OptIface = o.OptionInterface

Util = _AutoModProvider('util', 'Util')
Opt = _AutoModProvider('opt', 'Option', inst_name='Opt')
OptTemplate = _AutoModProvider('template', 'OptionTemplate')

UserUtil = _AutoModProvider('util', str(state.USER_UTIL_DIR))
UserOpt = _AutoModProvider('opt', str(state.USER_MOD_DIR), inst_name='Opt')
UserOptTemplate = _AutoModProvider('template', str(state.USER_OPT_TEMPLATE_DIR))