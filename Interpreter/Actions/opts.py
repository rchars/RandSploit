import Interpreter.StateUtils as su
import Interpreter.state as state
import tabulate


def execute():
	'''Get a list of all options for the chosen module.'''
	if not state.ACTIVE_MOD:
		print('Choose mod fist')
	else:
		print(
			tabulate.tabulate(
				su.iter_mod_opts_data(state.ACTIVE_MOD),
				headers=su.OPT_IFACE_PARAMS,
				tablefmt=state.TABLEFMT,
				showindex='never'
			)
		)
