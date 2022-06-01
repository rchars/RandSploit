import interfaces.keywordinterface
import sys


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('EXIT')

	def complete(self):
		return ''

	def execute(self):
		sys.exit()