import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('REGISTERS')

	def complete(self):
		return []

	def execute(self):
		if not state.globals.ACTIVE_MODULE:
			return 'Select a module first'
		try:
			print('NAME VALUE DESCRIPTION')
			for reg_name, reg_object in state.globals.ACTIVE_MODULE.registers.items():
				print(f'{reg_name} {reg_object.value} {reg_object.description}')
		except Exception as corrupted_registers_err:
			return f'Module {state.globals.ACTIVE_MODULE.name} has corrupted registers'