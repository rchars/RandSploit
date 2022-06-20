import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('EXIT')

	def complete(self):
		return []

	def execute(self):
		state.globals.EXIT_SCRIPT = True
