import Interpreter.state as state


def execute():
	'''Unchoose the module.'''
	state.ACTIVE_MOD_PROC = None
	state.ACTIVE_MOD = None
	state.PROMPT = 'rand>'
