import Interpreter.state as state


def execute():
	'''Unchoose the module.'''
	state.MOD_HANDLER.unset_mod()
