import importlib.machinery
import pathlib


class ModPathManager:
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
		self.mod_path_manager = ModPathManager(mod_locations)
		self.active_mod = None

	def use_mod(self, mod_id):
		mod_path = self.mod_path_manager[mod_id]
		mod_inst = importlib.machinery.SourceFileLoader(mod_path.stem, path=str(mod_path.resolve().parent / pathlib.Path('mods')))
		# self.validate_mod(mod_inst)
		self.active_mod = mod_inst

	def unroll_mod(self):
		self.active_mod = None
		
	# use aganist active_mod
	def run_mod(self):
		pass
	
	# use aganist active_mod
	def get_mod_opts(self):
		pass

	# kwargs is dict opt_name=new_value
	def set_mod_opts(self, **kwargs):
		pass

	def iter_mods(self):
		return self.mod_path_manager