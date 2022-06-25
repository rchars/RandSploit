import interfaces.keywordinterface
import state.globals


class Keyword(interfaces.keywordinterface.KeywordIface):
	def __init__(self):
		super().__init__('SET')

	def complete(self):
		match_reg = []
		try:
			match_str = state.globals.KEYWORD_CMD[0]
		except IndexError:
			match_str = ''
		for reg_name in state.globals.ACTIVE_MODULE.registers.keys():
			if reg_name.startswith(match_str):
				match_reg.append(reg_name)
		return match_reg

	def execute(self):
		if not state.globals.ACTIVE_MODULE:
			return 'Select a module, before you set a register'
		elif state.globals.KEYWORD_CMD_LEN == 0:
			return 'Register name is required'
		reg_name = state.globals.KEYWORD_CMD[0]
		passed_value = ''
		if state.globals.KEYWORD_CMD_LEN > 1:
			passed_value = ''.join(state.globals.KEYWORD_CMD[1:])
		try:
			validator = state.globals.ACTIVE_MODULE.registers[reg_name].validator
			if validator:
				validator(passed_value)
			state.globals.ACTIVE_MODULE.registers[reg_name].value = passed_value
		except KeyError:
			return f'No such register as \'{reg_name}\''
		return ''