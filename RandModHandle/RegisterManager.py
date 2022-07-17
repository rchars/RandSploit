import itertools


class RegisterManagerWrapper:
	def __init__(self, register_manager):
		self.register_manager = register_manager

	def __iter__(self):
		self.iter_this = itertools.chain([('Name', 'Value', 'Description')], self.register_manager)
		return self

	def __next__(self):
		return next(self.iter_this)