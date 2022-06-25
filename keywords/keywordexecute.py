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
			return 'Choose module first'
		except Exception as module_err:
			return f'Module {state.globals.ACTIVE_MODULE.name} exception: {module_err}'
		return ''