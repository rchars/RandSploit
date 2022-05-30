import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__(self, 'SET')

	def complete(self):
		ret_str = ''
		if state.globals.KEYWORD_CMD_LEN == 0:
			for reg_info in state.globals.ACTIVE_MODULE.registers:
				ret_str += f'{reg_info[0]} '
		elif state.globals.KEYWORD_CMD_LEN == 1:
			for reg_info in state.globals.ACTIVE_MODULE.registers:
				if reg_info[0].startswith(globals.KEYWORD_CMD[1]):
					ret_str += f'{reg_info[0]} '
		return ret_str
			
	def execute(self):
		if state.globals.KEYWORD_CMD_LEN == 0:
			return 'Missing register name and value'
		reg_name = state.globals.KEYWORD_CMD[0]
		new_value = None
		if state.globals.KEYWORD_CMD_LEN == 1:
			new_value = ''
		elif state.globals.KEYWORD_CMD_LEN >= 2:
			new_value = state.globals.KEYWORD_CMD[1]
		# to moze podniesc wyjatek, jesli:
		# wartosc jest nie taka jak trzeba
		# validator nie zostal sklecony
		# poprawnie
		try:
			state.globals.ACTIVE_MODULE.set_new_value(reg_name, new_value)
		except Exception as validator_err:
			print(validator_err)