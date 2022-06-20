import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('BACK')

	def complete(self):
		return []
	
	def execute(self):
		state.globals.ACTIVE_MODULE = None
