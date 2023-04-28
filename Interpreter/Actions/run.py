import Interpreter.StateUtils as su
import Interpreter.state as state


def execute(self):
	if state.ACTIVE_MOD is None:
		print('Select mod before executing')
	else:
		errors = ''
		for opt in su.iter_mod_opts_data(state.ACTIVE_MOD):
			if opt.required and opt.value == '':
				errors += f'\'{opt.name}\' is required\n'
		if errors:
			print(errors, end='')
			return None
		try:
			state.ACTIVE_MOD.run()
		except(KeyboardInterrupt, EOFError):
			print()
