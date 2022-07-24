import importlib.machinery


class ModulePathManager:
	def __init__(self, *modules_paths):
		self.modules_paths = modules_paths
		self.paths_len = len(self.modules_paths)
	
	def __iter__(self):
		self.index = 0
		self.current_path = self.modules_paths[0].iterdir()
		return self
	
	def __next__(self):
		ret_mod = None
		while not ret_mod:
			try:
				mod_path = next(self.current_path)
				if not mod_path.name.startswith('_') and mod_path.is_file():
					try:
						mod = self.__get_mod_inst(mod_path)
						self.__validate_mod(mod)
					except Exception:
						continue
					ret_mod = mod
			except StopIteration:
				self.index += 1
				if self.index >= self.paths_len:
					raise StopIteration
				self.current_path = self.modules_paths[self.index].iterdir()
		return ret_mod
	
	def __validate_mod(self, mod):
		if type(mod.NAME) is not str or not type(mod.DESCRIPTION):
			raise TypeError
		elif not callable(mod.run):
			raise TypeError
		elif not callable(mod.load_registers):
			raise TypeError
	
	def __get_mod_inst(self, mod_path):
		return importlib.machinery.SourceFileLoader(mod_path.stem, str(mod_path.resolve())).load_module()
	
	def get_mod(self, mod_name):
		mod_index = 1
		for mod_dir in self.modules_paths:
			for possible_mod in mod_dir.iterdir():
				try:
					if not possible_mod.is_file() or possible_mod.name.startswith('_'):
						continue
					mod = self.__get_mod_inst(possible_mod)
					self.__validate_mod(mod)
					if mod.NAME == mod_name or mod_name == str(mod_index):
						return mod
				except Exception:
					continue
				else:
					mod_index += 1
		else:
			raise ValueError(f'\'{mod_name}\' not found')


class TableWrapper:
	def __init__(self, module_path_manager):
		self.module_path_manager = module_path_manager
	
	def __iter__(self):
		self.mod_index = 0
		self.iter_manager = iter(self.module_path_manager)
		return self
	
	def __next__(self):
		# cheap
		if self.mod_index == 0:
			row = ('^', 'Name', 'Description')
		else:
			mod = next(self.iter_manager)
			row = (self.mod_index, mod.NAME, mod.DESCRIPTION)
		self.mod_index += 1
		return row
