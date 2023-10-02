import Interpreter.state as state
# import inspect


# def execute():
# 	if not state.ACTIVE_MOD: return
# 	module = inspect.getmodule(state.ACTIVE_MOD)


def execute():
	'''Reload the current module.'''
	if not state.MOD_HANDLER.is_mod_set(): return
	state.MOD_HANDLER.reload_current_mod()