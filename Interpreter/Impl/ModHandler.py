import OptionInterface.OptionInterface as opt_iface
import importlib.machinery as mach
import importlib.util as iu
import collections as c
import inspect
import pathlib
import sys


class Handler:
	def __init__(self, locations: tuple, default_prompt='rand>') -> None:
		if len(locations) < 0: raise ValueError('List can not be empty')
		self._default_prompt = default_prompt
		self._prompt = self._default_prompt
		# self._active_session = None
		self._locations = locations
		self._active_mod_path = None
		self._active_mod = None
		# self._sessions = None
		self._opt_iface_params = list(inspect.signature(opt_iface.OptionInterface).parameters)
		self._opt_fields = c.namedtuple('opt_fields', self._opt_iface_params)

	def iter_mods(self):
		for dir_path in self._locations:
			if not dir_path.is_dir(): continue
			for mod_path in dir_path.iterdir():
				if not mod_path.is_file(): continue
				yield mod_path
		return

	def iter_mods_with_index(self): return enumerate(self.iter_mods())

	def iter_mod_opts(self):
		for obj in vars(self._active_mod).values():
			if isinstance(obj, opt_iface.OptionInterface):
				yield obj

	def iter_mod_opts_data(self):
		for obj in self.iter_mod_opts():
			fields = list()
			for param in self._opt_iface_params:
				fields.append(getattr(obj, param))
			yield self._opt_fields(*fields)

	def set_mod_opt(self, name, value):
		for opt in self.iter_mod_opts():
			if opt.name == name:
				opt.value = value
				break
		else: raise ValueError(f'No such option as \'{name}\'')
	
	# May need option saving too.
	def reload_current_mod(self):
		self._set_active_mod(self._active_mod_path)

	def set_mod_by_index(self, index):
		for mod_index, mod_path in self.iter_mods_with_index():
			if mod_index == index:
				self._set_active_mod(mod_path)
				break
		else:
			raise ValueError(f'No module has index \'{index}\' assigned')

	# Quicker way.
	def set_mod_by_path(self, path_str):
		for dir_path in self._locations:
			if not dir_path.is_dir(): continue
			check_path = dir_path / pathlib.Path(path_str)
			if check_path.is_file():
				self._set_active_mod(check_path)
				break
		else:
			raise FileNotFoundError(f'Path not found {path_str}')
	
	def unset_mod(self):
		self._active_mod = None
		self._active_mod_path = None
		self._prompt = self._default_prompt

	def is_mod_set(self):
		if self._active_mod: return True
		return False
	
	def _set_active_mod(self, mod_path):
		self._active_mod = self._get_mod_inst(mod_path)
		self._active_mod_path = mod_path
		self._prompt = self._active_mod_path.stem + '>'

	def _get_mod_inst(self, mod_path):
		relative_path = f'{mod_path.parent.name}.{mod_path.stem}'
		spec = mach.ModuleSpec(
			name=relative_path,
			loader=mach.SourceFileLoader(relative_path, str(mod_path)),
			origin=mod_path,
			is_package=False
		)
		mod = iu.module_from_spec(spec)
		spec.loader.exec_module(mod)
		sys.modules[relative_path] = mod
		return mod.Mod()
	
	@property
	def prompt(self): return self._prompt

	@property
	def active_mod(self): return self._active_mod

	@property
	def opt_iface_params(self): return self._opt_iface_params