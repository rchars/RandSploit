import OptionInterface.OptionInterface as option_iface
import importlib.machinery as machinery
import Interpreter.state
import collections
import inspect
import pathlib


class State:
	def __init__(self):
		self._exit = False
		self._prompt = 'rand>'
		self._active_mod = None
		self._tabefmt = 'fancy_grid'
		# try to use property
		self._mod_locations = [
			pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
		]
		self._action_dir = pathlib.Path(__file__).parent / pathlib.Path('Actions')
		self._ModTuple = collections.namedtuple('ModTuple', 'mod_index mod_path')

	def get_action(self, action_name):
		if pathlib.Path(action_name).is_file():
			self.get_module_by_path(action_name)

	# method not optimized, need to refactor
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

	# ugly implementation, rewrite it on refactor branch
	def iter_mods(self):
		counter = 0
		for mod_dir in self._mod_locations:
			for mod_path in mod_dir.iterdir():
				yield self._ModTuple(counter, mod_path)
				counter += 1

	def iter_opts(self):
		if not is_mod_selected():
			# not sure if this is correct exception
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

	# @tablefmt.setter
	# def tablefmt(self, new_table):

state.STATE = State()
