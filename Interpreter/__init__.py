import OptionInterface.OptionInterface as option_iface
import importlib.machinery as machinery
import Interpreter.state
import collections
import itertools
import inspect
import pathlib


class State:
	def __init__(self):
		self._exit = False
		self._prompt = 'rand>'
		self._active_mod = None
		self._tablefmt = 'fancy_grid'
		self._mod_locations = [
			pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
		]
		self._action_dir = pathlib.Path(__file__).parent / pathlib.Path('Actions')
		self._ModTuple = collections.namedtuple('ModTuple', 'mod_index mod_path')

	def get_action(self, action_name):
		if pathlib.Path(action_name).is_file():
			self.get_module_by_path(action_name)

	def get_module_by_id(self, mod_id):
		try:
			mod_id = int(mod_id)
		except Exception:
			mod_id = pathlib.Path(mod_id)
		for mod_index, mod_path in self.iter_mods():
			if mod_index == mod_id or mod_path == mod_id:
				return self.get_module_by_path(mod_path)
		else:
			raise FileNotFoundError(f'No such module as \'{mod_id}\'')

	def get_module_by_path(self, mod_path):
		return machinery.SourceFileLoader(mod_path.name, str(mod_path)).load_module()

	def get_action_mod(self, action_mod_stem):
		return self.get_module_by_path(self._action_dir / pathlib.Path(f'{action_mod_stem}.py'))

	def is_mod_selected(self):
		if self._active_mod is None:
			return False
		return True

	def iter_mods(self):
		counter = 0
		for mod_dir in self._mod_locations:
			for mod_path in mod_dir.iterdir():
				yield self._ModTuple(counter, mod_path)
				counter += 1

	def iter_opts(self):
		if not is_mod_selected():
			raise RuntimeError('Module is not set')
		for member in inspect.getmembers(self._active_mod):
			if not isinstance(member[1], option_iface):
				continue
			yield member[1]

	def iter_actions(self):
		for action_mod in self._action_dir.iterdir():
			yield action_mod

	@property
	def prompt(self):
		return self._prompt

	@prompt.setter
	def prompt(self, new_prompt):
		if not self.is_mod_selected():
			self._prompt = 'rand>'
		else:
			self._prompt = new_prompt

	@property
	def active_mod(self):
		return self._active_mod

	@active_mod.setter
	def active_mod(self, mod):
		self._active_mod = mod.Mod()
		try:
			new_prompt = f'{self._active_mod.mod_name}>'
		except AttributeError:
			new_prompt = pathlib.Path(mod.__file__).stem + '>'
		self._prompt = new_prompt

	@property
	def exit(self):
		return self._exit

	@exit.setter
	def exit(self, exit):
		if type(exit) is not bool:
			raise TypeError('exit must be bool')
		self._exit = exit

	@property
	def tablefmt(self):
		return self._tablefmt


class ManagerInterface:
	@staticmethod
	def call_and_adapt_params(call_obj, arg):
		if len(inspect.signature(call_obj).parameters) >= 1:
			return call_obj(arg)
		return call_obj()


class ModManager(ManagerInterface):
	def __init__(self):
		self._mod_locations = [
			pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
		]
		self._active_mod = None
		self._opt_iface_params = list(inspect.signature(option_iface.OptionInterface).parameters.keys())
		# Join the params, in order to create positional arguments
		# self._opt_data = collections.namedtuple('OptData', ' '.join(self._opt_iface_params))
		self._opt_data = collections.namedtuple('OptData', self._opt_iface_params)
		# self._opt_data = tuple(inspect.signature(opt_iface.OptionInterface).parameters.keys())

	def __check_mod_active(self):
		if not self._active_mod:
			raise RuntimeError('Select module first')

	def get_opt(self, opt_name):
		self.__check_mod_active()
		for opt in self.iter_mods_opts:
			if opt.name == opt_name:
				return opt
		else:
			raise ValueError(f'No such opt as \'{opt_name}\'')

	# Ugly and duplicated
	def set_opt_value(self, opt_name, opt_value):
		self.__check_mod_active()
		for obj in vars(self._active_mod):
			if not isinstance(obj, option_iface.OptionInterface):
				continue
			if obj.name == opt_name:
				obj.value = opt_value
				break
		else:
			# repeats multiple times
			raise ValueError(f'No such opt as \'{opt_name}\'')

	def iter_mods_opts(self):
		self.__check_mod_active()
		use_fields = self._opt_data(self._opt_iface_params)
		for obj in vars(self._active_mod):
			if not isinstance(obj, option_iface.OptionInterface):
				continue
			# Not working, bad struct
			yield self._opt_data(vars(obj))

	def iter_mod_paths(self):
		for mod_dir in self._mod_locations:
			for mod_path in mod_dir.iterdir():
				if mod_path.is_file():
					yield mod_path

	def get_mod_inst_by_path(self, mod_path):
		for mod_dir in self._mod_locations:
			check_path = mod_dir / pathlib.Path(mod_path)
			if check_path.is_file():
				return machinery.SourceFileLoader(mod_path.name, str(mod_path)).load_module().Mod()
		else:
			raise FileNotFoundError('No such mod as \'{mod_path}\'')

	def get_mod_inst_by_index(self, index):
		mod_index = 0
		for mod_dir in self._mod_locations:
			for mod_path in mod_dir.iterdir():
				if not mod_path.is_file():
					continue
				elif mod_index == index:
					return machinery.SourceFileLoader(mod_path.name, str(mod_path)).load_module().Mod()
				mod_index += 1

	def call_mod_executor(self):
		self.__check_mod_active()
		return self._action_mod.run()

	@property
	def active_mod(self):
		return self._active_mod

	@active_mod.setter
	def active_mod(self, new_mod, index=True):
		if index:
			new_mod_inst = self.get_mod_inst_by_index(new_mod)
		else:
			new_mod_inst = self.get_mod_inst_by_path(new_mod)
		self._active_mod = new_mod_inst

	@property
	def opt_iface_params(self):
		return self._opt_iface_params


class ActionManager(ManagerInterface):
	def __init__(self):
		self._action_dir = pathlib.Path(__file__).parent / pathlib.Path('Actions')
		self._prompt = 'rand>'
		self._exit = False

	def call_action_completer(self, action_name):
		return self.get_action_inst(action_name).complete()

	def call_action_excecutor(self, action_name):
		return self.get_action_inst(action_name).execute()

	def find_action(self, action_name):
		action_file = self._action_dir / pathlib.Path(f'{action_name}.py')
		if action_file.is_file():
			return seif.get_action_inst(action_file)

	def get_action_mod(self, action_path):
		return machinery.SourceFileLoader(action_path.name, str(action_path))

	def get_action_inst(self, action_path):
		return machinery.SourceFileLoader(action_path.name, str(action_path)).Action()

	def iter_actions_names(self):
		for action_path in self._action_dir.iterdir():
			yield action_path.stem

	@property
	def prompt(self):
		return self._prompt

	@prompt.setter
	def prompt(self, new_prompt):
		self._prompt = new_prompt

	@property
	def exit(self):
		return self._exit

	@exit.setter
	def exit(self, new_state):
		if type(new_state) != bool:
			raise TypeError('new_state must be bool')
		self._exit = new_state


state.ACTION_STATE = ActionManager()
state.MOD_STATE = ModManager()
state.STATE = State()
