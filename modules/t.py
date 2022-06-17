import interfaces.moduleinterface


class Module(interfaces.moduleinterface.ModuleInterface):
	def __init__(self):
		super().__init__('test')
	
	def execute(self):
		pass