from operator import mod
import interfaces.moduleinterface


class Module(interfaces.moduleinterface.ModuleInterface):
	def __init__(self):
		super().__init__('AYEKARAMBA')

	def execute(self):
		pass