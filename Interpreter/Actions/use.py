import Interpreter.StateUtils as su
import Interpreter.state as state


def execute(text):
	if not text:
		print('Use what ?')
	else:
		try:
			mod_id = int(text)
		except ValueError:
			mod_id = text
		index = 0
		for mod_dir in state.MOD_DIRS:
			for mod_path in mod_dir.iterdir():
				if mod_id == index or mod_id == str(mod_path):
					mod_inst = su.get_mod_inst(mod_path)
					opt_names = list()
					errors = ''
					for opt_data in su.iter_mod_opts_data(mod_inst):
						if opt_data.name in opt_names:
							errors += f'Option named \'{opt_data.name}\' already exists\n'
						else:
							opt_names.append(opt_data.name)
					if errors:
						print(errors, end='')
						return None
					state.ACTIVE_MOD = mod_inst
					state.PROMPT = mod_path.stem + '>'
					return None
				index += 1
		else:
			raise su.CommonExc.get_exc(
				su.CommonExc.MOD_NF,
				mod_id
			)


# TODO:
# Need complete func
