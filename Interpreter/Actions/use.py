import Interpreter.state as state


# def execute(text):
# 	'''Use a module.'''
# 	if not text:
# 		print('Use what ?')
# 	else:
# 		try:
# 			mod_id = int(text)
# 		except ValueError:
# 			mod_id = text
# 		index = 0
# 		for mod_dir in state.MOD_DIRS:
# 			for mod_path in mod_dir.iterdir():
# 				if not mod_path.is_file():
# 					continue
# 				if mod_id == index or mod_id == str(mod_path):
# 					mod_inst = su.get_mod_inst(mod_path)
# 					opt_names = list()
# 					errors = ''
# 					for opt_data in su.iter_mod_opts_data(mod_inst):
# 						if opt_data.name in opt_names:
# 							errors += f'Option named \'{opt_data.name}\' already exists\n'
# 						else:
# 							opt_names.append(opt_data.name)
# 					if errors:
# 						print(errors, end='')
# 						return None
# 					state.ACTIVE_MOD = mod_inst
# 					state.ACTIVE_MOD_PROC = sn.Session(
# 						mod_inst
# 					)
# 					state.PROMPT = mod_path.stem + '>'
# 					return None
# 				index += 1
# 		else:
# 			raise su.CommonExc.get_exc(
# 				su.CommonExc.MOD_NF,
# 				mod_id
# 			)


def execute(text):
	'''Use a module.'''
	if not text:
		print('Use <module name>')
		return
	try:
		mod_index = int(text)
	except ValueError:
		state.MOD_HANDLER.set_mod_by_path(text)
	else:
		state.MOD_HANDLER.set_mod_by_index(mod_index)
