import Interpreter.state as state


def complete(text):
	if not state.MOD_HANDLER.is_mod_set(): return
	completions = list()
	for params in state.MOD_HANDLER.iter_mod_opts_data():
		if params.name.startswith(text):
			completions.append(params.name)
	return completions
