import interfaces.moduleinterface


class Module(interfaces.moduleinterface.ModuleInterface):
	def __init__(self):
		super().__init_('corrupted')
		self.add_reg('reg_name', 'the disaster', 'fucking ugly code is not working')

	def execute(self):
		print('{} -- nowy register'.format(self.get_reg('reg_name')))