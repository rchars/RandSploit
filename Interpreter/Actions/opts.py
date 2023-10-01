# import Interpreter.StateUtils as su
import Interpreter.state as state
import tabulate


# def execute():
# 	'''Get a list of all options for the chosen module.'''
# 	if not state.ACTIVE_MOD:
# 		print('Choose mod fist')
# 	else:
# 		print(
# 			tabulate.tabulate(
# 				su.iter_mod_opts_data(state.ACTIVE_MOD),
# 				headers=su.OPT_IFACE_PARAMS,
# 				tablefmt=state.TABLEFMT,
# 				showindex='never'
# 			)
# 		)


def execute():
	'''Get a list of all options for the chosen module.'''
	if not state.MOD_HANDLER.is_mod_set():
		print('Choose mod fist')
		return
	print(
		tabulate.tabulate(
			state.MOD_HANDLER.iter_mod_opts_data(),
			headers=state.MOD_HANDLER.opt_iface_params,
			tablefmt=state.TABLEFMT,
			showindex='never'
		)
	)
