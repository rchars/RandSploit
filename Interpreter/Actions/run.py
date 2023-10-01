# import Interpreter.StateUtils as su
import Interpreter.state as state
import traceback


# def run_in_foreground():
# 	try:
# 		state.ACTIVE_MOD_PROC.run()
# 	except Exception as run_err:
# 		if state.DEV:
# 			traceback.print_exc()
# 		else:
# 			print(run_err)


# # Many problems
# def run_in_background():
# 	state.ACTIVE_MOD_PROC.bg = True
# 	state.BACKGROUND_MODS.append(state.ACTIVE_MOD_PROC)
# 	state.ACTIVE_MOD_PROC.start()
# 	su.reload_current_mod()


def run_in_background(): print('Not implemented')


def run_in_foreground():
	try:
		state.MOD_HANDLER.active_mod.run()
	except(Exception, KeyboardInterrupt) as run_err:
		if state.MOD_DEV.value:
			traceback.print_exc()
		else:
			print(run_err)


def execute(where=''):
	'''Run the chosen module.'''
	if not state.MOD_HANDLER.is_mod_set():
		print('Choose mod before executing')
		return
	where_to_execute = {
		'fg': run_in_foreground,
		'bg': run_in_background
	}
	if not where: where = 'fg'
	elif where not in where_to_execute.keys():
		print(
			f'Invalid option \'{where}\'\n',
			f'Execute in background: run bg\n',
			f'Execute in foreground: run fg\n',
			end=''
		)
		return
	errors = ''
	for opt in state.MOD_HANDLER.iter_mod_opts_data():
		if opt.required and opt.value == '':
			errors += f'\'{opt.name}\' is required\n'
	if errors:
		print(errors, end='')
		return
	where_to_execute[where]()


# def execute(where=''):
# 	'''Run the chosen module.'''
# 	if state.ACTIVE_MOD is None:
# 		print('Select mod before executing')
# 		return
# 	where_to_execute = {
# 		'fg': run_in_foreground,
# 		# 'bg': run_in_background
# 	}
# 	if not where:
# 		where = 'fg'
# 	elif where not in where_to_execute.keys():
# 		print(
# 			f'Invalid option \'{where}\'',
# 			f'Execute in background: run bg',
# 			f'Execute in foreground: run fg'
# 		)
# 		return
# 	errors = ''
# 	for opt in su.iter_mod_opts_data(state.ACTIVE_MOD):
# 		if opt.required and opt.value == '':
# 			errors += f'\'{opt.name}\' is required\n'
# 	if errors:
# 		print(errors, end='')
# 		return
# 	where_to_execute[where]()
