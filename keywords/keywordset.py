import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('SET')

	def complete(self):
		if not state.globals.ACTIVE_MODULE:
			raise ValueError('Need a module')
		
	def execute(self):
		pass
