import ModulePattern.OneModuleIface


class Module(ModulePattern.OneModuleIface.ModuleInterface):
	def __init__(self):
		super().__init__('NotCorrupted')
		self.add_reg('NotCorrupted', 'this code is a distaster', 'fuck')

	def execute(self):
		passed_val = self.get_reg('NotCorrupted')
		print(f'You passed -- {passed_val}')