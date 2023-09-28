import OptionInterface.OptionInterface as opt_iface
import Interpreter.StateUtils as su
import Interpreter.state as state


# TODO:
# Replace "error" print statements with "RuntimeException".


def execute(text):
	'''Set an option for the chosen module.'''
	if not state.ACTIVE_MOD:
		print('Select module first')
		return None
	line = text.lstrip()
	if not line:
		print('set <opt_name> <value>')
		return None
	try:
		space_index = line.index(' ')
		name = line[0:space_index]
		value = line[space_index + 1:]
	except ValueError:
		name = line
		value = ''
	for obj in su.iter_mod_opts(state.ACTIVE_MOD):
		if obj.name == name:
			obj.value = value
			print(f'{name} => {value}')
			break
	else:
		print(f'No such option as \'{name}\'')


def complete(text):
	if not state.ACTIVE_MOD:
		return None
	completions = list()
	for params in su.iter_mod_opts_data(state.ACTIVE_MOD):
		if params.name.startswith(text):
			completions.append(params.name)
	return completions
