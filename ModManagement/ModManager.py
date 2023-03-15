import Option.ModOptionsWrapper
import importlib.machinery
import pathlib


class __ModPathManager:
	def __init__(self, *mod_locations):
		self.locations = mod_locations
		self.using_index = None

	def __getitem__(self, mod_id):
		try:
			mod_id = int(mod_id)
		except ValueError:
			pass
		for location in self.locations:
			if not location.is_dir():
				raise FileNotFoundError('No such dir as \'{checking_path}\'')
			for mod_path, mod_index in enumerate(location.iterdir()):
				# Im not sure if mod_path should be casted to str
				if mod_index == mod_id or mod_id == str(mod_path):
					return mod_path
		else:
			raise FileNotFoundError('No such module as \'{mod}\'')

	def __iter__(self):
		self.current_location_index = 0
		self.current_location = iter(
			self.locations[
				self.current_location_index
			].iterdir()
		)
		return self

	def __next__(self):
		try:
			# return mod_path
			return next(self.current_location)
		except StopIteration:
			try:
				self.current_location_index += 1
				self.current_location = iter(
					self.locations[
						self.current_location_index
					]
				)
			except IndexError:
				raise StopIteration


class ModManager:
	def __init__(self, *mod_locations):
		self.mod_path_manager = __ModPathManager(mod_locations)
		self.active_mod = None

	def roll_mod(self, mod_id):
		mod_path = self.mod_path_manager[mod_id]
		mod_inst = importlib.machinery.SourceFileLoader(mod_path.stem, path=str(mod_path.resolve().parent / pathlib.Path('mods')))
		# self.validate_mod(mod_inst)
		self.active_mod = Option.ModOptionsWrapper.ModOptionsWrapper(mod_inst.Mod())
			
	def unroll_mod(self):
		self.active_mod = None
		
	# use aganist active_mod
	def run_mod(self):
		self.active_mod.mod_inst.run()
	
	# use aganist active_mod
	def iter_mod_opts(self):
		return iter(self.active_mod)

	def get_mod_opt(self, opt_name):
		return self.active_mod[opt_name]

	# kwargs is dict opt_name=new_value
	def set_mod_opt(self, opt_name, new_value):
		for opt in self.get_mod_opts():
			if opt.name == opt_name:
				if callable(opt.validator) == opt_name:
					if callable(opt.validator):
						opt.validator(new_value)
					opt.value = new_value
					break
		else:
			raise ValueError(f'No such opt as \'{opt_name}\'')

	def iter_mods(self):
		return iter(self.mod_path_manager)