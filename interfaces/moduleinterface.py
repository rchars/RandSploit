from abc import ABC, abstractmethod
import regiface


class ModuleInterface(ABC):
	def __init__(self, name):
		self.name = name
		self.registers = regiface.RegisterManager()

	@abstractmethod
	def execute(self):
		pass