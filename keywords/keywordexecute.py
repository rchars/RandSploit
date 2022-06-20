import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('EXECUTE')

	def complete(self):
		return []

	def execute(self):
		try:
			state.globals.ACTIVE_MODULE.execute()
		except AttributeError:
			print('Nothin to execute')
		except Exception as module_err:
			print(module_err)
