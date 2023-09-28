import Interpreter.StateUtils as su
import Interpreter.state as state
import traceback


def run_in_foreground():
	try:
		state.ACTIVE_MOD_PROC.run()
	except Exception as run_err:
		if state.DEV:
			traceback.print_exc()
		else:
			print(run_err)


# Many problems
def run_in_background():
	state.ACTIVE_MOD_PROC.bg = True
	state.BACKGROUND_MODS.append(state.ACTIVE_MOD_PROC)
	state.ACTIVE_MOD_PROC.start()
	su.reload_current_mod()


def execute(where=''):
	'''Run the chosen module.'''
	if state.ACTIVE_MOD is None:
		print('Select mod before executing')
		return
	where_to_execute = {
		'fg': run_in_foreground,
		# 'bg': run_in_background
	}
	if not where:
		where = 'fg'
	elif where not in where_to_execute.keys():
		print(
			f'Invalid option \'{where}\'',
			f'Execute in background: run bg',
			f'Execute in foreground: run fg'
		)
		return
	errors = ''
	for opt in su.iter_mod_opts_data(state.ACTIVE_MOD):
		if opt.required and opt.value == '':
			errors += f'\'{opt.name}\' is required\n'
	if errors:
		print(errors, end='')
		return
	where_to_execute[where]()
