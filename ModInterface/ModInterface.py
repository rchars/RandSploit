import abc


class ModInterface(abc.ABC):
	def __init__(self, mod_name, mod_descr=''):
		# scan for option objects (use vars)
		self.mod_name  = mod_name
		self.mod_descr = mod_descr

	abc.abstractmethod
	def run():
		pass