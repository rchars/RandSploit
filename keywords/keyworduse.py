import interfaces.keywordinterface
import state.globals
import importlib


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('USE')
		self.__module_paths = (
			state.globals.USER_MODULES_PATH,
			state.globals.MODULES_PATH
		)

	def complete(self):
		pass

	def execute(self):
		pass