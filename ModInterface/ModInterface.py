import pathlib
import abc


class ModInterface(abc.ABC):
	def __init__(self, mod_name='', mod_descr=''):
		if mod_name:
			self.mod_name = mod_name
		self.mod_descr = mod_descr

	@abc.abstractmethod
	def run(): pass
