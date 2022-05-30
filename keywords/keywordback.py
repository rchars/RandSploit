import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__(self, 'BACK')

	def complete(self):
		return ''
	
	def execute(self):
		# tu powinien byc modul specjalny
		# czyli to co jest zawsze odpalane
		# na poczatku skryptu
		state.globals.ACTIVE_MODULE = None
